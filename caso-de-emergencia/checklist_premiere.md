# Checklist — aplicar no Premiere

Timecodes da sequência `CASO DE EMERGENCIA` (23,976 fps, começa em 00:00:00:00).

## 0. Ao importar
- [ ] **Vincular mídia** aos ORIGINAIS (ver LEIA-ME). `abertura_tensao.mov` fica na mesma pasta dos originais.
- [ ] Se algum clipe 4K aparecer **deitado**: Efeitos > Controles de efeito > Movimento > Rotação = 90° (o XML assume que o Premiere lê a rotação do arquivo, como faz nas versões atuais).
- [ ] Conferir se os clipes 4K vieram com **Escala 50%** (ocupam o quadro 1080×1920 inteiro).

## 1. Cena 1 — abertura (00:00:00:00 → 00:00:08:06)
- [ ] **SFX de telefone** na trilha A5 em 00:00:00:00 (marcador "SFX telefone"). Não havia esse som no Drive.
- [ ] **Texto "E AGORA DOUTORA?"** de 00:00:00:17 até 00:00:08:05: Gráficos essenciais, fonte sem serifa extra-negrito, branco, terço superior (Y ≈ 25%). Ou importe `texto_na_tela.srt`.
- [ ] O visual P&B + efeito já está **renderizado** em `abertura_tensao.mov` — nada a aplicar. Se quiser refazer no Premiere sobre o `C0120.MP4` original:

| Parâmetro | Início (00:00:00:00) | Fim (00:00:08:05) | Onde |
|---|---|---|---|
| Velocidade | 66.7% (Interpolação: Fluxo óptico) | — | Clique direito > Velocidade/Duração |
| Saturação | 0 | 0 | Lumetri > Correção básica |
| Contraste | +25 | +55 (keyframe linear) | Lumetri > Correção básica |
| Vinheta (Quantidade) | -1,5 | -3,0 (keyframe linear); Ponto médio 40, Difusão 50 | Lumetri > Vinheta |
| Grão | Ruído 8% (desmarcar ruído colorido) | igual | Efeitos > Ruído e granulação > Ruído |
| Escala | 50% | 60% (Bezier, **aceleração no fim** = ease-in) | Movimento |
| Posição | 540 × 960 | 540 × 914 (acompanha o zoom em direção às mãos) | Movimento |

- [ ] Virada P&B → cor em **00:00:08:06** = drop da música (112.501 s da faixa, tempo forte). Não mover.

## 2. Enquadramentos (zoom digital nos originais 4K) — o XML já leva, só conferir

| Plano | Entrada | Saída | Clipe | Escala | Posição (X × Y) |
|---|---|---|---|---|---|
| V02 aberto | 00:00:08:06 | 00:00:15:04 | C0216.MP4 | 50% | 540 × 960 |
| V03 fechado | 00:00:15:04 | 00:00:18:15 | C0221.MP4 | 60% | 540 × 1018 |
| V04 aberto | 00:00:18:15 | 00:00:26:21 | C0221.MP4 | 50% | 540 × 960 |
| V05 broll | 00:00:26:21 | 00:00:31:00 | C0150.MP4 | 50% | 540 × 960 |
| V06 fechado | 00:00:31:00 | 00:00:35:20 | C0221.MP4 | 60% | 540 × 1018 |
| V07 close | 00:00:35:20 | 00:00:38:14 | C0221.MP4 | 67.5% | 540 × 1094 |
| V08 aberto | 00:00:38:14 | 00:00:42:00 | C0222.MP4 | 50% | 540 × 960 |
| V09 fechado | 00:00:42:00 | 00:00:47:13 | C0222.MP4 | 60% | 540 × 1018 |
| V10 aberto | 00:00:47:13 | 00:00:51:16 | C0225.MP4 | 50% | 540 × 960 |

- [ ] B-roll `C0150.MP4` entra **sem áudio** (o som ambiente tem conversa). Se o Premiere trouxer áudio vinculado, apague.

## 3. Textos e legendas
- [ ] Arquivo > Importar `legendas.srt` → arrastar para a linha do tempo (cria trilha de legendas). Revisar grafia: a transcrição é automática e foi corrigida à mão.
- [ ] Estilo sugerido (como na referência): branco, contorno preto fino, centralizado a ~65% da altura.

## 4. Áudio
- [ ] Locução (A1/A2, áudio da câmera): Som essencial > Diálogo > Loudness: Corresponder automaticamente (-16 LUFS para Reels).
- [ ] Música (A3/A4): o XML leva keyframes de nível. Conferir:
  - 00:00:00:00: +0.0 dB
  - 00:00:08:09: +0.0 dB
  - 00:00:08:18: -16.5 dB
  - 00:00:50:16: -16.5 dB
  - 00:00:50:22: -6.9 dB
  - 00:00:51:16: -∞ dB
  Se os keyframes não vierem, recrie com a ferramenta Caneta nos pontos acima.
- [ ] **Fade-out da música** nos últimos 2 tempos (marcador "Fade-out música").

## 5. Final
- [ ] Mergulho para preto (12 quadros) no fim — o XML leva uma Dissolução cruzada; se não vier, aplique *Mergulhar para preto*.
- [ ] **Desligar o botão de proxy** antes de exportar. Exportar H.264, 1080×1920, 23,976, "Corresponder à sequência", taxa alvo 16–20 Mbps.
