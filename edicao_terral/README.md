# Edição Terral — delivery 9:16 / 20 s

- `saida/preview.mp4` — prévia 720×1280
- `saida/sequencia.xml` — importar no Premiere (FCP7 XML)
- `saida/checklist_premiere.md` — o que conferir/aplicar no Premiere
- `saida/relatorio.md` — roteiro, cena → clipe, descartados, premissas
- `plano.json` — base da edição (cena → clipe, entrada/saída, transição)
- `analise/musica.json` — BPM, batidas, tempos fortes, seções de energia
- `scripts/` — pipeline (`bash scripts/rodar_tudo.sh [--recalcular]`)

Requisitos: ffmpeg, python3, librosa, opencv-python-headless, gdown (download), opentimelineio + otio-fcp-adapter (validação opcional).
Os originais não estão no repositório (baixar do Drive com `gdown --folder <url> -O <pasta>`).
