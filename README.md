# Impulso — PWA

Sistema de execução para quem trava: um próximo passo por vez, foco cronometrado (Pomodoro) e trackers de corpo e sono. Funciona offline e instala na tela de início como um app.

## Como instalar no iPhone (17 Pro Max)

1. Abra a URL do app (Vercel) no **Safari**.
2. Toque no botão **Compartilhar** (o quadrado com a seta pra cima).
3. Role e toque em **Adicionar à Tela de Início**.
4. Confirme em **Adicionar**. O ícone do Impulso aparece na tela inicial e abre em tela cheia, sem a barra do Safari.

> O app mostra um lembrete com essas instruções na primeira vez que você abre no Safari.

## Deploy na Vercel

Repositório de site estático — não precisa de build.

1. Acesse [vercel.com/new](https://vercel.com/new) e faça login com o GitHub.
2. Importe o repositório `pedroaugustogmc-source/APP-PWA-IMPULSO`.
3. Framework Preset: **Other** · Build Command: *(vazio)* · Output Directory: *(vazio / raiz)*.
4. Clique em **Deploy**. Ao terminar, abra a URL `https://<seu-projeto>.vercel.app` no iPhone.

Cada `git push` para a branch conectada gera um novo deploy automático.

## Estrutura

```
index.html              app (uma página, tudo inline)
manifest.webmanifest    metadados do PWA (nome, ícones, cores)
sw.js                   service worker (funcionamento offline)
vercel.json             headers de cache / mime
icons/                  ícones do app (192, 512, maskable, apple-touch, favicon)
scripts/make_icons.py   gerador dos ícones (Pillow)
```

## Dados

Tudo é salvo **localmente no aparelho** (`localStorage`). Nada sai do dispositivo. "zerar tudo" no rodapé apaga os registros.
