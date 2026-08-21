---
name: loop-agentic-kb
description: "Genera, aggiorna e valida database di brand e-commerce profondi, evidence-first e agent-ready, con moduli autonomamente utilizzabili per onboarding, prodotti, competitor, personas, psicografia, recensioni/VOC, Brand Voice, Tone of Voice, lessico, Meta Ads, creative strategy, Google Ads, landing, mercati, measurement ed experiment memory. Usare quando Codex deve trasformare sito e materiali interni in un'unica fonte di verità riutilizzabile, creare analisi complete per singolo modulo, oppure orchestrare specialisti senza inventare dati."
---

# Loop Agentic KB

Costruire una KB operativa che separi identità stabile, decisioni di mercato, decisioni di campagna e memoria delle performance.

## Principi non negoziabili

- Separare `evidence`, `inference`, `hypothesis`, `missing` e `blocked`.
- Citare fonte, data e perimetro per fatti, prezzi, policy, claim e recensioni.
- Non inventare target reali, demographics, volumi, CPC, margini, stock, performance o approvazioni.
- Separare Brand Voice, Tone of Voice, lessico e Voice of Customer.
- Trattare personas e keyword non misurate come ipotesi.
- Non dichiarare `campaign-ready` senza prodotto/offerta, mercato, target, obiettivo, destinazione, proof ed economics minimi.
- Mantenere i moduli brand-neutral separati dai market pack e dai campaign brief.
- Conservare output validi esistenti; aggiornare solo moduli obsoleti o insufficienti.
- Trattare la KB come un database normalizzato: una sola autorità per ogni entità, nessuna verità concorrente.
- Rendere ogni file una vista materializzata autonoma: deve essere comprensibile e azionabile senza aprire altri file, pur referenziando gli ID canonici.
- Non dichiarare completo un modulo che contiene soltanto framework, checklist, pochi esempi o una selezione non dichiarata.

Leggere sempre [evidence-governance.md](references/evidence-governance.md). Leggere [module-contracts.md](references/module-contracts.md) prima di creare file e [agent-contracts.md](references/agent-contracts.md) prima di delegare.
Leggere [blocking-input-protocol.md](references/blocking-input-protocol.md) durante l'intake e prima di ogni readiness gate. Leggere [canonical-schema.md](references/canonical-schema.md) prima di assegnare ID o creare registri YAML.
Leggere sempre [standalone-completeness.md](references/standalone-completeness.md) prima della ricerca e durante il QA. Leggere [customer-product-intelligence.md](references/customer-product-intelligence.md) per Product Message Map, prodotti, personas, psicografia, pain point e VOC.

## Intake

Raccogliere ciò che esiste senza richiedere di nuovo informazioni già presenti:

- brand e URL;
- obiettivo della KB e agenti downstream;
- mercato e lingua, se specifici;
- materiali interni, catalogo e asset;
- prodotto/offerta prioritari;
- dati economici, stock e performance disponibili;
- claim approvati e vincoli;
- esempi on-brand/off-brand;
- canali previsti.

Classificare ogni dato mancante rispetto all'output richiesto:

- `non_blocking`: riduce confidence o profondità, ma consente un output affidabile;
- `branch_blocking`: blocca solo un modulo o canale; completare i rami indipendenti;
- `run_blocking`: impedisce di produrre l'output richiesto senza inventare o scegliere arbitrariamente.

Per un input `branch_blocking` o `run_blocking`, applicare il protocollo obbligatorio:

1. non inventare placeholder semantici come se fossero decisioni;
2. chiedere all'utente il dato prima di superare il gate;
3. iniziare la richiesta con la frase esatta **"Mi serve X"**, sostituendo X con il dato concreto; `brief`, `dati`, `informazioni`, `dettagli`, `materiali` e `input` da soli non sono X validi;
4. spiegare in una frase cosa rimane bloccato e il formato minimo accettabile;
5. raggruppare solo blocker collegati, senza ripetere dati già disponibili o reperibili dalle fonti autorizzate.

Esempio: `Mi serve il mercato di destinazione. Senza paese e lingua non posso validare prezzi, policy, keyword e landing. È sufficiente indicare paese e lingua.`

Se l'utente non dispone del dato, proporre esplicitamente un output ridotto e marcarlo `blocked_missing_input`; non descriverlo come equivalente all'output richiesto. Vedere [blocking-input-protocol.md](references/blocking-input-protocol.md).

## Modalità

### Brand onboarding

