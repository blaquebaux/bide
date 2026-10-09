# bide

**Cash as a position — "wait for the fat pitch" (the Baupost / Klarman posture).**

Not a premium, a *posture*: capital preservation first, patience, and cash held as an **option** —
sit in T-bills by default, deploy into equities only when a margin of safety appears (a drawdown from
the highs), scale in as it deepens, retreat on recovery. Absolute return, drawdown-first. The
conservative end of the hedge-fund risk spectrum — a "hedge fund" that sits nearer a family office
than a macro fund. Alpaca SIP daily, total-return; cash = `BIL` (real T-bill yield); causal, 2 bp/side.

## Verdict

**NULL as a mechanical posture — a boring 60/40 dominates it in this sample.** The preservation DNA
is real (positive skew, almost never underwater), but waiting in cash gives up too much to beat a
static balanced book, and the Klarman *edge* — security selection, not cash-timing — isn't something
a drawdown-ladder into index ETFs can capture.

| book | Sharpe | CAGR | maxDD | avg DD | skew |
|---|---|---|---|---|---|
| **bide → SPY** (drawdown ladder) | +0.59 | +5.5% | −22% | **−0.4%** | **+0.07** |
| bide → USMV | +0.47 | +3.8% | −24% | −0.5% | +0.11 |
| bide → VLUE | +0.44 | +4.3% | −24% | −0.6% | +0.02 |
| buy-hold SPY | +0.88 | +15.0% | −34% | −4.2% | −0.35 |
| **60/40 SPY-IEF** | **+0.93** | **+9.7%** | **−21%** | −3.2% | −0.24 |
| all-cash BIL | +7.88* | +2.1% | −0% | −0.0% | +0.33 |

\*cash's "Sharpe" is a low-vol artifact, not a return.

**The honest comparison that sinks it:** 60/40 beats bide on **Sharpe (0.93 vs 0.59), return
(+9.7 vs +5.5%), *and* drawdown (−21 vs −22%)** — all three. Being 78% in cash (12% average equity
weight) buys positive skew and a ~0 average drawdown, but you can preserve capital *more efficiently*
by just holding bonds. The patient-cash posture is dominated.

## Why it's null here — and where the edge actually lives

Two reasons this is the posture's worst case, not its fair test:

1. **Wrong regime.** 2016–2026 is a bull decade; the ~17 dips past the −12% trigger were mostly shallow
   and V-shaped (2020 recovered in months). "Wait for the fat pitch" earns its keep in *secular* bears
   — 2000-02, 2008 — which sit outside Alpaca's 2016+ window. A preservation posture judged in a bull is
   judged unfairly (the standing weak-sample problem).
2. **Wrong mechanism.** Klarman's return isn't cash-timing — it's **security selection with a margin of
   safety** and concentrated conviction when he *does* deploy. A mechanical drawdown-ladder into SPY/USMV/
   VLUE can't express that; it only tests the cash-as-option wrapper, which is the least special part.

## `bide_2`

The fair test: **full-cycle history (Massive 2003+, through 2008)** so the fat-pitch years are in sample,
plus a real **cheapness / margin-of-safety trigger** (earnings yield vs rates, credit spreads) rather than
a pure drawdown trigger — and, ideally, deployment into a deep-value *security-selection* book, not an
index ETF. Until then, the mechanical posture is beaten by 60/40.

## Reproduce

```bash
export ALPACA_KEY_ID=... ALPACA_SECRET_KEY=...
python3 research/bide_1.py
```

`SPY/BIL/USMV/VLUE/IEF`, 2016-01 … 2026-07. Deployment is a causal drawdown ladder off the trailing
252-day high (0 / 33 / 66 / 100% equity at 0 / −6 / −12 / −20% drawdown), acting on yesterday's
drawdown, cash earning `BIL`, 2 bp/side on changes.

---

*Blaque Baux — a Carter Warrens research initiative. Research only; not investment advice. The verdict
falls where the data puts it — and this bull decade is this posture's worst case.*
