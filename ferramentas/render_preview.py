"""Renderiza preview.mp4 (720x1280) a partir do plano.json usando os proxies.
Uso: python3 -I render_preview.py <plano.json> <pasta_proxies> <musica_audio> <saida.mp4>
       [--locucao arquivo] [--ass legendas.ass] [--sobre ID=imagem.png ...]
"""
import sys, json, subprocess, os
plano_p, proxies, musica, out = sys.argv[1:5]
extra = sys.argv[5:]
def opt(nome):
    return extra[extra.index(nome) + 1] if nome in extra else None
imgs = dict(x.split("=", 1) for i, x in enumerate(extra) if i > 0 and extra[i - 1] == "--sobre")
P = json.load(open(plano_p)); cfg = P["config"]; ps = P["planos"]
FPS = cfg["fps_num"] / cfg["fps_den"]; fpsr = f'{cfg["fps_num"]}/{cfg["fps_den"]}'
total_f = cfg["duracao_final_f"]; total = total_f / FPS
inputs, filt, labels = [], [], []
# transições centradas no corte: o plano que sai ganha d/2 no fim, o que entra começa d/2 antes
for i, p in enumerate(ps):
    a, b = p["fonte_in_f"], p["fonte_out_f"]
    if i > 0 and ps[i-1].get("transicao_saida", {}).get("tipo") == "Cross Dissolve":
        a -= ps[i-1]["transicao_saida"]["frames"] // 2
    t = p.get("transicao_saida", {})
    if t.get("tipo") == "Cross Dissolve":
        b += t["frames"] - t["frames"] // 2
    inputs += ["-i", os.path.join(proxies, p["clipe"].rsplit(".", 1)[0] + ".mp4")]
    filt.append(f"[{i}:v]fps={fpsr},trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS,"
                f"scale=720:1280,setsar=1,format=yuv420p[v{i}]")
cur, cur_len = "v0", None
cur_len = (ps[0]["fonte_out_f"] + (ps[0].get("transicao_saida", {}).get("frames", 0)
           - ps[0].get("transicao_saida", {}).get("frames", 0)//2 if ps[0].get("transicao_saida", {}).get("tipo") == "Cross Dissolve" else 0)
           - ps[0]["fonte_in_f"])
for i in range(1, len(ps)):
    prev_t = ps[i-1].get("transicao_saida", {})
    seg_len = ps[i]["timeline_out_f"] - ps[i]["timeline_in_f"]
    t = ps[i].get("transicao_saida", {})
    extra_out = (t["frames"] - t["frames"]//2) if t.get("tipo") == "Cross Dissolve" else 0
    if prev_t.get("tipo") == "Cross Dissolve":
        d = prev_t["frames"]
        off = (cur_len - d) / FPS
        filt.append(f"[{cur}][v{i}]xfade=transition=fade:duration={d/FPS:.5f}:offset={off:.5f}[x{i}]")
        cur_len = cur_len - d + (seg_len + d//2 + extra_out)
    else:
        filt.append(f"[{cur}][v{i}]concat=n=2:v=1:a=0[x{i}]")
        cur_len = cur_len + seg_len + extra_out
    cur = f"x{i}"
last = ps[-1].get("transicao_saida", {})
fv = last.get("frames", cfg["musica"]["fade_video_frames"]) / FPS if last.get("tipo") == "Fade to Black" else 0
vf = f"[{cur}]trim=end_frame={total_f}"
if fv: vf += f",fade=t=out:st={total - fv:.4f}:d={fv:.4f}"
n = len(ps); idx = n + 1  # n = música; depois locução e imagens
vlab = "vfin"; filt.append(vf + f"[{vlab}]")
ins_extra = []
for k, s in enumerate(P.get("sobreposicoes", [])):
    if s["id"] not in imgs: continue
    ins_extra += ["-loop", "1", "-i", imgs[s["id"]]]
    a, b = s["timeline_in_f"] / FPS, s["timeline_out_f"] / FPS; fd = 0.25
    filt.append(f"[{idx}:v]scale=720*{s.get('largura_rel', 0.83)}:-1,format=rgba,fade=t=in:st={a:.3f}:d={fd}:alpha=1,"
                f"fade=t=out:st={b - fd:.3f}:d={fd}:alpha=1[img{k}]")
    filt.append(f"[{vlab}][img{k}]overlay=(W-w)/2:(H-h)/2:enable='between(t,{a:.3f},{b:.3f})':shortest=1[vo{k}]")
    vlab = f"vo{k}"; idx += 1
ass = opt("--ass")
if ass:
    filt.append(f"[{vlab}]ass={ass}:original_size={cfg['largura']}x{cfg['altura']}[vsub]"); vlab = "vsub"
filt.append(f"[{vlab}]null[vout]")
m = cfg["musica"]
vol = "1"
d = P.get("ducking")
if d:
    a, b, g, rmp = d["de_f"] / FPS, d["ate_f"] / FPS, 10 ** (d["ganho_db"] / 20), 0.4
    vol = (f"if(lt(t,{a - rmp}),1,if(lt(t,{a}),1-(1-{g})*(t-{a - rmp})/{rmp},if(lt(t,{b}),{g},"
           f"if(lt(t,{b + rmp}),{g}+(1-{g})*(t-{b})/{rmp},1))))")
filt.append(f"[{n}:a]atrim=start={m['inicio_s']}:duration={total:.4f},asetpts=PTS-STARTPTS,"
            f"volume='{vol}':eval=frame,afade=t=out:st={total - m['fade_out_s']:.4f}:d={m['fade_out_s']}[mus]")
loc = P.get("locucao"); locf = opt("--locucao")
if loc and locf:
    li = idx; ins_extra += ["-i", locf]; idx += 1
    filt.append(f"[{li}:a]atrim=start={loc['fonte_in_f'] / FPS:.4f}:end={loc['fonte_out_f'] / FPS:.4f},asetpts=PTS-STARTPTS,"
                f"aformat=channel_layouts=stereo,adelay={int(loc['timeline_in_f'] / FPS * 1000)}:all=1[voz]")
    filt.append(f"[mus][voz]amix=inputs=2:normalize=0:duration=first[aout]")
else:
    filt.append("[mus]anull[aout]")
cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-i", musica, *ins_extra, "-filter_complex", ";".join(filt),
       "-map", "[vout]", "-map", "[aout]", "-r", fpsr, "-c:v", "libx264", "-crf", "23", "-preset", "fast",
       "-c:a", "aac", "-b:a", "160k", "-t", f"{total:.4f}", "-movflags", "+faststart", out]
subprocess.run(cmd, check=True)
print("ok", out)