Produrre moduli 01–10, fonti, gap e context pack.

### Agent-ready KB

Produrre moduli 00–21. I moduli 11–21 possono contenere campi mancanti espliciti: la completezza strutturale non equivale a campaign readiness.

Usare profondità `deep` come default per una KB completa. Usare `lean` o campionamento soltanto se l'utente lo chiede esplicitamente o se un limite tecnico viene dichiarato; in quel caso marcare i moduli interessati `module_quality.overall: conditional|fail`, mai completi.

### Channel pack

Aggiornare soltanto il brief del canale e le sue dipendenze. Per ADV/creative leggere [adv-creative-playbook.md](references/adv-creative-playbook.md). Per Google leggere [google-ads-playbook.md](references/google-ads-playbook.md).

### Market pack

Creare `19-market-packs/<country-code>.md`; non riscrivere la KB centrale con conclusioni locali.

## Database e viste autonome

Creare `brand-database.yaml` come indice canonico del database: versione, moduli, autorità, entity IDs, dipendenze, freshness e readiness. Non duplicare al suo interno tutti i record.

Ogni modulo deve incorporare un `standalone_context` o una sezione `Contesto autonomo` generata dalle autorità canoniche, contenente almeno:

- brand, scope, mercato/lingua e data;
- decisioni supportate e usi consentiti/vietati;
- sintesi di posizionamento, portfolio e audience rilevanti per il modulo;
- definizione degli ID referenziati;
- prove essenziali con fonte/data;
- limiti, blocker e freshness.

Il contesto incorporato è una vista derivata: aggiornarlo rigenerando il modulo, non modificandolo come fonte indipendente.

## Orchestrazione multi-agent

Leggere [orchestration.md](references/orchestration.md) quando sono disponibili sub-agent o il task richiede una KB completa.

1. Eseguire localmente intake, manifest e registro fonti.
2. Costruire prima la KB foundation: brand, portafoglio e source registry.
3. Avviare in parallelo soltanto task con input stabili e output distinti.
4. Non delegare la lettura delle istruzioni della Skill.
5. Assegnare a ogni agente un file o gruppo di file senza overlap.
6. Richiedere output atomici con schema, fonti, confidence, gap e handoff.
7. Integrare centralmente contraddizioni, claim e readiness.
8. Eseguire validazione deterministica e quality gate semantico.

DAG consigliato:

```text
intake + sources
  └─ foundation KB + portfolio
       ├─ competitors
       ├─ reviews/VOC
       └─ brand corpus
            ├─ personas + psychographics + pain points
            ├─ Brand Voice + Tone + lexicon
            └─ product/offer + claims/proof
                 ├─ funnel + creative + Meta brief
                 ├─ Google Ads + landing map
                 └─ assets + market packs
                      └─ measurement + experiment memory + synthesis
```

## Output contract

Usare questa struttura; vedere dettagli in [module-contracts.md](references/module-contracts.md):

```text
00-agent-manifest.md
01-knowledge-base.md
02-product-message-map.md
03-competitors.md
04-personas.md
05-psychographics.md
06-pain-points.md
07-reviews-voc.md
08-brand-voice.md
09-tone-of-voice.md
10-lexicon.md
11-product-offer-registry.yaml
12-claims-proof-library.yaml
13-funnel-awareness-matrix.yaml
14-creative-strategy-library.yaml
15-meta-ads-brief.yaml
16-google-ads-playbook.md
17-landing-page-map.yaml
18-asset-library.yaml
19-market-packs/
20-measurement-framework.yaml
21-experiment-memory.yaml
sources.yaml
evidence-ledger.yaml
assumptions-and-gaps.yaml
context-pack.yaml
brand-database.yaml
strategic-summary.md
review-checklist.yaml
qa-report.yaml
```

Questi nomi sono canonici. Non produrre alias legacy come `01a`, `07a`, `07b` o numerazioni alternative. I Markdown devono usare nel titolo lo stesso numero del filename. `brand-database.yaml` è l'indice; `sources.yaml`, `evidence-ledger.yaml`, `11-product-offer-registry.yaml`, `12-claims-proof-library.yaml` e `18-asset-library.yaml` sono autorità normalizzate. Gli altri moduli sono viste autonome derivate e referenziano gli ID canonici.

## Completezza sostanziale

Separare sempre:

- `module_completeness`: il file copre integralmente il proprio scopo;
- `standalone_ready`: il file può essere usato da solo;
- readiness di attivazione/pubblicazione.

