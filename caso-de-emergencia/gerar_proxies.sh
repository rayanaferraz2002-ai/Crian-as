#!/bin/bash
# ---------------------------------------------------------------------------
# gerar_proxies.sh — cria proxies leves (ProRes Proxy + PCM) de TODOS os vídeos
# de uma pasta, para editar no Premiere sem travar.
#
#   Uso:  bash gerar_proxies.sh "/caminho/da/pasta/dos/originais"  [pasta_saida]
#
# - NÃO altera nem apaga os originais (só lê). Grava em <pasta>/proxies/
# - Mesmo nome base: C0216.MP4 -> proxies/C0216.mov
# - Mesma duração, fps, canais de áudio e orientação (vertical continua vertical)
# - Lado maior = 1280 px, proporção mantida
# - Pula o que já foi gerado; mostra o progresso; confere a duração no fim
# Compatível com macOS 12 (bash 3.2) e Linux. Requer ffmpeg + ffprobe.
# ---------------------------------------------------------------------------
set -u

ENTRADA="${1:-}"
if [ -z "$ENTRADA" ] || [ ! -d "$ENTRADA" ]; then
  echo "Uso: bash $0 \"/pasta/dos/originais\" [pasta_saida]"; exit 1
fi
ENTRADA="${ENTRADA%/}"
SAIDA="${2:-$ENTRADA/proxies}"
LADO=1280

for b in ffmpeg ffprobe; do
  command -v "$b" >/dev/null 2>&1 || { echo "ERRO: '$b' não encontrado. Veja o LEIA-ME (instalar ffmpeg)."; exit 1; }
done
mkdir -p "$SAIDA" || exit 1

# --- lista os vídeos (só arquivos com faixa de vídeo) ---
ARQS=()
for f in "$ENTRADA"/*; do
  [ -f "$f" ] || continue
  ext=$(echo "${f##*.}" | tr '[:upper:]' '[:lower:]')
  case "$ext" in mp4|mov|mxf|m4v|mts|avi) ;; *) continue ;; esac
  v=$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_type -of csv=p=0 "$f" 2>/dev/null | head -1 | cut -d, -f1)
  [ "$v" = "video" ] && ARQS+=("$f")
done
TOTAL=${#ARQS[@]}
[ "$TOTAL" -eq 0 ] && { echo "Nenhum vídeo em $ENTRADA"; exit 0; }
echo "Originais: $ENTRADA"
echo "Proxies:   $SAIDA"
echo "$TOTAL vídeo(s) encontrados."
echo

dur() { ffprobe -v error -show_entries format=duration -of csv=p=0 "$1" 2>/dev/null; }
tam() { du -hL "$1" | cut -f1; }

N=0; FEITOS=0; PULADOS=0; FALHAS=0
for f in "${ARQS[@]}"; do
  N=$((N+1))
  nome=$(basename "$f"); base="${nome%.*}"
  out="$SAIDA/$base.mov"; tmp="$SAIDA/.$base.parcial.mov"
  if [ -s "$out" ]; then
    echo "[$N/$TOTAL] $nome  -> já existe, pulando"; PULADOS=$((PULADOS+1)); continue
  fi
  fps=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$f" | head -1 | cut -d, -f1)
  tc=$(ffprobe -v error -show_entries format_tags=timecode:stream_tags=timecode -of csv=p=0 "$f" 2>/dev/null | grep -m1 ':' | tr -d ',')
  tcopt=(); [ -n "$tc" ] && tcopt=(-timecode "$tc")
  echo "[$N/$TOTAL] $nome  ($fps fps) -> proxies/$base.mov"
  # autorrotação ligada (padrão do ffmpeg): o proxy já sai na orientação em que o vídeo é exibido.
  # scale: lado maior = 1280, o outro proporcional e par.
  ffmpeg -hide_banner -v error -stats -nostdin -y -i "$f" \
    -map 0:v:0 -map '0:a?' -map_metadata 0 \
    -vf "scale='if(gte(iw,ih),$LADO,-2)':'if(gte(iw,ih),-2,$LADO)':flags=bicubic" \
    -r "$fps" -c:v prores_ks -profile:v 0 -vendor apl0 -pix_fmt yuv422p10le \
    -c:a pcm_s16le ${tcopt[@]+"${tcopt[@]}"} -f mov "$tmp"
  if [ $? -ne 0 ] || [ ! -s "$tmp" ]; then
    echo "   ERRO ao converter $nome"; rm -f "$tmp"; FALHAS=$((FALHAS+1)); continue
  fi
  mv "$tmp" "$out"
  d1=$(dur "$f"); d2=$(dur "$out")
  ok=$(awk -v a="$d1" -v b="$d2" 'BEGIN{d=a-b; if(d<0)d=-d; print (d<=0.05)?"OK":"DIFERENTE"}')
  echo "   duração original ${d1}s | proxy ${d2}s [$ok] | tamanho $(tam "$f") -> $(tam "$out")"
  FEITOS=$((FEITOS+1))
done
echo
echo "Concluído: $FEITOS gerado(s), $PULADOS pulado(s), $FALHAS falha(s)."
[ "$FALHAS" -eq 0 ]
