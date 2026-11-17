#!/usr/bin/env bash
# Refaz tudo deste projeto. Uso: bash rodar.sh [--recalcular]   (BASE = pasta dos originais no seu computador)
set -euo pipefail; cd "$(dirname "$0")"; F=../ferramentas; T=${TRAB:-/home/user/trabalho_dra}; BASE=${BASE:-/Terral_material}
python3 -I $F/montar_plano.py projeto.json analise/musica.json plano.json $T/proxies ${1:-}
python3 -I $F/gerar_legendas.py plano.json analise/review_transcricao.json saida/legendas
python3 -I $F/render_preview.py plano.json $T/proxies $T/musica.wav saida/preview.mp4 --locucao /home/user/material_dra/feitos/REVIEW.m4a --ass saida/legendas.ass --sobre PRINT=saida/PRINT_AVALIACAO_placeholder.png
python3 -I $F/gerar_xml.py plano.json saida/sequencia.xml --base "$BASE" --sobre PRINT=saida/PRINT_AVALIACAO_placeholder.png
python3 -I $F/validar_xml.py saida/sequencia.xml plano.json
python3 -I $F/gerar_relatorio.py projeto.json plano.json analise/musica.json saida
