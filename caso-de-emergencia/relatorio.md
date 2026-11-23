# Relatório — "Caso de emergência"

## 1. Como entendi o direcional (resumo)
1. A referência só ensina **ritmo de corte e estrutura narrativa** (gancho → caso → explicação → fecho); o visual não é copiado.
2. A **cena 1 abre com tensão**: preto e branco + efeito, e a tensão cresce até a virada.
3. A **virada** para o caso cai num **tempo forte** da música, junto com o começo da fala.
4. Depois da abertura, o vídeo **volta à cor** (o roteiro não diz o contrário).
5. Todo corte cai na **batida mais próxima** sem cortar palavra.
6. O clímax da música fica nos momentos de maior impacto.
7. Se houver conflito: roteiro > direcional > música > referência. Cada divergência está registrada na seção 9.

## 2. Material recebido e como interpretei
A pasta do Drive não tinha subpastas. Tudo estava em `05. CASO DE EMERGÊNCIA/`. A referência e o clipe da cena 4 chegaram depois, a seu pedido.

| Arquivo | Tipo identificado | Uso |
|---|---|---|
| `CASO DE EMERGÊNCIA` (Google Doc → .docx) | roteiro | Passo 1 |
| `snapinsta-1795455482487.mp4` | vídeo de referência (Reels, 720×1280, 30 fps, 111,7 s) | Passo 2 |
| `Hit Me Back (feat. Phury) (Instrumental).mp4` | música (só áudio, 198,7 s) | Passo 3 |
| ~~`C0120.MP4`, `C0150.MP4`~~ | B-roll (atendimento, mãos) | **removidos da pasta por você na revisão 2** — a doutora não fala para a câmera |
| `C0216`, `C0221`, `C0222`, `C0225.MP4` | a doutora falando | cenas 1–4 (C0225 veio por link à parte, não está na pasta; mantido porque ela fala para a câmera) |
| — | **não há locução separada** | a "locução" é o áudio dos próprios clipes de fala |

Formato dos clipes: 4K **vertical** (3840×2160 com rotação de 90°), 23,976 fps, PCM 2 canais a 48 kHz.

## 3. Roteiro (Passo 1)
| Cena | Direção de imagem | Direção de edição | Duração prevista | Áudio / fala |
|---|---|---|---|---|
| 1 | Contar a história da emergência: o que o cliente falou e o que aconteceu | Texto na tela **"E AGORA DOUTORA?"** + efeito sonoro de telefone | não informada | "Meu paciente falou, Dra. é urgente…" → C0216 (abertura P&B) + início do C0221 |
| 2 | Responder olhando para a câmera | — | não informada | "Conte porque aconteceu o que aconteceu?" → C0221 |
| 3 | Responder olhando para a câmera | — | não informada | "Explique como prevenir o que aconteceu" → C0222 |
| 4 | Responder olhando para a câmera | — | não informada | "Manda esse vídeo pra alguém que já passou por algo parecido!" → C0225 |

Transcrição dos clipes (faster-whisper, revisada à mão), em `analise/transcricoes.json`.

## 4. Referência (Passo 2) — `analise/referencia.json`
- **Formato:** 111,7 s; 9:16 (720×1280); 30 fps.
- **Planos:** 16, com média de 7,0 s. A duração média muda ao longo do vídeo: 5,5 s no 1º terço, 7,3 s no 2º e 9,3 s no 3º. O ritmo é mais picado no meio, com inserções de 1,4 a 3,9 s, e fica mais lento no fim.
- **Cortes por batida (86 BPM):** cerca de 10 batidas por plano de fala e 2 a 5 batidas por inserção.
- **Transições:** só cortes secos. Há legenda o tempo todo.
- **Estrutura:**
  - gancho em P&B, de 0 a 8,6 s ("minha secretária me ligou… é urgente");
  - virada para cor quando o caso começa ("Nós recebemos esse paciente");
  - caso de 8,6 a 26 s;
  - explicação de 27 a 85 s, com B-roll ilustrando;
  - conclusão de 85 a 111,7 s.

## 5. Música (Passo 3) — `analise/mapa_batidas.json` / `.csv`
- **Andamento:** 86,13 BPM (batida a cada 0,697 s), 256 batidas, compasso 4/4. O tempo forte é a fase 3 da grade detectada.
- **Seções:**

