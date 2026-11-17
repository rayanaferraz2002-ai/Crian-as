# Relatório de edição — Terral — café da manhã (cinematográfico, takes curtos)

## Material recebido e interpretação

Estrutura do Drive diferente da esperada (arquivos soltos). Interpretação:

| Arquivo | Interpretado como | Observação |
|---|---|---|
| When The Fog Lift (Instrumental).mp4 | musica/ | Só áudio AAC, 181,9 s |
| PlantersInnChs_pindown.io_1794924184.mp4 | referencia/ | Vídeo do Pinterest, 720×1280, 30 fps, 8,76 s |
| MVI_9205.MP4 | clipes/ | Homem escrevendo 'Café Colonial' na lousa. 4,7 s |
| MVI_9164.MP4 | clipes/ | Travelling de cima: pratos → suco + café com leite. 7,9 s |
| MVI_9149.MP4 | clipes/ | Café saindo da máquina na xícara (desfocado até ~3 s). 9,3 s |
| MVI_9167.MP4 | clipes/ | Café com leite visto de cima. 4,4 s |
| MVI_9117.MP4 | clipes/ | Prato de frutas/queijo/presunto/pão + mel escorrendo. 11,1 s |
| MVI_9111.MP4 | clipes/ | Bolo de fubá com goiabada; mão desfocada até 4,5 s; fatia levantada em 6,1 s. 7,5 s |
| MVI_9187.MP4 | clipes/ | Mesa posta; foco passa da mesa para as pessoas ao fundo. 6,0 s |
| MVI_9115.MP4 | clipes/ (novo) | Pegador tirando melancia da travessa de frutas. 7,9 s |
| MVI_9099.MP4 | clipes/ (novo) | Queijos com rosa de tomate, close. 3,1 s |
| MVI_9120.MP4 | clipes/ (novo) | Jarra de suco → pratos (câmera descendo). 9,6 s |
| — | roteiro/ | Ausente; usado o roteiro da conversa (1 frase) |
| — | locucao/ | Ausente |

Clipes 1920×1080 23,976 fps gravados com câmera deitada (conteúdo vertical): girados −90° → 1080×1920.

## Passo 1 — Roteiro

| Cena | Direção de imagem | Direção de edição | Duração | Áudio/fala |
|---|---|---|---|---|
| Única | Café da manhã do Terral | Cinematográfico, takes curtos | Não definida → ~20 s (sua decisão) | Nenhuma (só música) |

## Passo 2 — Referência

- 8,76 s, 9:16 (720×1280), 30 fps, 6 planos, só cortes secos (sem transição).
- Cortes em 1,63 / 4,00 / 4,87 / 6,47 / 7,23 s → planos de 0,77–2,37 s (média 1,46 s), alternando longo e curto.
- Áudio da referência ~92 BPM (librosa mede 184): corte a cada ~2–4 batidas, ritmo constante do início ao fim.
- Estrutura: fachada com título → mesa vista de cima → leite no café → corte do prato → mexendo o café → mesa em plano aberto.
- Título na tela ('Sunday Brunch…') nos primeiros 4 s: não reproduzido (sua decisão: sem texto).

## Passo 3 — Música

- BPM **129.2** (batida 0.4644 s), 381 batidas.
- Seções de energia (s): 1.6–9.1 baixa; 9.1–12.8 media; 12.8–53.4 alta; 53.4–57.1 media; 57.1–103.5 alta; 103.5–105.5 media; 105.5–176.0 alta; 176.0–181.9 media
- Trecho usado: **1.625 → 21.728 s**. Drop em 12.841 s = 00:00:11:05 na timeline.
- Mapa de batidas: `analise/musica.json`.

## Passo 4/5 — Plano → clipe escolhido

