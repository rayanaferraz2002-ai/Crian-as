"""PASSO 3 — Música: BPM, batidas, tempos fortes, seções de energia e melhor drop.
Uso: python3 01_analisar_musica.py --src PASTA_ORIGINAIS"""
import argparse, subprocess, tempfile
import numpy as np, librosa
from comum import ANALISE, MUSICA, midia_dir, gravar_json

ap = argparse.ArgumentParser(); ap.add_argument("--src"); a = ap.parse_args()
src = midia_dir(a.src) / MUSICA
with tempfile.NamedTemporaryFile(suffix=".wav") as w:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-ac", "1", "-ar", "22050", w.name], check=True)
    y, sr = librosa.load(w.name, sr=22050)

tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
bpm = float(np.atleast_1d(tempo)[0])
onset = librosa.onset.onset_strength(y=y, sr=sr); ot = librosa.times_like(onset, sr=sr)
forca = np.interp(beats, ot, onset)
fase = int(max(range(4), key=lambda p: forca[p::4].mean()))       # fase do tempo 1 do compasso
rms = librosa.feature.rms(y=y)[0]; t = librosa.times_like(rms, sr=sr)
perc = librosa.feature.rms(y=librosa.effects.percussive(y))[0]

downs = beats[fase::4]
compassos = []
for i in range(len(downs) - 1):
    m = (t >= downs[i]) & (t < downs[i + 1])
    compassos.append({"inicio": round(float(downs[i]), 3), "energia": round(float(rms[m].mean()), 4),
                      "percussao": round(float(perc[m].mean()), 4)})

# seções: rotula pela energia percussiva (break = percussão < 40% da mediana)
med = np.median([c["percussao"] for c in compassos])
for c in compassos:
    p = c["percussao"]
    c["secao"] = "break/tensao" if p < 0.45 * med else ("alta" if c["energia"] > 0.15 else "media")
# drop = compasso cuja percussão mais cresce em relação aos 4 anteriores
ganhos = [(compassos[i]["percussao"] / (np.mean([c["percussao"] for c in compassos[i-4:i]]) + 1e-6), i)
          for i in range(4, len(compassos))]
ganho, idx = max(ganhos)
drop = compassos[idx]["inicio"]

dados = {"arquivo": MUSICA, "duracao": round(len(y) / sr, 3), "bpm": round(bpm, 2),
         "periodo_batida": round(float(np.median(np.diff(beats))), 4), "fase_tempo_forte": fase,
         "batidas": [round(float(b), 3) for b in beats],
         "tempos_fortes": [round(float(b), 3) for b in downs],
         "compassos": compassos,
         "melhor_drop_para_virada": {"tempo": drop, "ganho_percussao": round(float(ganho), 2)}}
gravar_json(ANALISE / "mapa_batidas.json", dados)
with open(ANALISE / "mapa_batidas.csv", "w") as f:
    f.write("batida,tempo_s,tempo_forte\n")
    for i, b in enumerate(beats):
        f.write(f"{i},{b:.3f},{int(i % 4 == fase)}\n")
print(f"BPM {bpm:.2f} | {len(beats)} batidas | drop sugerido {drop:.3f}s (ganho x{ganho:.1f})")
