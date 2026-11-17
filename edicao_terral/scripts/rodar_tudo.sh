#!/usr/bin/env bash
# Pipeline completo. Uso: bash scripts/rodar_tudo.sh [--recalcular]
#   ORIG  = pasta dos originais (somente leitura)   TRAB = pasta de trabalho (proxies/wav)
#   BASE  = caminho dos originais na máquina onde o Premiere vai abrir (para o XML)
set -euo pipefail
cd "$(dirname "$0")/.."
ORIG=${ORIG:-/home/user/material_drive}; TRAB=${TRAB:-/home/user/trabalho}; BASE=${BASE:-/Terral_material}
MUS="$ORIG/Drop Top Summer (Instrumental).mp4"
mkdir -p "$TRAB" analise saida
[ -f "$TRAB/musica.wav" ] || ffmpeg -v error -y -i "$MUS" -ac 2 -ar 48000 "$TRAB/musica.wav"
[ -f analise/musica.json ] || python3 -I scripts/analisar_musica.py "$TRAB/musica.wav" analise/musica.json
bash scripts/gerar_proxies.sh "$ORIG" "$TRAB/proxies" "$TRAB/folhas" 4
python3 -I scripts/montar_plano.py analise/musica.json plano.json "$TRAB/proxies" ${1:-}
python3 -I scripts/render_preview.py plano.json "$TRAB/proxies" "$TRAB/musica.wav" saida/preview.mp4
python3 -I scripts/gerar_xml.py plano.json saida/sequencia.xml --base "$BASE"
python3 -I scripts/validar_xml.py saida/sequencia.xml plano.json
python3 -I scripts/gerar_relatorio.py plano.json analise/musica.json saida
