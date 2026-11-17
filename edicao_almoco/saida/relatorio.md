# Relatório de edição — Terral — almoço executivo (ambiente + pratos)

## Material recebido e interpretação

Estrutura do Drive diferente da esperada (arquivos soltos). Interpretação:

| Arquivo | Interpretado como | Observação |
|---|---|---|
| Quanta Saudade (Feels Like Heaven) (Instrumental) (1).mp4 | musica/ | Só áudio, 227,9 s |
| cantinaclasse_pindown.io_1794929150.mp4 | referencia/ | Vídeo do Pinterest, 720×1280, 60 fps, 10,7 s |
| MVI_9152.MP4 | clipes/ ambiente | Mesa cheia; garçom passa (4–6 s) |
| MVI_9153.MP4 | clipes/ ambiente | Garçom atendendo (0–2,5 s); clientes comendo (4–7 s) |
| MVI_9161.MP4 | clipes/ ambiente | Panorâmica: adega → homem → casal à mesa (5–7,7 s); borrado em ~4 s |
| MVI_9162.MP4 | clipes/ ambiente | Plantas no teto (sem pessoas) |
| MVI_9209.MP4 | clipes/ ambiente | Salão vazio com adega; gravado invertido em relação aos outros (gira +90°) |
| MVI_9068.MP4 | clipes/ prato | Prato executivo; feijão servido (1–4 s); guardanapo (5–9 s) |
| MVI_9069.MP4 | clipes/ prato | 35 s: vinagrete, farofa, garfo, corte do bife |
| MVI_9072.MP4 | clipes/ prato | Salada com frango de cima |
| MVI_9074.MP4 | clipes/ prato | Garfo pegando salada |
| MVI_9081.MP4 | clipes/ prato | Boca comendo salada (close) |
| MVI_9086.MP4 | clipes/ prato | Corte do bife acebolado com fritas |
| MVI_9087.MP4 | clipes/ prato | Bife acebolado com fritas de cima |
| MVI_9088.MP4 | clipes/ prato | Mão pegando batata frita |
| — | roteiro/ | Ausente; usado o roteiro da conversa |
| — | locucao/ | Ausente |

Clipes 1920×1080 23,976 fps gravados na vertical: −90° em todos, exceto MVI_9209 (+90°).

## Passo 1 — Roteiro

| Cena | Direção de imagem | Direção de edição | Duração | Áudio/fala |
|---|---|---|---|---|
| Ciclo ×6 | 1 take de ambiente (movimento da casa no almoço executivo) + 2 takes de pratos | Alternância fixa A-P-P; cortes secos na batida | Até 30 s (sua decisão) → 29,6 s | Só música |

## Passo 2 — Referência

- 10,7 s, 9:16 (720×1280), 60 fps, 8 planos de ambiente/pessoas, só cortes secos, tons quentes.
- Cortes em 2,10 / 3,57 / 4,57 / 5,72 / 7,15 / 8,12 / 9,70 s → planos de 0,97–2,10 s (média 1,34 s).
- Música da referência ~152 BPM: corte a cada ~3 batidas; ritmo constante, primeiro plano mais longo.

## Passo 3 — Música

- BPM **89.1** (batida 0.6734 s), 315 batidas.
- Seções de energia (s): 9.0–30.8 alta; 30.8–36.3 media; 36.3–41.7 alta; 41.7–47.2 media; 47.2–63.6 alta; 63.6–66.3 media; 66.3–74.5 alta; 74.5–77.2 media; 77.2–85.4 alta; 85.4–88.1 media; 88.1–96.3 alta; 96.3–101.8 media; 101.8–107.2 alta; 107.2–112.7 media; 112.7–139.9 alta; 139.9–145.4 media; 145.4–150.9 alta; 150.9–156.3 media; 156.3–159.0 alta; 159.0–180.9 media; 180.9–183.6 alta; 183.6–189.0 media; 189.0–216.3 alta; 216.3–227.9 media
- Trecho usado: **9.033 → 39.021 s**. Drop em 9.033 s = 00:00:00:00 na timeline.
- Mapa de batidas: `analise/musica.json`.

## Passo 4/5 — Plano → clipe escolhido