| Trecho | Seção |
|---|---|
| 0–4,9 s | intro |
| 4,9–24 s | groove leve |
| 24–68 s | subida |
| 68–90 s | clímax 1 |
| 90,4–112,5 s | **breakdown** (percussão cai para cerca de 1/3) |
| 112,5–180 s | **drop / clímax 2** |
| 180–198,7 s | final |

- **Melhor tempo forte para a virada: 112,501 s.** É o drop depois do breakdown. A percussão triplica (detectado automaticamente: ganho ×3,0).
- **Trecho usado:** a música entra em 104,931 s, 11 batidas antes do drop. É o menor número de batidas em que cabem o título/telefone e toda a fala da abertura. A abertura fica no fim do breakdown, onde a tensão sobe naturalmente, e a virada cai exatamente no drop.
- **Clímax:** o close do "implante" (00:00:28:06) cai na parte de alta energia (133,2 s da faixa). O vídeo termina em 149,1 s da faixa, ainda no clímax 2, com fade-out.

## 6. Cena → clipe escolhido (revisão 2 — só a doutora falando)
Os tempos de origem estão em segundos. TL = linha do tempo. Todos os cortes caem em batida.

| Plano | Cena | Arquivo | Origem in→out | TL | Enquadramento | Motivo |
|---|---|---|---|---|---|---|
| V01 | 1 | `abertura_tensao.mov` (de `C0216.MP4` 1,25→8,80) | 0→181 q | 00:00:00:00–00:00:07:13 | P&B + efeito | A urgência contada por ela ("consulta mais rápido possível… coroa está mole") é o "telefonema" do roteiro, como o gancho P&B da referência. Antes da fala ela fica em silêncio, olhando de lado: é aí que entram o título e o telefone. |
| V02 | 1 | `C0221.MP4` | 1,38→4,84 | 07:13–11:00 | aberto | **Virada no drop**: a cor entra junto com "Quando eu fui atendê-la" (início do caso). |
| V03 | 2 | `C0221.MP4` | 4,84→13,14 | 11:00–19:07 | fechado (1,2×) | Cena 2: "Por que isso aconteceu? Porque ela tem bruxismo…". |
| V04 | 2 | `C0221.MP4` | 13,14→17,27 | 19:07–23:10 | close (1,35×) | Ocupa o lugar do B-roll removido, com o mesmo pulso de inserção da referência, sem sair da doutora ("a mordida apertou tanto"). |
| V05 | 2 | `C0221.MP4` | 17,27→22,11 | 23:10–28:06 | aberto | Respiro: "quebrasse uma parte da raiz…". |
| V06 | 2 | `C0221.MP4` | 22,11→24,86 | 28:06–31:00 | close | Momento de impacto: "Ela precisou fazer o implante". |
| V07 | 3 | `C0222.MP4` | 1,00→4,46 | 31:00–34:11 | aberto | Pergunta da prevenção. |
| V08 | 3 | `C0222.MP4` | 4,46→9,97 | 34:11–39:23 | fechado | Resposta: placa de bruxismo / corrigir a mordida. |
| V09 | 4 | `C0225.MP4` | 1,58→5,71 | 39:23–44:02 | aberto | CTA olhando para a câmera, com respiro final e fade para preto. |

Áudio da fala (A1/A2): `C0216` vai de 2,21 a 8,80 s, sob a abertura, e o `C0221` é contínuo de 1,38 a 24,86 s. Os cortes de enquadramento são só de imagem, então a fala não sofre nenhum salto.

## 7. Efeito de abertura — escolha e porquê
- **P&B**, saturação 0.
- **Sem câmera lenta.** Como ela fala na abertura, a câmera lenta quebraria a sincronia labial (conferida aqui: 0 ms de defasagem). Isso diverge da sugestão do direcional; veja a seção 9.
- **Zoom de 1,00× para 1,30× com aceleração (ease-in)**, ancorado no rosto. Começa quase parado e vai "apertando" até o drop. É o principal motor da tensão crescente.
- **Contraste de 1,25 para 1,55** e **vinheta de 0,55 para 0,95 rad**, ambos crescentes. As bordas escurecem e o foco se concentra no rosto.
- **Grão constante** (12): textura de filme.
- **Música:** cheia durante o telefone e o título, depois abaixa (−14 dB) quando ela começa a falar.
- **Descartado:** flicker e tremor de câmera. Brigariam com o tom profissional.

Arquivo: `abertura_tensao.mov`, 1080×1920, 23,976 fps, 181 quadros (7,55 s), **ProRes 422 LT** (82 MB), só imagem. Para HQ, rode `python3 scripts/05_render_abertura.py --perfil 3`.

