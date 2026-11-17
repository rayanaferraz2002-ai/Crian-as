"""Analisa a música: BPM, batidas, tempos fortes (downbeats estimados) e seções de energia.
Uso: python3 -I analisar_musica.py <audio> <saida.json>
"""
import sys, json
import numpy as np
import librosa

src, out = sys.argv[1], sys.argv[2]
y, sr = librosa.load(src, sr=22050, mono=True)
dur = len(y) / sr
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="frames")
tempo = float(np.atleast_1d(tempo)[0])
beat_t = librosa.frames_to_time(beats, sr=sr)
onset = librosa.onset.onset_strength(y=y, sr=sr)
# tempo forte: fase de 4 com maior soma de onset nas batidas
strength = onset[np.clip(beats, 0, len(onset) - 1)]
phase = int(np.argmax([strength[p::4].sum() for p in range(4)]))
downbeats = beat_t[phase::4]
# energia RMS por segundo, suavizada
rms = librosa.feature.rms(y=y)[0]
rms_t = librosa.frames_to_time(np.arange(len(rms)), sr=sr)
sec = np.arange(0, int(dur))
energy = np.array([rms[(rms_t >= s) & (rms_t < s + 1)].mean() for s in sec])
e_s = np.convolve(energy, np.ones(4) / 4, mode="same")
e_n = (e_s - e_s.min()) / (e_s.max() - e_s.min() + 1e-9)
# seções: segmentação por mudança de nível de energia em blocos de compasso (4 batidas)
bars = list(downbeats) + [dur]
bar_e = [float(e_n[int(a):max(int(a) + 1, int(b))].mean()) for a, b in zip(bars[:-1], bars[1:])]
def label(v):
    return "baixa" if v < 0.35 else ("media" if v < 0.7 else "alta")
sections, cur = [], None
for (a, b), v in zip(zip(bars[:-1], bars[1:]), bar_e):
    l = label(v)
    if cur and cur["energia"] == l:
        cur["fim"] = round(b, 3)
    else:
        cur = {"inicio": round(a, 3), "fim": round(b, 3), "energia": l}
        sections.append(cur)
json.dump({
    "arquivo": src, "duracao": round(dur, 3), "bpm": round(tempo, 2),
    "intervalo_batida": round(60 / tempo, 4),
    "batidas": [round(t, 3) for t in beat_t],
    "tempos_fortes": [round(t, 3) for t in downbeats],
    "energia_por_segundo": [round(float(v), 3) for v in e_n],
    "secoes": sections,
}, open(out, "w"), indent=1)
print(f"dur {dur:.1f}s  bpm {tempo:.2f}  batidas {len(beat_t)}  fase forte {phase}")
for s in sections:
    print(f"  {s['inicio']:7.2f}-{s['fim']:7.2f}  {s['energia']}")
