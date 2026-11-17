# Checklist — Premiere

## Importar

1. Ponha numa pasta os originais: `MVI_9068.MP4`, `MVI_9069.MP4`, `MVI_9072.MP4`, `MVI_9074.MP4`, `MVI_9081.MP4`, `MVI_9086.MP4`, `MVI_9087.MP4`, `MVI_9088.MP4`, `MVI_9152.MP4`, `MVI_9153.MP4`, `MVI_9161.MP4`, `MVI_9162.MP4`, `MVI_9209.MP4`, `Quanta Saudade (Feels Like Heaven) (Instrumental) (1).mp4`.
2. Arquivo → Importar → `sequencia.xml`. Na janela “Link Media”, aponte para essa pasta (os demais são achados pelo nome).
3. Confira a sequência `Terral_almoco_executivo_9x16_30s`: 1080×1920, 23.976 fps, 00:00:29:23.

## Conferir / aplicar

| Timecode | Item | Instrução |
|---|---|---|
| 00:00:00:00 → 00:00:29:23 | Rotação | XML aplica Rotação -90° e Escala 100 em todos. Se algum vier deitado/invertido, corrija em Controles de Efeito → Movimento. |
| 00:00:29:11 → 00:00:29:23 | Fade para preto | 12 quadros no fim do último plano (se não vier, Dip to Black). |
| 00:00:28:11 → 00:00:29:23 | Fade-out da música | Constant Power no fim de A1/A2 (se não vier, aplique). |
| — | Áudio dos clipes | Não incluído (só música). |
| 00:00:00:00 → 00:00:29:23 | Cor | A referência tem tom quente/âmbar. Sugestão: camada de ajuste com Lumetri (temperatura +10, saturação +5) para unificar ambientes (claros) e pratos (mais quentes). |
| 00:00:00:00 → 00:00:02:01 | Rotação 9209 | MVI_9209 usa +90° (os demais −90°). Confira se o salão está de pé. |
| — | Velocidade | 100% em todos (nada aplicado). |
| — | Textos | Nenhum. Sem .srt. |

## Trocas

Edite `projeto.json` (entrada_s/batidas/clipe de um plano) e rode `bash ../ferramentas/rodar_projeto.sh .`. Para ajuste fino sem perder o resto, edite `plano.json` e rode com `--recalcular`.
