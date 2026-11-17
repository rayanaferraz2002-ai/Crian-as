# Checklist — Premiere

## Importar

1. Ponha TODOS numa mesma pasta (mesmo que no Drive estejam em pastas diferentes): `Bed Time (Instrumental).mp4`, `C0075.MP4`, `C0080.MP4`, `C0081.MP4`, `C0082.MP4`, `C0088.MP4`, `C0091.MP4`, `C0098.MP4`, `C0100.MP4`, `C0106.MP4`, `C0108.MP4`, `C0110.MP4`, `C0115.MP4`, `C0119.MP4`, `C0120.MP4`, `C0121.MP4`, `C0134.MP4`, `C0146.MP4`, `C0147.MP4`, `C0150.MP4`, `C0227.MP4`, `C0229.MP4`, `PRINT_AVALIACAO_placeholder.png`, `REVIEW.m4a`.
2. Arquivo → Importar → `sequencia.xml`. Na janela “Link Media”, aponte para essa pasta (os demais são achados pelo nome).
3. Confira a sequência `Dra_avaliacoes_google_9x16`: 1080×1920, 29.970 fps, 00:00:39:24.

## Conferir / aplicar

| Timecode | Item | Instrução |
|---|---|---|
| 00:00:00:00 → 00:00:39:24 | Rotação | XML aplica Rotação 0° e Escala automática (preenche o quadro) em todos. Se algum vier deitado/invertido, corrija em Controles de Efeito → Movimento. |
| 00:00:39:09 → 00:00:39:24 | Fade para preto | 15 quadros no fim do último plano (se não vier, Dip to Black). |
| 00:00:37:24 → 00:00:39:24 | Fade-out da música | Constant Power no fim de A1/A2 (se não vier, aplique). |
| — | Áudio dos clipes | Não incluído (só música e locução na A3). |
| 00:00:00:00 → 00:00:02:26 | Título (cena 1) | Ferramenta Texto: 'Lendo avaliações do meu / consultório no Google', branco, negrito, centralizado no terço superior (veja preview). Duração = plano T1. |
| 00:00:02:26 → 00:00:34:14 | Legendas da locução | Arquivo → Importar → legendas.srt → arraste para a trilha de legendas (ou use Texto → Legendas). Estilo: branco, negrito, contorno preto, parte de baixo (veja preview). |
| 00:00:35:24 → 00:00:38:14 | Print (V2) | Clique no PRINT_AVALIACAO_placeholder.png na V2 → botão direito → 'Substituir pelo clipe' → imagem real do print. Escala ~85% da largura; fade de 8 quadros na entrada e saída (como na prévia). |
| 00:00:00:00 → 00:00:39:24 | Rotação/escala | Os clipes Sony devem aparecer em pé e preenchendo o quadro (Escala 50). Se algum vier deitado, Movimento → Rotação 90 (ou −90). |
| 00:00:00:00 → 00:00:39:24 | Fps misto | Clipes 23,976 numa sequência 29,97: o Premiere faz a conversão sozinho; confira o 1º quadro de 2–3 planos contra a prévia. |
| 00:00:02:26 → 00:00:34:14 | Música abaixo da voz | O XML corta a música em 3 trechos (0 dB / −14 dB / 0 dB) com cross-fade. Se preferir, junte e use keyframes de volume ou 'Essential Sound → Ducking'. |
| — | Velocidade | 100% em todos (nada aplicado). |
| — | Textos | Ver itens acima e `legendas.srt`. |

## Trocas

Edite `projeto.json` (entrada_s/batidas/clipe de um plano) e rode o script do projeto (`rodar.sh` na pasta, ou `bash ../ferramentas/rodar_projeto.sh .`). Para ajuste fino sem perder o resto, edite `plano.json` e rode com `--recalcular`.
