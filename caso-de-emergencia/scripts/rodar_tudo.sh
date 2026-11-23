#!/bin/bash
# Refaz a edição a partir de decisoes.json (troque planos/tempos lá e rode de novo).
#   MIDIA="/pasta/dos/originais" CACHE="/tmp/cache_edicao" bash scripts/rodar_tudo.sh [--analisar] [--abertura]
#   --analisar : refaz análises (música, referência, transcrição) — só se trocar música/clipes
#   --abertura : re-renderiza abertura_tensao.mov (só se mudar o efeito/trecho da cena 1)
set -euo pipefail
cd "$(dirname "$0")"
: "${MIDIA:?defina MIDIA=pasta dos originais}"; CACHE="${CACHE:-/tmp/cache_edicao}"
for a in "$@"; do
  case "$a" in
    --analisar) python3 01_analisar_musica.py; python3 02_analisar_referencia.py
                python3 03_transcrever.py C0216 C0221 C0222 C0225 ;;
  esac
done
python3 04_montar_plano.py
for a in "$@"; do [ "$a" = "--abertura" ] && python3 05_render_abertura.py; done
python3 06_render_preview.py --cache "$CACHE"
python3 07_gerar_xml.py --src "$MIDIA" ${MEDIA_DIR:+--media-dir "$MEDIA_DIR"}
python3 08_validar_xml.py
python3 09_gerar_srt_checklist.py
