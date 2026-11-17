# Checklist — Premiere

## Importar

1. Ponha numa pasta os originais: `MVI_9111.MP4`, `MVI_9117.MP4`, `MVI_9149.MP4`, `MVI_9164.MP4`, `MVI_9167.MP4`, `MVI_9187.MP4`, `MVI_9205.MP4`, `When The Fog Lift (Instrumental).mp4`.
2. Arquivo → Importar → `sequencia.xml`. Na janela “Link Media”, aponte para essa pasta (os demais são achados pelo nome).
3. Confira a sequência `Terral_cafe_da_manha_9x16_20s`: 1080×1920, 23.976 fps, 00:00:20:02.

## Conferir / aplicar

| Timecode | Item | Instrução |
|---|---|---|
| 00:00:00:00 → 00:00:20:02 | Rotação | XML aplica Rotação -90° e Escala 100 em todos. Se algum vier deitado/invertido, corrija em Controles de Efeito → Movimento. |
| 00:00:19:14 → 00:00:20:02 | Fade para preto | 12 quadros no fim do último plano (se não vier, Dip to Black). |
| 00:00:18:14 → 00:00:20:02 | Fade-out da música | Constant Power no fim de A1/A2 (se não vier, aplique). |
| — | Áudio dos clipes | Não incluído (só música). |
| 00:00:00:00 → 00:00:20:02 | Câmera lenta (opcional) | 'Cinematográfico': se quiser, aplique 80–90% de velocidade nos planos 03, 05 e 12 e ajuste a duração para manter o corte na batida. Não aplicado para não deslocar os cortes. |
| 00:00:00:00 → 00:00:20:02 | Cor | Clipes de cozinha (03 e 10, MVI_9149) estão bem mais escuros (luminância ~50) que os de mesa (~115–140). Em Lumetri: +0,5 a +0,8 de exposição no 9149, ou um look quente único em toda a sequência (camada de ajuste). |
| 00:00:03:17 → 00:00:05:14 | Cor plano 03 | MVI_9149 escuro: subir exposição (ver item Cor). |
| 00:00:14:23 → 00:00:16:07 | Cor plano 10 | MVI_9149 escuro: subir exposição (ver item Cor). |
| — | Velocidade | 100% em todos (nada aplicado). |
| — | Textos | Nenhum. Sem .srt. |

## Trocas

Edite `projeto.json` (entrada_s/batidas/clipe de um plano) e rode `bash ../ferramentas/rodar_projeto.sh .`. Para ajuste fino sem perder o resto, edite `plano.json` e rode com `--recalcular`.
