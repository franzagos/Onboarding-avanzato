# Loop Agentic KB

Skill per generare knowledge base e-commerce riutilizzabili da agenti di onboarding, ADV, creative strategy e Google Ads.

## Download

Scarica il pacchetto pronto all'installazione:

- [`loop-agentic-kb.skill`](dist/loop-agentic-kb.skill)

Il sorgente completo è disponibile nella cartella [`loop-agentic-kb/`](loop-agentic-kb/).

## Cosa genera

- brand e product knowledge base;
- product message map;
- competitor, personas, psicografia e pain point;
- recensioni e Voice of Customer;
- Brand Voice, Tone of Voice e lessico;
- product/offer registry e claims ledger;
- funnel e awareness matrix;
- creative strategy e brief Meta Ads;
- playbook Google Search, Shopping e PMax;
- landing page map e asset library;
- market pack, measurement framework ed experiment memory.

## Principi

- separazione fra evidenze, inferenze, ipotesi e dati mancanti;
- Brand Voice distinta dalla Voice of Customer;
- nessun target, claim, CPC, volume o performance inventati;
- readiness distinta in brand, product, channel, campaign e publish;
- orchestrazione multi-agent con ownership dei file e handoff strutturati.

## Utilizzo

Esempio:

```text
Usa $loop-agentic-kb per creare una knowledge base completa e agent-ready per https://example.com.
```

Per generare la struttura vuota:

```bash
python3 loop-agentic-kb/scripts/init_kb.py \
  --brand "Nome Brand" \
  --output /percorso/output
```

Per validare una KB completa:

```bash
python3 loop-agentic-kb/scripts/validate_kb.py /percorso/output --mode full
```

Per validare soltanto il nucleo ADV/Google:

```bash
python3 loop-agentic-kb/scripts/validate_kb.py /percorso/output --mode nucleus
```

## Stato

La Skill è stata validata strutturalmente e sottoposta a forward test indipendente. Un output può essere pronto per l'ideazione senza essere pronto per l'attivazione live: i file generati espongono sempre i dati bloccanti.
