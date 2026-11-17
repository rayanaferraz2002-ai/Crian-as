#!/usr/bin/env bash
# Pipeline genérico. Uso: bash rodar_projeto.sh <pasta_projeto> [--recalcular]
# Variáveis: TRAB (pasta de trabalho: proxies/wav), BASE (pasta dos originais na máquina do Premiere)
set -euo pipefail
F=$(cd "$(dirname "$0")" && pwd); cd "$1"; shift || true
ORIG=$(python3 -I -c "import json;print(json.load(open('projeto.json'))['config']['originais_dir'])")
MUS=$(python3 -I -c "import json;print(json.load(open('projeto.json'))['config']['musica']['arquivo'])")
TRAB=${TRAB:-/home/user/trabalho_$(basename "$PWD")}; BASE=${BASE:-/Terral_material}
mkdir -p "$TRAB" analise saida
[ -f "$TRAB/musica.wav" ] || ffmpeg -v error -y -i "$ORIG/$MUS" -ac 2 -ar 48000 "$TRAB/musica.wav"
[ -f analise/musica.json ] || python3 -I "$F/analisar_musica.py" "$TRAB/musica.wav" analise/musica.json
GIRAR_HORARIO=$(python3 -I -c "import json;print(' '.join(json.load(open('projeto.json'))['config'].get('girar_horario',[])))") bash "$F/gerar_proxies.sh" "$ORIG" "$TRAB/proxies" "$TRAB/folhas" 4
python3 -I "$F/montar_plano.py" projeto.json analise/musica.json plano.json "$TRAB/proxies" ${1:-}
python3 -I "$F/render_preview.py" plano.json "$TRAB/proxies" "$TRAB/musica.wav" saida/preview.mp4
python3 -I "$F/gerar_xml.py" plano.json saida/sequencia.xml --base "$BASE"
python3 -I "$F/validar_xml.py" saida/sequencia.xml plano.json
python3 -I "$F/gerar_relatorio.py" projeto.json plano.json analise/musica.json saida
