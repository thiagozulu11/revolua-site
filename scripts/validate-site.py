"""Check the actual static artifact before sending it to a host."""
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

DIST = Path(__file__).resolve().parents[1] / "dist"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
errors = []


def check_reference(value, origin):
    url = urlsplit(value)
    if url.scheme or url.netloc or not url.path:
        return
    resource = DIST / unquote(url.path.lstrip("/")) if url.path.startswith("/") else origin.parent / unquote(url.path)
    if not resource.is_file():
        errors.append(f"Missing resource in {origin.name}: {value}")


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.photos = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in VOID:
            self.stack.append(tag)
        if tag == "img":
            self.photos += 1
        for name in ("src", "href"):
            if attrs.get(name):
                check_reference(attrs[name], DIST / "index.html")

    def handle_startendtag(self, tag, attrs):
        if tag not in VOID:
            errors.append(f"Invalid self-closing HTML element: {tag}")
        else:
            self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            errors.append(f"Unbalanced HTML closing tag: {tag}")
        else:
            self.stack.pop()


page = Page()
page.feed((DIST / "index.html").read_text())
page.close()
if page.stack:
    errors.append(f"Unclosed HTML elements: {page.stack}")
if not page.photos:
    errors.append("The page contains no image elements")
for css in DIST.glob("*.css"):
    for reference in re.findall(r"url\(\s*['\"]?([^)'\"]+)", css.read_text()):
        check_reference(reference, css)
if errors:
    raise SystemExit("\n".join(errors))
print("Static site valid: balanced HTML and all local assets found.")