| # | Cena | Arquivo original | Entrada → saída (fonte) | Timeline | Batidas | Motivo | Nitidez/mov./lum. |
|---|---|---|---|---|---|---|---|
| 01 | Ambiente | MVI_9209.MP4 | 1.00 → 3.04 s | 00:00:00:00 → 00:00:02:01 | 3 | Salão do Terral com a adega iluminada: abre apresentando a casa. | 617.1/3.89/108.0 |
| 02 | Prato | MVI_9068.MP4 | 1.50 → 2.88 s | 00:00:02:01 → 00:00:03:10 | 2 | Prato executivo (bife, fritas, arroz, salada) com o feijão sendo servido. | 131.1/11.59/132.8 |
| 03 | Prato | MVI_9072.MP4 | 0.30 → 1.63 s | 00:00:03:10 → 00:00:04:18 | 2 | Salada com frango vista de cima, muito nítida. | 789.2/6.08/112.4 |
| 04 | Ambiente | MVI_9152.MP4 | 0.50 → 2.59 s | 00:00:04:18 → 00:00:06:20 | 3 | Mesa cheia de clientes almoçando e conversando. | 515.1/8.22/145.8 |
| 05 | Prato | MVI_9069.MP4 | 0.50 → 1.88 s | 00:00:06:20 → 00:00:08:05 | 2 | Vinagrete sendo colocado ao lado do bife. | 73.5/7.66/101.7 |
| 06 | Prato | MVI_9086.MP4 | 1.00 → 2.34 s | 00:00:08:05 → 00:00:09:13 | 2 | Faca e garfo cortando o bife acebolado com fritas. | 151.1/4.93/91.2 |
| 07 | Ambiente | MVI_9153.MP4 | 0.00 → 2.04 s | 00:00:09:13 → 00:00:11:14 | 3 | Garçom atendendo uma mesa: movimento do serviço. | 494.0/7.98/123.3 |
| 08 | Prato | MVI_9074.MP4 | 1.50 → 2.88 s | 00:00:11:14 → 00:00:12:23 | 2 | Garfo pegando a salada. | 165.9/10.59/154.2 |
| 09 | Prato | MVI_9081.MP4 | 0.90 → 2.25 s | 00:00:12:23 → 00:00:14:07 | 2 | Corte em sequência: a salada chega à boca. | 20.4/7.52/150.5 |
| 10 | Ambiente | MVI_9161.MP4 | 5.60 → 7.63 s | 00:00:14:07 → 00:00:16:08 | 3 | Casal almoçando à mesa. | 379.6/8.08/135.2 |
| 11 | Prato | MVI_9069.MP4 | 11.80 → 13.18 s | 00:00:16:08 → 00:00:17:17 | 2 | Farofa sendo servida sobre o arroz. | 282.7/8.91/100.7 |
| 12 | Prato | MVI_9088.MP4 | 0.30 → 1.67 s | 00:00:17:17 → 00:00:19:02 | 2 | Mão pegando batata frita do prato executivo. | 65.2/7.55/161.6 |
| 13 | Ambiente | MVI_9162.MP4 | 0.00 → 2.04 s | 00:00:19:02 → 00:00:21:03 | 3 | Plantas pendentes no teto de madeira: respiro de ambiente (sem pessoas, autorizado por você). | 205.3/10.65/95.3 |
| 14 | Prato | MVI_9069.MP4 | 28.80 → 30.16 s | 00:00:21:03 → 00:00:22:11 | 2 | Garfo e faca cortando o bife, com vinagrete e farofa. | 255.1/5.02/120.5 |
| 15 | Prato | MVI_9074.MP4 | 4.00 → 5.38 s | 00:00:22:11 → 00:00:23:20 | 2 | Garfo levando a salada (trecho diferente do plano 08). | 163.3/8.57/159.1 |
| 16 | Ambiente | MVI_9152.MP4 | 4.30 → 6.34 s | 00:00:23:20 → 00:00:25:21 | 3 | Garçom passando entre as mesas cheias (trecho diferente do plano 04). | 526.7/10.38/134.2 |
| 17 | Prato | MVI_9072.MP4 | 2.00 → 3.38 s | 00:00:25:21 → 00:00:27:06 | 2 | Salada com frango de cima (trecho diferente do plano 03): contraste de cor antes do bife final. | 960.9/9.11/120.6 |
| 18 | Prato | MVI_9087.MP4 | 1.90 → 4.63 s | 00:00:27:06 → 00:00:29:23 | 4 | Bife acebolado com fritas de cima, o plano mais nítido: fecha com fade. | 337.1/8.08/120.4 |

Duração 29.988 s (719 quadros), 18 planos, média 1.67 s (mín 1.33, máx 2.71).
6 ciclos: ambiente 3 batidas (2,02 s) + 2 pratos de 2 batidas (1,35 s, igual à média da referência). Último prato 4 batidas com fade.
Transições: corte seco na batida; 18: Fade to Black 12 quadros. Fade-out da música 1.5 s.

## Descartados

| Trecho | Motivo |
|---|---|
| MVI_9161 0–5,5 s | Panorâmica rápida (movimento alto) e borrada em ~4 s; usado só o casal. |
| MVI_9068 5–7 s | Mão com guardanapo cobrindo o prato. |
| MVI_9069 1,5–10 s / 15–25 s | Repetitivo; ficaram os três momentos mais claros (vinagrete, farofa, corte). |
| MVI_9081 2,5 s → fim | Boca fechada, sem ação. |
| MVI_9153 3,5–7 s | Bom, mas o 9153 já entra com o garçom; evitado repetir. |
| MVI_9068 7–9,7 s | Testado no plano 17: potinho de feijão em quadro, repetia o plano 02. |

## Premissas

1. Duração até 30 s e uso de ambientes sem pessoas (9162, 9209): decisões suas.
2. Formato: 9:16 em 1080×1920, 23,976 fps (fps dos clipes). A referência é 720×1280, 60 fps (download do Pinterest); converter para 60 fps não traz ganho e faria a imagem trepidar. Para seguir à risca, troque fps/resolução no projeto.json.
3. Trecho da música 9,033 → 38,66 s: começa no primeiro tempo forte da parte com energia alta (a introdução de 0–9 s fica de fora). Há uma queda de energia em 30,8–36,3 s da faixa (21,8–27,2 s da timeline), suavizada pelo plano de respiro (plantas) e pelo fim.
4. Repetições (18 planos, 13 clipes): 9152, 9069 (3 momentos), 9072 e 9074 aparecem mais de uma vez, sempre em trechos diferentes e nunca seguidos.
5. Sem velocidade, zoom, texto ou cor aplicados. Sugestões no checklist.
6. Originais intocados (somente leitura); trabalho em cópias/proxies 720p.