## 8. Descartados
| Trecho | Motivo |
|---|---|
| C0120.MP4 e C0150.MP4 | removidos da pasta por você (a doutora não fala para a câmera) |
| C0216 0–1,25 s | contagem da equipe ("2, 1, foi") |
| C0221 0–1,3 s | ruído/fala antes da tomada |
| C0221 25,4–27,0 s | "O que é melhor?" (bastidor, fora do roteiro) |
| C0222 0–1,0 s | fala da equipe antes da tomada (inclui um "E" que não entra; a legenda começa em "O que pode…") |
| C0222 9,95–12,0 s | "Não, não gostaria" (bastidor) |
| C0225 0–1,6 s e 5,7–7,0 s | "Fui." e "Tchau." (fora do roteiro) |

## 9. Premissas e divergências
1. **Formato:** 1080×1920 a 23,976 fps (decisão sua). A referência é 720×1280 a 30 fps por compressão do Instagram. Mantive a mesma proporção 9:16, mas no fps nativo dos clipes, para não repetir quadros.
2. **Duração final: 44,1 s, contra 111,7 s da referência.** O roteiro não dá durações, e o material de fala útil soma cerca de 43 s. Não estiquei com material repetido.
3. **Cena 1 × direcional (revisão 2):** sem os planos de atendimento, a abertura P&B passou a ser a doutora contando a urgência, como no gancho P&B da referência. A virada cai no drop junto com o início da narrativa do caso ("Quando eu fui atendê-la"), não com o primeiro som de fala. A câmera lenta sugerida no direcional não foi usada, para não quebrar a sincronia labial.
   - **Atenção:** no `C0216` ela olha um pouco para o lado, e não direto para a lente. Mantive porque ele continua na pasta. Se quiser tirá-lo também, a abertura teria que vir de outro trecho dela falando (C0221/C0222), repetindo fala.
4. **SFX de telefone:** não existe no Drive. Deixei a trilha A5 vazia e um marcador em 00:00:00:00 (decisão sua).
5. **Cor depois da abertura:** o roteiro não diz nada em contrário, então tudo volta à cor a partir de 00:00:08:06.
6. **B-roll:** removido (revisão 2). A variação de plano vem só dos zooms digitais. **Transições:** a referência só tem cortes secos, e os mantive. A única "fusão" é o mergulho para preto de 12 quadros no fim. O pedido de "fusões simples" foi atendido só onde não briga com a referência.
7. **Legendas:** a referência tem legenda o tempo todo, então gerei `legendas.srt` com toda a fala. O texto segue a fala literal, com pontuação minha. A transcrição automática foi conferida trecho a trecho.
8. **Ducking:** a música sob a fala fica em −16,5 dB (≈ 13 LU abaixo da voz) e a 0 dB na abertura. Medições: música −13,9 LUFS, fala ≈ −17,5 LUFS; prévia final ≈ −15 LUFS integrado.
9. **Zoom digital (1,2× e 1,35×):** feito sobre o 4K original, sem perda em 1080p. Serve para variar planos, já que só há um ângulo de câmera.
10. **Rotação:** o XML assume que o Premiere lê a rotação de 90° dos MP4 (as versões atuais leem). Se algum clipe aparecer deitado, veja o checklist.
11. **Keyframes de volume no XML:** foram gravados no tempo da mídia (padrão FCP7). Se o Premiere não os trouxer, os pontos estão no checklist.

## 10. Verificações feitas
- `sequencia.xml` passou no validador. Ele confere:
  - XML bem-formado e DOCTYPE xmeml;
  - in/out e durações coerentes, sem sobreposição;
  - aponta para os originais;
  - trilha V1 idêntica ao `plano.json`.
- O XML também foi **lido de forma independente pelo OpenTimelineIO** (adaptador FCP7): 6 trilhas, 9 clipes, 1058 quadros.
- `preview.mp4` (revisão 2): 1058 quadros (44,1 s), 720×1280, 23,976 fps, 7,5 MB. Virada conferida (q180 P&B → q181 cor). Sincronia labial da abertura medida: 0 ms.
- `abertura_tensao.mov`: 181 quadros contados com ffprobe.
- `gerar_proxies.sh` testado em 1 clipe (`C0216.MP4`):
  - tamanho: **201,5 MB → 25,0 MB**;
  - duração 11,011 s → 11,011 s;
  - 23,976 fps, 2 canais;
  - vertical 720×1280;
  - a 2ª execução pulou o arquivo já gerado.
