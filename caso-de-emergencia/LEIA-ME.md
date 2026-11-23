# LEIA-ME — Caso de emergência (Premiere)

## O que tem aqui
| Arquivo | Para quê |
|---|---|
| `sequencia.xml` | Sequência para importar no Premiere (1080×1920, 23,976 fps) |
| `abertura_tensao.mov` | Cena 1 já pronta (P&B + efeito) — usada pelo XML |
| `preview.mp4` | Prévia leve da edição |
| `checklist_premiere.md` | O que aplicar à mão (texto, SFX, conferências) com timecode |
| `legendas.srt` / `texto_na_tela.srt` | Legendas da fala / título "E AGORA DOUTORA?" |
| `gerar_proxies.sh` | Cria proxies leves de todos os clipes |
| `relatorio.md` | Decisões, escolhas de clipe, premissas |
| `plano.json` / `decisoes.json` / `scripts/` | Base da edição — para pedir trocas sem refazer tudo |

## 1. Instalar o ffmpeg (macOS 12)
Opção A — Homebrew (se já usa):
```bash
brew install ffmpeg
```
Opção B — sem Homebrew (mais rápido no macOS 12): baixe **ffmpeg** e **ffprobe** em <https://evermeet.cx/ffmpeg/> (Mac Intel) ou <https://www.osxexperts.net> (Mac M1/M2), descompacte e mova:
```bash
sudo mkdir -p /usr/local/bin && sudo mv ~/Downloads/ffmpeg ~/Downloads/ffprobe /usr/local/bin/
```
```bash
xattr -d com.apple.quarantine /usr/local/bin/ffmpeg /usr/local/bin/ffprobe
```
Teste:
```bash
ffmpeg -version
```

## 2. Gerar os proxies
1. Coloque `gerar_proxies.sh` em qualquer lugar (ex.: Downloads).
2. No Terminal, rode (troque pelo caminho da sua pasta de clipes; dá para arrastar a pasta para o Terminal):
```bash
bash ~/Downloads/gerar_proxies.sh "/Users/SEU_USUARIO/Videos/05. CASO DE EMERGÊNCIA"
```
3. Os proxies vão para `…/05. CASO DE EMERGÊNCIA/proxies/` (`C0216.MP4` → `proxies/C0216.mov`). Os originais não são tocados. Se parar no meio, rode de novo: ele pula o que já fez.

## 3. Importar o XML
1. Copie `abertura_tensao.mov` para a **mesma pasta dos originais** (junto da música).
2. Premiere: **Arquivo > Importar** → `sequencia.xml`.
3. Abra a sequência **CASO DE EMERGENCIA**.

(Opcional) Para o XML já abrir com os caminhos certos no seu Mac:
```bash
python3 scripts/07_gerar_xml.py --media-dir "/Users/SEU_USUARIO/Videos/05. CASO DE EMERGÊNCIA"
```

## 4. Vincular a mídia aos ORIGINAIS
1. Se aparecer "Vincular mídia" (ou clipes offline em vermelho): selecione tudo no Projeto > clique direito > **Vincular mídia…**
2. Clique em **Localizar**, vá até a pasta dos **originais** (NÃO a pasta `proxies`) e escolha o primeiro arquivo. Marque *Corresponder ao nome do arquivo* e *Vincular os outros automaticamente*.
3. Confira: clipes 4K vêm com Escala 50% e de pé (se algum vier deitado, veja o checklist, item 0).

## 5. Anexar os proxies
1. No painel Projeto, selecione os clipes (C0216, C0221, C0222, C0225).
2. Clique direito > **Proxy > Anexar proxies…**
3. Aponte cada um para o arquivo de mesmo nome em `proxies/` (pelo nome).
   - Não anexe proxy à música nem ao `abertura_tensao.mov` (já são leves).

## 6. Botão de proxy
- **Ligar para editar:** no Monitor do programa, clique no **+** (Editor de botões) e arraste o botão **Alternar proxies** para a barra. Clique nele: azul = editando com proxies (leve).
- **DESLIGAR antes de exportar:** clique de novo (fica cinza). Assim o vídeo final sai dos originais 4K, em qualidade total.
  - A exportação usa os originais quando o botão está desligado. Confira em *Exportar > Configurações*: 1080×1920, 23,976 fps.

## 7. Pedir ajustes
Edite `decisoes.json` (trocar trecho, enquadramento, níveis) ou peça a troca. Para refazer prévia + XML + checklist:
```bash
MIDIA="/caminho/dos/originais" bash scripts/rodar_tudo.sh
```
(precisa de `pip install -r scripts/requirements.txt`; `--abertura` re-renderiza a cena 1).

## 8. Só os proxies, sem edição (`proxies_premiere.xml`)
Os 4 proxies prontos estão em `proxies/` (ProRes Proxy, 720×1280, 23,976 fps, áudio PCM 2 canais, mesma duração dos originais).
1. Deixe a pasta `proxies/` junto do `proxies_premiere.xml` (ou em qualquer lugar).
2. Premiere: **Arquivo > Importar** → `proxies_premiere.xml`. Entra só uma pasta **PROXIES - CASO DE EMERGENCIA** com os 4 clipes, sem sequência.
3. Se ficarem offline: clique direito > **Vincular mídia…** > **Localizar** → pasta `proxies/` → escolha o 1º arquivo (os outros vinculam sozinhos pelo nome).
Para gravar o caminho certo do seu Mac direto no XML:
```bash
python3 scripts/10_gerar_xml_proxies.py --media-dir "/Users/SEU_USUARIO/caminho/proxies"
```
