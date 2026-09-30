# Astera Engenharia Industrial: landing page

Página de apresentação da Astera (gestão de paradas, confiabilidade, projetos e painéis de manutenção), hospedada na Netlify a partir deste repositório.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `site/` | O que vai ao ar: `index.html` autocontido, `og-image.jpg` (preview de WhatsApp/Instagram), `obrigado.html` e `robots.txt` |
| `marca/` | Sugestões de logotipo em PNG transparente e a prancha de apresentação |
| `fonte/` | Código-fonte legível da página (`template.html`) e o script que gera `site/index.html` com fontes e imagens embutidas |
| `netlify.toml` | Diz à Netlify para publicar a pasta `site/` |

## Publicar na Netlify

1. Na Netlify: **Add new site > Import an existing project > GitHub** e escolha este repositório.
2. Deixe o comando de build vazio. A pasta de publicação já vem do `netlify.toml` (`site`).
3. Depois do primeiro deploy, abra **Forms** e confirme que o formulário `diagnostico` aparece.
4. Em **Site configuration > Notifications > Form submission notifications**, adicione o e-mail que deve receber as solicitações.

Cada `git push` na branch principal publica uma nova versão automaticamente.

## Antes de divulgar o link

- **Domínio:** troque `https://www.astera.eng.br` em `fonte/template.html` pelo endereço real (o `xxx.netlify.app` ou o domínio próprio). Sem isso, a imagem de preview não aparece no WhatsApp.
- **Contatos:** e-mail e WhatsApp no rodapé e em `CONFIG.email`, no fim do template.
- **Resultados de exemplo:** os três números da faixa azul (−3 dias, −38%, 1 painel) são ilustrativos. Estão marcados com `EXEMPLO` no código.

## Editar o conteúdo

Edite `fonte/template.html` (texto e estilo, sem os blocos base64) e gere a página:

```bash
python3 fonte/build.py
```

O script grava o resultado em `site/index.html`. Precisa só de Python 3, sem dependências.
Pequenas correções de texto também podem ser feitas direto em `site/index.html`.
