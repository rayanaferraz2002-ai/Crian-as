# Checklist — aplicar no Premiere

## Importar

1. Coloque os 5 arquivos originais numa pasta (nomes exatos: MVI_9197.MP4, MVI_9199.MP4, MVI_9200.MP4, MVI_9201.MP4, Drop Top Summer (Instrumental).mp4).
2. Premiere → Arquivo → Importar → `sequencia.xml`. Se aparecer “Link Media”, aponte para essa pasta (ele acha os demais pelo nome).
   - Ou gere o XML já com o seu caminho: `python3 -I scripts/gerar_xml.py plano.json saida/sequencia.xml --base "/Users/VOCE/Terral"`.
3. Confira a sequência: 1080×1920, 23,976 fps, 00:00:20:00.

## O que conferir/aplicar (o XML não carrega bem)

| Timecode | Item | Instrução |
|---|---|---|
| 00:00:00:00 → 00:00:20:00 (todos os clipes) | Rotação | O XML aplica Rotação −90° e Escala 100. Se algum clipe vier deitado ou de cabeça para baixo, em Controles de Efeito → Movimento use −90 (ou 90) e Escala 100. A imagem deve preencher o quadro vertical inteiro. |
| 00:00:01:22 | Fusão A→B | Cross Dissolve de 4 quadros centrado no corte. Se não vier, aplique (Ctrl/Cmd+D). |
| 00:00:19:12 → 00:00:20:00 | Fade para preto | Cross Dissolve/Dip to Black de 12 quadros no fim do último clipe. |
| 00:00:18:12 → 00:00:20:00 | Fade-out da música | Constant Power de 1,5 s no fim das trilhas A1/A2. Se não vier, aplique. |
| 00:00:00:00 | Áudio dos clipes | O XML não traz o áudio de câmera (só a música). Mantenha assim. |
| 00:00:01:22 → 00:00:07:14 | Cor (opcional) | Planos do celular (MVI_9197) têm fundo preto e contraste diferente das cenas de balcão; ajuste fino opcional. |
| 00:00:15:22 → 00:00:18:15 | Cor | MVI_9201 está mais clara/quente que os demais (luminância ~84 vs ~65). Em Lumetri, baixe exposição ~0,3 e temperatura levemente para casar com 9199/9200. |
| 00:00:07:14 | Drop da música | Corte no drop. Opcional: punch-in leve (Escala 100→108 em 6 quadros) para marcar o drop — não pedido no roteiro. |
| — | Velocidade | Nenhuma alteração de velocidade aplicada (100% em todos). |
| — | Textos na tela | Nenhum (decisão: sem falas). Sem .srt. |

## Trocas depois

Edite `plano.json` (campo `entrada_s` ou `batidas` de um plano) e rode `bash scripts/rodar_tudo.sh --recalcular`. Os cortes se re-encaixam nas batidas e preview/XML/relatórios são refeitos.
