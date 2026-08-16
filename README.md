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
- richiesta esplicita degli input realmente bloccanti con la formula `Mi serve X`;
- prosecuzione dei rami non bloccati, senza trasformare un draft in output launch-ready;
- source/evidence ledger canonici, ID stabili e controllo dei riferimenti orfani.
- `brand-database.yaml` come entry point unico della fonte di verità;
- ogni modulo come vista autonoma con contesto, coverage, prove, conclusioni e next action;
- gate separati per completezza sostanziale e readiness di attivazione.

## Come gestisce i dati mancanti

La Skill valuta il dato rispetto all'output richiesto. Un'informazione può essere facoltativa per l'onboarding e bloccante per una campagna live. Quando il blocco è reale, l'agente chiede il minimo necessario spiegando cosa non può completare:

```text
Mi serve il mercato e la lingua. Senza questo non posso validare prezzi, policy, keyword e landing.
```

Se il dato non è disponibile, la Skill propone un output ridotto, conserva il blocker e non lo presenta come equivalente a un deliverable pronto all'attivazione.

## Standard di completezza

La Skill non considera completo un file che contiene soltanto checklist, framework o pochi esempi. Ogni modulo deve superare sette controlli:

- coverage;
- evidence;
- depth;
- actionability;
- standalone usability;
- consistency;
- freshness.

Product intelligence, psicografia, Meta Ads e Google Ads hanno contratti di profondità dedicati. Un modulo può essere strategicamente completo ma ancora bloccato per il lancio: le due cose vengono dichiarate separatamente.

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

Durante la compilazione usare `--stage draft`; prima della revisione o attivazione usare rispettivamente `--stage review` e `--stage activation`.

Per validare soltanto il nucleo ADV/Google:

```bash
python3 loop-agentic-kb/scripts/validate_kb.py /percorso/output --mode nucleus
```

## Stato

La Skill è stata validata strutturalmente e sottoposta a forward test indipendente. Un output può essere pronto per l'ideazione senza essere pronto per l'attivazione live: i file generati espongono sempre i dati bloccanti.
