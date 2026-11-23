"""Transcreve a fala dos clipes (faster-whisper, modelo small, pt) com tempo por palavra.
Uso: python3 03_transcrever.py --src PASTA C0216 C0221 ...   -> analise/transcricoes.json"""
import argparse, subprocess, tempfile
import soundfile as sf
from faster_whisper import WhisperModel
from comum import ANALISE, midia_dir, gravar_json

ap = argparse.ArgumentParser(); ap.add_argument("--src"); ap.add_argument("clipes", nargs="+"); a = ap.parse_args()
m = WhisperModel("small", device="cpu", compute_type="int8")
saida = {}
for c in a.clipes:
    arq = next(midia_dir(a.src).glob(c + ".*"))
    with tempfile.NamedTemporaryFile(suffix=".wav") as w:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(arq), "-ac", "1", "-ar", "16000", w.name], check=True)
        audio, _ = sf.read(w.name, dtype="float32")
    segs, _ = m.transcribe(audio, language="pt", word_timestamps=True)
    saida[c] = [{"inicio": round(s.start, 2), "fim": round(s.end, 2), "texto": s.text.strip(),
                 "palavras": [[w.word.strip(), round(w.start, 2), round(w.end, 2)] for w in s.words]} for s in segs]
    print(c, " | ".join(s["texto"] for s in saida[c]))
gravar_json(ANALISE / "transcricoes.json", saida)
