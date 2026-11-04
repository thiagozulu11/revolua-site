# Revolua — Site institucional

Site estático com versões desktop e celular, fotografias e fontes locais.

## Arquivos

- `dist/`: site pronto para hospedagem, incluindo os recursos locais.
- `figma-reference.tsx` e `figma-mobile-reference.tsx`: referências exportadas do Figma.
- `build.py`: gera `dist/index.html` e `dist/layout.css` a partir das referências.
- `dist/site.css` e `dist/site.js`: estilos de interação e navegação.
- `.openai/hosting.json`: identidade da publicação original no Sites.

## Atualizar e conferir

```sh
python3 build.py
python3 scripts/validate-site.py
node --check dist/site.js
```

Para conferir no navegador:

```sh
python3 -m http.server 4173 --directory dist
```

Alterações no Figma precisam ser incorporadas ao código antes de gerar uma nova versão. O GitHub não recebe automaticamente as edições feitas no Figma.

O workflow `validate.yml` confere cada pull request e cada push na branch `main`. Após as verificações passarem, publica `dist/` no GitHub Pages. Pull requests apenas validam, sem publicar.

Para ativar, conecte este projeto a um repositório GitHub e configure **Settings → Pages → Source → GitHub Actions**. O workflow só estará ativo depois que os arquivos estiverem no repositório e o Pages estiver habilitado. A primeira execução bem-sucedida informará o novo endereço do site.

O fluxo de atualização é: incorporar as alterações ao código → commit → push em `main` → validação → publicação automática. Uma falha de validação impede a publicação daquela versão.

## Publicação original

https://revolua-apresentacao.rocky-field-2036.chatgpt.site

O endereço original permanece na versão publicada até que uma nova publicação seja concluída.

