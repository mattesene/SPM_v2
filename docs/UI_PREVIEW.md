# SPM_v2 — UI preview

## Dashboard

```text
┌─────────────────────────────────────────────────────────────────────┐
│ SPM_v2                         Dashboard   Analisi   Progressioni    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  BANKROLL              PROFITTO              DRAWDOWN               │
│  € 1.000,00             +€ 0,00               € 0,00                │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  SELEZIONI DI OGGI                                                   │
│                                                                     │
│  Inter       Milan        SPM 87   P(D) 31,8%   Quota 3,45   ★★★★☆ │
│  Roma        Lazio        SPM 82   P(D) 29,7%   Quota 3,20   ★★★★☆ │
│  Atalanta    Torino       SPM 76   P(D) 28,9%   Quota 3,40   ★★★☆☆ │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  PROGRESSIONI ATTIVE                                                 │
│                                                                     │
│  Inter        Livello 2    Puntata €20    Esposizione €30   ● ATTIVA│
│  Roma         Livello 1    Puntata €10    Esposizione €10   ● ATTIVA│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Analisi partita

```text
Inter — Milan                                      SPM SCORE 87/100

Probabilità pareggio        31,8%
Quota pareggio              3,45
Probabilità implicita       29,0%
EDGE                         +2,8%

STRISCIA / FORMA
Inter       W  L  W  D  L  W  L
Milan       L  W  L  L  W  L  W

[ Avvia progressione ]     [ Dettaglio statistico ]
```

## Principi UI

- mobile-first e responsive;
- schermata iniziale orientata alle decisioni;
- nessun dato inventato: tutti i valori devono arrivare dal motore SPM;
- colori usati solo per stato/alert, non per sostituire i valori numerici;
- storico e backtest sempre separati dalle selezioni operative.

Questa anteprima è intenzionalmente una specifica visuale iniziale: l'interfaccia verrà collegata alle API/dati del motore dopo la stabilizzazione della pipeline statistica e del backtest.