| # | Cena | Arquivo original | Entrada → saída (fonte) | Timeline | Batidas | Motivo | Nitidez/mov./lum. |
|---|---|---|---|---|---|---|---|
| 01 | Abertura | MVI_9205.MP4 | 1.00 → 2.84 s | 00:00:00:00 → 00:00:01:20 | 4 | Lousa 'Café Colonial' sendo escrita: apresenta o lugar, como a fachada com título da referência. | 1039.9/3.23/78.5 |
| 02 | Detalhes (intro) | MVI_9164.MP4 | 0.00 → 1.88 s | 00:00:01:20 → 00:00:03:17 | 4 | Travelling de cima sobre pratos (pão, frutas, frios): equivale ao plano de mesa vista de cima da referência. | 144.3/6.85/127.8 |
| 03 | Detalhes (intro) | MVI_9149.MP4 | 3.10 → 4.96 s | 00:00:03:17 → 00:00:05:14 | 4 | Café saindo da máquina na xícara (trecho já em foco; antes de 3 s está desfocado): equivale ao 'leite no café' da referência. | 430.8/1.92/50.2 |
| 04 | Detalhes (intro) | MVI_9167.MP4 | 0.30 → 2.17 s | 00:00:05:14 → 00:00:07:11 | 4 | Café com leite visto de cima, espuma em movimento. | 120.9/5.39/114.3 |
| 05 | Detalhes (subida) | MVI_9117.MP4 | 3.60 → 5.46 s | 00:00:07:11 → 00:00:09:08 | 4 | Pegador de mel entra e escorre sobre o prato de frutas e queijo. | 141.3/4.18/135.4 |
| 06 | Detalhes (subida) | MVI_9111.MP4 | 4.55 → 6.42 s | 00:00:09:08 → 00:00:11:05 | 4 | Bolo de fubá com goiabada: câmera passa pelo bolo e a fatia é levantada no fim (ação de servir, como o corte do prato na referência). Antes de 4,5 s há mão desfocada no primeiro plano. | 104.9/6.47/122.0 |
| 07 | Detalhes (clímax) | MVI_9115.MP4 | 1.40 → 3.34 s | 00:00:11:05 → 00:00:13:03 | 4 | Corte depois do drop: pegador tira a melancia da travessa de frutas (ação de servir, nítido 1,2–3,5 s). | 89.1/9.67/152.1 |
| 08 | Detalhes (clímax) | MVI_9099.MP4 | 1.50 → 2.88 s | 00:00:13:03 → 00:00:14:12 | 3 | Take curto em close: queijos com rosa de tomate (trecho mais nítido do clipe). | 39.6/3.01/103.6 |
| 09 | Detalhes (clímax) | MVI_9120.MP4 | 5.00 → 6.80 s | 00:00:14:12 → 00:00:16:07 | 4 | Câmera desce da jarra de suco para os pratos (pão, frios, melancia): prepara o plano aberto final. | 32.3/6.42/136.5 |
| 10 | Fechamento | MVI_9187.MP4 | 2.15 → 5.96 s | 00:00:16:07 → 00:00:20:02 | 8 | Mesa posta nítida e o foco passa para as pessoas tomando café ao fundo: plano aberto final com fade, como na referência. | 151.7/4.06/129.4 |

Duração 20.103 s (482 quadros), 10 planos, média 2.01 s (mín 1.38, máx 3.80).
10 planos, 1 por clipe (sem repetição). Intro: 4 batidas (1,86 s) por plano. Depois do drop: 3–4 batidas, com take curto de 3 batidas no meio. Final: 8 batidas (mesa + passagem de foco) com fade.
Transições: corte seco na batida; 10: Fade to Black 12 quadros. Fade-out da música 1.5 s.

## Descartados

| Trecho | Motivo |
|---|---|
| MVI_9149 0–3,0 s | Fora de foco (nitidez 4–18 vs >400 depois). |
| MVI_9111 0–4,5 s | Mão desfocada em primeiro plano; quadro poluído. |
| MVI_9111 6,5 s → fim | Fatia sai do quadro; plano vazio. |
| MVI_9205 0–0,9 s | Câmera ajustando, quadro instável. |
| MVI_9187 0–3,5 s | Mesa nítida mas sem a passagem de foco; o trecho escolhido contém a mesa e termina nas pessoas. |
| MVI_9117 0–3,5 s | Prato parado, sem mel (menos ação). |
| MVI_9115 4,0 s → fim | Melancia já saiu do quadro; travessa parada e desfocada no fim. |
| MVI_9120 0–4,5 s | Jarra parada; o trecho com movimento para os pratos é mais forte. |
| MVI_9099 0–1,5 s | Menos nítido que o fim do clipe. |
| Versão anterior (v1) | Repetia 5 clipes (9164, 9117, 9167, 9149, 9205). Substituídos pelos 3 novos + plano final mais longo. v1 salva em projeto_v1.json do trabalho. |

## Premissas

1. Duração ~20 s, sem texto, abertura com a lousa e fechamento com a mesa posta: decisões suas.
2. Formato: a regra pede a resolução/fps da referência (720×1280, 30 fps). Usei 9:16 (mesma proporção) em 1080×1920 e 23,976 fps, porque a referência é um download do Pinterest em baixa resolução, e passar os clipes de 23,976 para 30 fps faria a imagem trepidar. Para seguir a referência à risca, troque fps_num/fps_den/largura/altura no projeto.json e rode de novo.
3. Sem repetição de clipe (seu pedido). Com 10 clipes para 20 s, os planos ficaram um pouco mais longos (média 2 s) que os da referência (1,46 s); o plano final tem 3,7 s para caber a passagem de foco inteira.
4. Trecho da música: 1,625 s → 21,73 s (começa num tempo forte). O drop (12,84 s) cai no corte bolo → melancia: a fatia sobe no fim do plano 06 e o pegador entra no 07; os takes mais curtos ficam na parte de maior energia.
5. Duração final 20,10 s = 43 batidas (o mais perto de 20 s na grade de batidas).
6. Sem velocidade, zoom ou cor aplicados no XML; sugestões no checklist.
7. Originais intocados (somente leitura); trabalho em cópias/proxies 720p.
