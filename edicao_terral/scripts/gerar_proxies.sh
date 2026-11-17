#!/usr/bin/env bash
# Gera proxies 720x1280 (girados p/ vertical) e folhas de contato. Não toca nos originais.
# Uso: gerar_proxies.sh <pasta_originais> <pasta_proxies> <pasta_folhas> [fps_folha]
set -euo pipefail
IN=$1; PX=$2; SH=$3; FPS=${4:-4}
mkdir -p "$PX" "$SH"
for f in "$IN"/MVI_*.MP4; do
  b=$(basename "${f%.*}")
  [ -f "$PX/$b.mp4" ] || ffmpeg -v error -y -i "$f" -vf "transpose=2,scale=720:1280" -c:v libx264 -crf 23 -preset veryfast -an "$PX/$b.mp4"
  ffmpeg -v error -y -i "$PX/$b.mp4" -vf "fps=$FPS,scale=180:-1,drawtext=text='%{pts\:hms}':x=3:y=3:fontsize=14:fontcolor=yellow:box=1:boxcolor=black,tile=12x8" -frames:v 1 "$SH/$b.jpg"
done