Un modulo può essere completo e standalone per strategia, ma avere `activation_ready: blocked`. Non può essere `module_completeness: pass` se mancano sezioni, copertura, fonti o ragionamento necessari alla sua funzione. Applicare tutti i gate in [standalone-completeness.md](references/standalone-completeness.md).

## Moduli commerciali strutturati

Leggere [product-offer-claims.md](references/product-offer-claims.md) per compilare 11 e 12.

- Il registry prodotto descrive fatti e ruolo commerciale; non elegge hero sulla sola prominenza visiva.
- Il claim ledger contiene formulazione massima, fonte, perimetro, stato, owner e scadenza.
- `evidence` non significa `approved_for_ads`.
- Prezzo e disponibilità devono avere mercato, valuta e data.

## ADV e creative

Leggere [adv-creative-playbook.md](references/adv-creative-playbook.md).

- Collegare sempre `product × persona × awareness × objection × proof × CTA`.
- Separare direct response da awareness/engagement.
- Marcare gli angoli come `supported`, `hypothesis` o `blocked`.
- Non generare testimonianze, urgenza o scene clienti come fatti.
- Un creative brief può essere pronto per ideazione ma non per pubblicazione.

## Google Ads

Leggere [google-ads-playbook.md](references/google-ads-playbook.md).

- Classificare intenti brand, product, category, problem/job, gifting, designer/collab e competitor.
- Trattare keyword, negative e query mapping come ipotesi finché non validate con Search Console, Keyword Planner o search terms.
- Non inventare volumi, CPC, ROAS o ranking.
- Verificare landing, feed, GTIN/MPN, stock, shipping e policy prima di dichiarare Shopping/PMax ready.

## Measurement e memoria

Leggere [measurement-governance.md](references/measurement-governance.md).

- Definire KPI per obiettivo e fonte dati.
- Registrare test con ipotesi, contesto, variante, periodo, risultato e limiti.
- Non chiamare “learning” una variazione senza campione o contesto sufficiente.
- Non trasferire automaticamente un risultato tra mercati, prodotti o placement.

## Script

Per creare una nuova cartella KB:

```bash
python3 scripts/init_kb.py --brand "Brand" --output /absolute/path
```

Per validare struttura e stati:

```bash
python3 scripts/validate_kb.py /absolute/path --mode full
```

Usare `--mode nucleus` per un handoff ADV/Google deliberatamente ridotto. Gli script verificano struttura, non correttezza strategica.

## Readiness

Assegnare separatamente e con i soli valori `pass|conditional|blocked|not_applicable`:

- `framework_ready`: struttura e registri canonici validi;
- `onboarding_ready`: identità, portafoglio, competitor, cliente, voce e fonti sufficienti per onboarding;
- `strategy_ready`: personas, pain, funnel e ipotesi collegati alle prove;
- `activation_ready`: prodotto, mercato, canale, landing, asset ed economics sufficienti per costruire una campagna;
- `publish_ready`: claim approvati, stock/prezzo ricontrollati, asset autorizzati, tracking e QA completati.

Ogni stato deve includere `status`, `blocking_input_ids`, `conditions` e `last_checked_at`. Non comprimere gli stati in un unico sì/no e non usare `partial`, `ready-with-conditions` o booleani come sinonimi.

## Quality gate finale

- Ogni file dichiara scopo, stato, fonti, inferenze, gap e handoff.
- Nessun claim operativo manca di fonte e perimetro.
- Nessun dato mutevole manca di data.
- Personas, keyword e psicografia non sono presentate come dati osservati quando non lo sono.
- Brand Voice e VOC sono separate.
- Product registry, claim ledger e landing mapping usano ID coerenti.
- I brief di canale espongono input bloccanti.
- Ogni input bloccante ha un `input_id`, un output impattato e una richiesta utente nel formato `Mi serve X`.
- Nessun ID referenziato è orfano e ogni file dichiara `schema_version`.
- Contraddizioni tra fonti sono conservate e risolte esplicitamente.
- `validate_kb.py` termina senza errori strutturali.
- Un revisore può usare la KB senza ricostruire il contesto dalla chat.
- Ogni modulo supera il test in isolamento: il reviewer riceve soltanto quel file e riesce a comprendere brand, evidenze, analisi, decisioni, limiti e next action.
- `qa-report.yaml` contiene un assessment per ogni file su coverage, evidence, depth, actionability, standalone usability, consistency e freshness.
