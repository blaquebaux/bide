#!/usr/bin/python3
# =============================================================================
# bide_1.py — cash as a position: "wait for the fat pitch" (the Baupost/Klarman posture).
#
# Not a premium — a POSTURE. Capital preservation first, patient deep value, and cash held as an
# OPTION: sit in T-bills by default, deploy into equities only when a margin of safety appears (a
# drawdown from the highs), scale in as it deepens, retreat to cash on recovery. Absolute return,
# drawdown-first — the opposite of always-invested. Questions:
#   Q1  Does drawdown-triggered deployment beat buy-and-hold, risk-adjusted? (preservation scorecard)
#   Q2  What does the patience COST — time in cash and return forgone — in a bull decade?
#   Q3  Deploy into what: the market (SPY), low-vol (USMV), or deep value (VLUE)?
#   Q4  The honest cycle caveat — how many real "fat pitches" did 2016-2026 even offer?
# Alpaca SIP daily, total-return; cash = BIL (real T-bill yield). Causal; 2 bp/side on changes.
# =============================================================================
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from _bide_common import panel, rets, stats, skew_of, corr

COST = 2e-4

def ladder_positions(spy_px):
    """Causal drawdown ladder off the trailing 252-day high: deploy more as the drawdown deepens.
    Returns a per-bar equity weight in {0, .33, .66, 1.0} using YESTERDAY's drawdown (no peeking)."""
    n = len(spy_px); hi = np.array([spy_px[max(0, i-252):i+1].max() for i in range(n)])
    dd = spy_px / hi - 1.0                                  # current drawdown (<=0)
    w = np.zeros(n)
    for t in range(1, n):
        d = dd[t-1]                                         # act on yesterday's drawdown
        w[t] = 1.0 if d <= -0.20 else 0.66 if d <= -0.12 else 0.33 if d <= -0.06 else 0.0
    return w, dd

def run(spy_px, risk_rets, cash_rets):
    """Blend equity (risk_rets) and cash (cash_rets) by the ladder; net of switching cost."""
    w, dd = ladder_positions(spy_px)
    L = min(len(w)-1, len(risk_rets), len(cash_rets))
    w = w[1:L+1]; r = risk_rets[-L:]; c = cash_rets[-L:]
    switch = np.abs(np.diff(np.concatenate([[0.0], w])))
    strat = w * r + (1 - w) * c - switch * COST
    return strat, w

def preservation(name, r):
    r = np.asarray(r, float); cum = np.cumprod(1+r); dd = cum/np.maximum.accumulate(cum) - 1
    st = stats(r)
    return f"  {name:18}{st['sh']:>+7.2f}{st['cagr']*100:>+8.1f}%{st['dd']*100:>+8.0f}%{dd.mean()*100:>+9.1f}%{skew_of(r):>+7.2f}"

def main():
    syms = ["SPY", "BIL", "USMV", "VLUE", "IEF"]
    P, dates = panel(syms); R = {s: rets(P[s]) for s in syms if s in P}
    spy_px = P["SPY"]
    print("=" * 92); print("BIDE — cash as a position: 'wait for the fat pitch' (Baupost/Klarman posture)"); print("=" * 92)
    print(f"  window {dates[0]}..{dates[-1]}  ({len(dates)} days)")
    spy, bil = R["SPY"], R.get("BIL", np.zeros(len(R["SPY"])))

    # ---- Q1 / Q3: deployment target + preservation scorecard --------------------------------
    print("\n  Q1/Q3  DRAWDOWN-LADDER DEPLOYMENT (cash→equity as drawdown deepens), vs always-invested")
    print(f"  {'book':18}{'Sharpe':>7}{'CAGR':>9}{'maxDD':>9}{'avgDD':>10}{'skew':>7}")
    books = {}
    for tgt in ["SPY", "USMV", "VLUE"]:
        if tgt not in R: continue
        strat, w = run(spy_px, R[tgt], bil); books[f"bide→{tgt}"] = (strat, w)
        print(preservation(f"bide→{tgt}", strat))
    # benchmarks
    print(preservation("buy-hold SPY", spy))
    L = min(len(spy), len(R["IEF"])); print(preservation("60/40 SPY-IEF", 0.6*spy[-L:]+0.4*R["IEF"][-L:]))
    print(preservation("all-cash BIL", bil))

    # ---- Q2: the cost of patience ----------------------------------------------------------
    strat, w = books["bide→SPY"]
    print("\n  Q2  THE COST OF PATIENCE (bide→SPY)")
    print(f"      time in cash: {(w==0).mean()*100:.0f}%   fully deployed: {(w>=1.0).mean()*100:.0f}%   avg equity weight: {w.mean()*100:.0f}%")
    print(f"      CAGR {stats(strat)['cagr']*100:+.1f}% vs buy-hold {stats(spy)['cagr']*100:+.1f}%  → forgone {(stats(spy)['cagr']-stats(strat)['cagr'])*100:+.1f}%/yr")
    print(f"      maxDD {stats(strat)['dd']*100:+.0f}% vs buy-hold {stats(spy)['dd']*100:+.0f}%  → drawdown saved {(stats(strat)['dd']-stats(spy)['dd'])*100:+.0f}pts")

    # ---- Q4: how many fat pitches did the sample even offer? --------------------------------
    _, dd = ladder_positions(spy_px)
    deep = dd <= -0.12; crossings = int(np.sum((~deep[:-1]) & (deep[1:])))
    print("\n  Q4  FAT PITCHES IN SAMPLE")
    print(f"      distinct drawdowns beyond -12% (the deploy trigger): {crossings}   deepest: {dd.min()*100:.0f}%")
    print(f"      → a ~{len(dates)/252:.0f}-year bull decade offered only a handful; preservation postures are")
    print(f"        judged unfairly here — the payoff years (2000-02, 2008) are outside Alpaca's 2016+ window.")

    print("\n  READ: if bide cuts drawdown hard but gives up CAGR to cash drag, it is a genuine PRESERVATION")
    print("  posture, not alpha — and this bull sample is its worst case. bide_2 = the full-cycle test across")
    print("  2008 (Massive 2003+), where 'wait for the fat pitch' is supposed to earn its keep.")

if __name__ == "__main__":
    main()
