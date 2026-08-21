---
name: loop-agentic-kb
description: "Genera, aggiorna, valida ed esporta knowledge base e-commerce evidence-first e agent-ready. Usare per onboarding brand, product intelligence, competitor, personas, psicografia, VOC, Brand Voice, Meta Ads, Google Ads, landing, measurement; per consegnare ogni modulo come file Markdown; oppure per unire i moduli completati in un dossier finale o ZIP senza inventare dati."
---

# Loop Agentic KB

Costruire una fonte di verità canonica e generare viste Markdown leggibili solo quando servono.

## Regole essenziali

- Separare `evidence`, `inference`, `hypothesis`, `missing` e `blocked`.
- Citare fonte, data e perimetro per fatti, prezzi, policy, claim e recensioni.
- Non inventare target reali, demographics, volumi, CPC, margini, stock, performance, diritti o approvazioni.
- Separare Brand Voice, Tone of Voice, lessico e Voice of Customer.
- Trattare personas, psicografia, keyword e angoli non misurati come ipotesi verificabili.
- Non confondere completezza strategica con readiness di attivazione o pubblicazione.
- Usare un'autorità canonica per ogni entità; referenziare ID stabili nelle viste derivate.
- Aggiornare soltanto moduli obsoleti o dipendenti da dati cambiati.
- Scrivere i risultati nei file; restituire in chat un handoff breve e i link, non il report completo.

## Avvio

1. Raccogliere brand, URL/materiali, obiettivo, mercato/lingua, prodotti prioritari e canali.
2. Non richiedere informazioni già disponibili o reperibili dalle fonti autorizzate.
3. Scegliere il profilo minimo adeguato: `onboarding`, `meta`, `google`, `activation`, `full` o `custom`.
4. Creare la KB:

```bash
python3 scripts/init_kb.py \
  --brand "Nome Brand" \
  --profile onboarding \
  --output /absolute/path
```

Per un profilo custom, passare `--profile custom --modules 01 02 07 08`.

## Dati mancanti

Classificare ogni dato rispetto all'output richiesto:

- `non_blocking`: riduce confidence o profondità;
- `branch_blocking`: blocca soltanto un modulo o canale;
- `run_blocking`: impedisce l'output richiesto senza inventare o scegliere arbitrariamente.

Per un blocker reale, iniziare la richiesta con **“Mi serve X”**, spiegare cosa rimane bloccato e indicare il formato minimo accettabile. Proseguire sui rami indipendenti. Se il dato non esiste, produrre un output ridotto marcato `blocked_missing_input`.

Leggere [blocking-input-protocol.md](references/blocking-input-protocol.md) solo quando emerge un blocker o prima di superare un readiness gate con input mancanti.

## Produzione modulare

Usare i filename e le dipendenze in [module-contracts.md](references/module-contracts.md), leggendo soltanto la sezione relativa ai moduli richiesti. Mantenere:

- YAML canonici per registri e consumo agentico;
- Markdown canonici per i moduli narrativi;
- `brand-database.yaml` come indice delle autorità;
- `sources.yaml`, `evidence-ledger.yaml` e `assumptions-and-gaps.yaml` come registri trasversali;
- `exports/modules/` come viste di consegna, mai come fonte da modificare.

Prima di assegnare nuovi ID o modificare registri, leggere [canonical-schema.md](references/canonical-schema.md). Per conflitti tra fonti, claim sensibili o evidence ledger, leggere [evidence-governance.md](references/evidence-governance.md).

Caricare gli approfondimenti soltanto quando il modulo li richiede:

- product message, personas, psicografia, pain e VOC: [customer-product-intelligence.md](references/customer-product-intelligence.md);
- product registry e claim: [product-offer-claims.md](references/product-offer-claims.md);
- creative e Meta: [adv-creative-playbook.md](references/adv-creative-playbook.md);
- Google Ads e landing: [google-ads-playbook.md](references/google-ads-playbook.md);
- measurement ed esperimenti: [measurement-governance.md](references/measurement-governance.md).

## Orchestrazione

Per una KB completa o quando sono disponibili specialisti, leggere [orchestration.md](references/orchestration.md). Prima di delegare, leggere [agent-contracts.md](references/agent-contracts.md).

- Materializzare prima foundation, portfolio e fonti.
- Parallelizzare soltanto output distinti con input stabili.
- Assegnare write scope senza overlap.
- Passare path, versioni, ID e context pack mirati; non copiare l'intera KB nel prompt.
- Chiedere agli specialisti file atomici e un handoff breve.
- Integrare centralmente conflitti, claim, readiness e QA.
- Se non sono disponibili specialisti, eseguire lo stesso DAG in sequenza.

## Delivery contract

Al completamento di ogni modulo:

1. salvare o aggiornare la fonte canonica;
2. generare la vista Markdown;
3. validare il file;
4. restituire all'utente il link, lo stato, i blocker e la prossima dipendenza;
5. non incollare l'intero modulo nella chat.

Generare un singolo modulo:

```bash
python3 scripts/render_module.py /absolute/path --module 11
```

Generare tutti i moduli previsti dal manifest:

```bash
python3 scripts/render_module.py /absolute/path
```

Quando l'utente chiede di unire il lavoro, generare il dossier finale deduplicato:

```bash
python3 scripts/build_final_md.py /absolute/path
```

Quando chiede un pacchetto completo, generare anche lo ZIP:

```bash
python3 scripts/package_delivery.py /absolute/path
```

Il dossier finale deve includere un solo contesto globale, indice, moduli in ordine canonico e appendici di fonti/gap. Le viste singole devono invece conservare il proprio contesto autonomo.

## Readiness e QA

Usare soltanto `pass|conditional|blocked|not_applicable` per `framework_ready`, `onboarding_ready`, `strategy_ready`, `activation_ready` e `publish_ready`. Includere sempre blocker, condizioni e data di controllo.

Validare durante il lavoro in `draft`; usare `review` o `activation` prima della relativa consegna:

```bash
python3 scripts/validate_kb.py /absolute/path --stage draft
```

Prima del package finale leggere [standalone-completeness.md](references/standalone-completeness.md) ed eseguire il test in isolamento dei moduli consegnati. Un modulo può essere strategicamente completo e avere activation bloccata; non può risultare completo se è soltanto una checklist o un elenco di dati mancanti.

Concludere soltanto quando:

- i file richiesti esistono e non contengono placeholder incompatibili con lo stage;
- fatti, claim e dati mutevoli hanno prove, scope e freshness;
- non esistono ID orfani o verità concorrenti;
- ogni modulo richiesto ha il proprio Markdown in `exports/modules/`;
- il dossier finale, se richiesto, esiste in `deliverables/`;
- l'utente riceve link diretti ai file prodotti.
