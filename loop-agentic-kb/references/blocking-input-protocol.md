# Protocollo per input mancanti e blocchi

## Scopo

Chiedere dati all'utente solo quando la loro assenza rende inaffidabile l'output richiesto. Non trasformare ogni gap in una domanda e non nascondere un blocker dietro un template compilato a metà.

## Classificazione

| Classe | Effetto | Azione |
|---|---|---|
| `non_blocking` | riduce profondità o confidence | procedere, registrare il gap |
| `branch_blocking` | blocca un modulo/canale, non il resto | completare i rami indipendenti, poi chiedere l'input prima del ramo bloccato |
| `run_blocking` | impedisce l'output esplicitamente richiesto | fermarsi e chiedere subito |

La stessa informazione può cambiare classe in base all'obiettivo. Il margine è `non_blocking` per Brand Voice, `branch_blocking` per una strategia media esplorativa e `run_blocking` per un piano performance dichiarato pronto al lancio.

## Decisione

Per ogni dato mancante, chiedere in ordine:

1. È già presente nei file, nella conversazione o in una fonte autorizzata?
2. Può essere osservato senza chiedere una decisione o un'informazione proprietaria?
3. Se resta mancante, posso produrre l'output richiesto senza inventare, scegliere arbitrariamente o creare rischio di pubblicazione?
4. Il blocco riguarda tutto il run o un solo ramo?

Non chiedere dati già disponibili. Non navigare o accedere a sistemi non autorizzati per evitare la domanda.

## Formato obbligatorio della richiesta

La prima frase deve seguire esattamente questo schema:

> Mi serve [dato concreto].

Completare con:

> Senza questo non posso [decisione/output bloccato]. Puoi fornirmelo come [formato minimo]? Nel frattempo posso [eventuale output ridotto affidabile].

Regole:

- usare il nome reale del dato, non formule vaghe come "maggiori informazioni";
- non usare come X parole contenitore come `brief`, `dati`, `informazioni`, `dettagli`, `materiali` o `input` senza nominare subito gli elementi concreti;
- quando esistono più blocker, usare `Mi serve questo set minimo: [elementi concreti]` oppure aprire richieste separate, sempre entro il limite di cinque;
- spiegare l'impatto, non soltanto elencare campi;
- chiedere il minimo sufficiente;
- raggruppare al massimo cinque blocker strettamente collegati;
- mettere prima il blocker che sblocca più decisioni;
- non presentare l'alternativa ridotta come equivalente.

## Registro machine-readable

```yaml
missing_input:
  input_id: "INP-market-language"
  label: "mercato e lingua"
  classification: "run_blocking"
  required_for: ["activation_ready"]
  affected_modules: ["15-meta-ads-brief.yaml", "16-google-ads-playbook.md"]
  reason: "Prezzi, policy, keyword e landing dipendono dal mercato."
  minimum_acceptable: "Paese ISO e lingua."
  request_text: "Mi serve il mercato e la lingua."
  status: "requested"
  owner: "user"
  requested_at: "YYYY-MM-DD"
  resolved_at: null
  resolution_evidence_ids: []
```

Status consentiti: `identified`, `requested`, `provided`, `declined`, `unavailable`, `resolved`.

## Gate per output

### Onboarding

Run-blocker: nessuna fonte brand accessibile e nessun materiale fornito. Chiedere URL ufficiale o materiali. Dati economici, tracking e asset paid sono normalmente non bloccanti.

### Brand Voice

Per una voce sostenuta da `evidence`, basta un corpus ufficiale sufficientemente vario. Per una voce approvata, esempi accettati/rifiutati e conferma dell'owner sono bloccanti.

### Meta Ads live

Sono bloccanti: mercato/lingua, prodotto, offerta, obiettivo, audience o accettazione della persona come ipotesi, landing, claim autorizzati, stock/prezzo, economics, KPI/tracking e asset con diritti.

Esempio: `Mi serve il prodotto e l'offerta da promuovere. Senza questa scelta non posso costruire un brief Meta eseguibile. È sufficiente indicare SKU/famiglia, prezzo, incentivo e validità.`

### Google Ads live

Search richiede almeno mercato/lingua, conversione, landing, prodotto/servizio, economics e tracking. Shopping/PMax richiedono inoltre feed, identificatori, prezzo/stock sincronizzati, shipping e diagnostica Merchant Center.

Esempio: `Mi serve l'export del feed destinato alla Germania. Senza SKU, prezzo, stock, URL e identificatori per mercato non posso dichiarare Shopping o PMax pronti. Va bene un CSV o un export Merchant Center.`

### Market pack

Una ricerca pubblica preliminare può procedere senza dati interni. Un market pack operativo richiede catalogo, prezzi, stock, shipping, pagamenti, resi, customer care e owner locale per il mercato.

### Measurement

Un framework può essere creato senza baseline. Un piano di test eseguibile richiede obiettivo, evento primario, fonte dati, tracking verificato, guardrail e criterio decisionale.

## Risposta dell'utente

- Se il dato viene fornito, registrare fonte/data e riprendere dal gate bloccato.
- Se l'utente dice di non averlo, proporre la versione ridotta e registrare `unavailable`.
- Se l'utente rifiuta, registrare `declined`; non ripetere la domanda nello stesso run.
- Se il dato è parziale, chiedere solo la parte residua realmente bloccante.
- Non trasformare `unavailable` o `declined` in un'assunzione silenziosa.

## Criteri di accettazione

- Ogni blocker ha un `input_id` e un output impattato.
- La richiesta comincia con `Mi serve` e nomina un dato concreto.
- Un ramo non bloccato continua quando può produrre valore affidabile.
- Nessun output supera il relativo gate finché il blocker non è risolto.
- Il report finale distingue chiaramente ciò che è completo da ciò che attende l'utente.
