# Evidence governance

## Stati

| Stato | Significato | Uso pubblico |
|---|---|---|
| evidence | osservato direttamente in una fonte | sì, entro il perimetro |
| inference | interpretazione sostenuta da evidenze | solo come interpretazione |
| hypothesis | modello da testare | no come fatto |
| missing | informazione non disponibile | no |
| blocked | esiste un rischio o requisito irrisolto | no |

## Stato dei claim

| Stato | Significato |
|---|---|
| approved-for-ads | approvato esplicitamente con perimetro |
| public-brand-claim | dichiarato pubblicamente dal brand, non ancora approvato per ADV |
| observed-spec | specifica osservata e verificabile |
| qualified-only | utilizzabile solo con caveat |
| blocked | non pubblicabile senza nuova prova |

## Campi minimi di una prova

```yaml
evidence_id: EV-000
statement: ""
source_url: ""
source_type: "official|internal|review|retailer|editorial|tool"
observed_at: "YYYY-MM-DD"
market: "global|IT|DE|..."
scope: "brand|category|product_id|policy"
status: "evidence|inference|hypothesis|missing|blocked"
confidence: "high|moderate|low"
expires_at: null
notes: ""
```

## Gerarchia delle fonti

1. Dati interni con owner e definizione.
2. Fonte ufficiale primaria.
3. Piattaforma o documento normativo pertinente.
4. Retailer e marketplace.
5. Recensioni e community.
6. Editoriale e tool di stima.

Una fonte più autorevole non cancella automaticamente un'esperienza cliente: descrivono oggetti diversi.

## Dati mutevoli

Prezzi, stock, spedizione, resi, policy, specifiche di piattaforma e competitor richiedono data di accesso e ricontrollo prima della pubblicazione.

## Recensioni

- Conservare piattaforma, data, rating, verified status quando disponibile e oggetto recensito.
- Separare brand, prodotto, retailer e logistica.
- Non presentare frequenze se il campione non è censito o rappresentativo.
- Non usare un verbatim in pubblicità senza autorizzazione.

## Contraddizioni

Registrare entrambe le fonti, definire cosa misurano, attribuire affidabilità per la decisione e aprire un gap. Non scegliere la versione più favorevole.

