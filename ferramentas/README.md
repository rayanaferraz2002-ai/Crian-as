# Ferramentas de edição (reutilizáveis)

Projeto = pasta com `projeto.json` (config + planos + textos do relatório). Rodar:

```bash
TRAB=/caminho/trabalho BASE="/pasta/dos/originais/no/seu/computador" bash ferramentas/rodar_projeto.sh <pasta_projeto> [--recalcular]
```

Etapas: analisar_musica.py (librosa) → gerar_proxies.sh (720p girado + folhas de contato) → montar_plano.py (encaixe nas batidas + nitidez/movimento) → render_preview.py → gerar_xml.py (FCP7 xmeml) → validar_xml.py (checagens + OpenTimelineIO) → gerar_relatorio.py.
