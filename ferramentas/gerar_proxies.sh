#!/usr/bin/env bash
# Gera proxies 720x1280 (girados p/ vertical) e folhas de contato. Não toca nos originais.
# Uso: gerar_proxies.sh <pasta_originais> <pasta_proxies> <pasta_folhas> [fps_folha]
# GIRAR_HORARIO="MVI_9209 ..." = clipes que giram 90° horário (padrão: anti-horário)
set -euo pipefail
IN=$1; PX=$2; SH=$3; FPS=${4:-4}
mkdir -p "$PX" "$SH"
shopt -s nullglob
# ARQUIVOS="C0075.MP4 ..." limita aos arquivos listados; TRANSPOSE=none usa a rotação gravada no arquivo (autorotate)
if [ -n "${ARQUIVOS:-}" ]; then LISTA=(); for a in $ARQUIVOS; do LISTA+=("$IN/$a"); done; else LISTA=("$IN"/MVI_*.MP4 "$IN"/MVI_*.mp4 "$IN"/MVI_*.MOV); fi
for f in "${LISTA[@]}"; do
  b=$(basename "${f%.*}")
  tr=2; [[ " ${GIRAR_HORARIO:-} " == *" $b "* ]] && tr=1
  vf="transpose=$tr,"; [ "${TRANSPOSE:-}" = none ] && vf=""
  [ -f "$PX/$b.mp4" ] || ffmpeg -v error -y -i "$f" -vf "${vf}scale=720:1280,fps=30000/1001" -c:v libx264 -crf 23 -preset veryfast -an "$PX/$b.mp4"
  ffmpeg -v error -y -i "$PX/$b.mp4" -vf "fps=$FPS,scale=180:-1,drawtext=text='%{pts\:hms}':x=3:y=3:fontsize=14:fontcolor=yellow:box=1:boxcolor=black,tile=12x8" -frames:v 1 "$SH/$b.jpg"
done
