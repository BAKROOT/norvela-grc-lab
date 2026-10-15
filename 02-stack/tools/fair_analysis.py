#!/usr/bin/env python3
"""FAIR quantitative risk analysis — Norvela Pay settlement fraud scenario.

Models the NOR-2026-0908 risk scenario quantitatively so you can answer the
question every CFO eventually asks: "how much is this worth fixing?"

Dependencies:  pip install numpy matplotlib
(pyfair is optional; this implements the Monte Carlo directly so you can see
the mechanics rather than treat them as a black box. Read the maths — being
able to explain PERT sampling in an interview is a real differentiator.)

Run:  python3 fair_analysis.py
"""
from __future__ import annotations

import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_PLT = True
except ImportError:
    HAVE_PLT = False

RNG = np.random.default_rng(20260908)
N = 100_000


def pert(low: float, mode: float, high: float, lam: float = 4.0,
         size: int = N) -> np.ndarray:
    """Modified-PERT sample.

    FAIR uses PERT because subject-matter experts can give you a minimum,
    a most-likely and a maximum far more reliably than they can give you a
    mean and a standard deviation. lam (lambda) controls confidence in the
    mode: 4 is the standard PERT default; raise it when the expert is
    confident, lower it when the estimate is soft.
    """
    if high <= low:
        return np.full(size, float(low))
    mu = (low + lam * mode + high) / (lam + 2)
    if np.isclose(mu, mode):
        a = b = 3.0
    else:
        a = ((mu - low) * (2 * mode - low - high)) / ((mode - mu) * (high - low))
        b = a * (high - mu) / (mu - low)
    a, b = max(a, 0.1), max(b, 0.1)
    return low + RNG.beta(a, b, size) * (high - low)


class Scenario:
    """One FAIR risk scenario.

    Risk = Loss Event Frequency x Loss Magnitude
    LEF  = Threat Event Frequency x Vulnerability
    LM   = Primary Loss + Secondary Loss (secondary only when it materialises)
    """

    def __init__(self, name, tef, vuln, primary, secondary, sec_prob):
        self.name = name
        self.tef = tef              # (low, mode, high) events per year
        self.vuln = vuln            # probability a threat event becomes a loss
        self.primary = primary      # (low, mode, high) EUR
        self.secondary = secondary  # (low, mode, high) EUR
        self.sec_prob = sec_prob    # probability secondary losses occur

    def simulate(self) -> np.ndarray:
        tef = pert(*self.tef)
        vuln = pert(*self.vuln)
        lef = tef * vuln
        events = RNG.poisson(np.maximum(lef, 0))

        annual = np.zeros(N)
        max_ev = int(events.max())
        for k in range(1, max_ev + 1):
            mask = events >= k
            n = int(mask.sum())
            if n == 0:
                continue
            prim = pert(*self.primary, size=n)
            sec = pert(*self.secondary, size=n)
            hit = RNG.random(n) < pert(*self.sec_prob, size=n)
            annual[mask] += prim + sec * hit
        return annual


def describe(name: str, losses: np.ndarray) -> dict:
    pct_zero = float((losses == 0).mean() * 100)
    d = {
        "name": name,
        "p_any_loss": 100 - pct_zero,
        "mean": float(losses.mean()),
        "p50": float(np.percentile(losses, 50)),
        "p90": float(np.percentile(losses, 90)),
        "p95": float(np.percentile(losses, 95)),
        "p99": float(np.percentile(losses, 99)),
        "max": float(losses.max()),
    }
    return d


def euro(x: float) -> str:
    return f"€{x:,.0f}"


def main() -> None:
    # ---------------------------------------------------------------- inputs
    # These are YOUR estimates. Change them. The point of the exercise is to
    # be able to defend each number, not to accept mine.
    #
    # Rationale for the CURRENT state, drawn from the dossier:
    #   TEF  - credential-stuffing / leaked-secret exploitation attempts
    #          against a payments API. Public repo exposure for 11 days in
    #          2024 raises this materially.
    #   Vuln - 6 unrotated secrets from the scan, no egress filtering, no
    #          anomaly detection on service accounts. High.
    #   Primary loss - direct unauthorised payouts. Observed €310k, €96k
    #          recovered. Range reflects that a longer dwell time could have
    #          been far worse.
    #   Secondary - supervisory response, forensics, legal, merchant
    #          remediation, churn. Banco de Portugal is already watching.

    current = Scenario(
        name="Settlement fraud via compromised service credential — CURRENT",
        tef=(1.0, 3.0, 8.0),
        vuln=(0.25, 0.45, 0.70),
        primary=(80_000, 310_000, 1_400_000),
        secondary=(150_000, 600_000, 2_800_000),
        sec_prob=(0.45, 0.65, 0.85),
    )

    # TREATED state assumes you implement, and can evidence:
    #   - short-lived credentials (IRSA / OIDC federation) for all services
    #   - automated rotation + secret scanning gate in CI
    #   - egress allow-listing from production
    #   - anomaly detection on service-account payout volume
    #   - 400-day application log retention for payment services
    treated = Scenario(
        name="Settlement fraud via compromised service credential — TREATED",
        tef=(1.0, 3.0, 8.0),          # threat activity is unchanged
        vuln=(0.02, 0.06, 0.15),      # you reduce VULNERABILITY, not TEF
        primary=(20_000, 70_000, 350_000),   # detection caps the loss
        secondary=(40_000, 150_000, 700_000),
        sec_prob=(0.20, 0.35, 0.55),
    )

    cur = current.simulate()
    trt = treated.simulate()

    c, t = describe("Current", cur), describe("Treated", trt)

    annual_control_cost = 180_000  # engineering + tooling, your estimate

    print("=" * 74)
    print("FAIR ANALYSIS — Norvela Pay")
    print("Scenario: unauthorised settlement payouts via compromised")
    print("          service-account credential (ref NOR-2026-0908)")
    print(f"Simulations: {N:,}")
    print("=" * 74)
    rows = [
        ("Probability of >=1 loss event in a year",
         f"{c['p_any_loss']:.1f}%", f"{t['p_any_loss']:.1f}%"),
        ("Mean annual loss (ALE)", euro(c["mean"]), euro(t["mean"])),
        ("Median (P50)", euro(c["p50"]), euro(t["p50"])),
        ("P90 — 1-in-10 bad year", euro(c["p90"]), euro(t["p90"])),
        ("P95", euro(c["p95"]), euro(t["p95"])),
        ("P99 — tail", euro(c["p99"]), euro(t["p99"])),
    ]
    print(f"\n{'Metric':<42}{'Current':>15}{'Treated':>15}")
    print("-" * 74)
    for label, a, b in rows:
        print(f"{label:<42}{a:>15}{b:>15}")

    reduction = c["mean"] - t["mean"]
    print("-" * 74)
    print(f"{'Expected annual loss avoided':<42}{euro(reduction):>30}")
    print(f"{'Annual cost of control':<42}{euro(annual_control_cost):>30}")
    print(f"{'Net annual benefit':<42}"
          f"{euro(reduction - annual_control_cost):>30}")
    if annual_control_cost:
        print(f"{'Return on control investment':<42}"
              f"{(reduction - annual_control_cost) / annual_control_cost:>29.1%}")
    print("-" * 74)

    print("\nHOW TO USE THIS IN A BOARD PAPER")
    print("Do not show the board a distribution. Show them one sentence:\n")
    print(f'  "Today, a bad year for this scenario costs us {euro(c["p90"])}.')
    print(f'   For {euro(annual_control_cost)} a year we reduce that to')
    print(f'   {euro(t["p90"])}. We recommend proceeding."\n')
    print("Keep the distribution in the appendix for whoever asks. Someone")
    print("always does, and being ready for that question is the point.\n")

    print("HOW TO DEFEND IT WHEN CHALLENGED")
    print("  * 'Your numbers are made up.'  -> They are calibrated estimates")
    print("    with stated ranges, which is strictly more honest than a red")
    print("    square on a heat map. Show the range, not a point.")
    print("  * 'Why is TEF unchanged after treatment?'  -> Because controls")
    print("    reduce vulnerability and loss magnitude. They do not reduce")
    print("    how often criminals try. Getting this wrong is the most")
    print("    common FAIR modelling error.")
    print("  * 'What would change your mind?'  -> Name the input you are")
    print("    least confident in (here: secondary loss probability) and say")
    print("    what evidence would tighten it.\n")

    if HAVE_PLT:
        fig, axes = plt.subplots(1, 2, figsize=(13, 5))

        ax = axes[0]
        bins = np.linspace(0, np.percentile(cur, 99.5), 70)
        ax.hist(cur[cur > 0], bins=bins, alpha=0.65, label="Current")
        ax.hist(trt[trt > 0], bins=bins, alpha=0.65, label="Treated")
        ax.set_title("Annual loss distribution (loss years only)")
        ax.set_xlabel("Annual loss (EUR)")
        ax.set_ylabel("Frequency")
        ax.legend()

        ax = axes[1]
        for data, label in ((cur, "Current"), (trt, "Treated")):
            s = np.sort(data)
            exceed = 1.0 - np.arange(1, len(s) + 1) / len(s)
            ax.plot(s, exceed * 100, label=label, linewidth=2)
        # Log axis from €10k: zero-loss years sit off-axis, so each curve
        # starts at its probability of any loss and decays through the tail.
        ax.set_xscale("log")
        ax.set_xlim(left=1e4)
        ax.set_ylim(0, 100)
        ax.set_title("Loss exceedance curve")
        ax.set_xlabel("Annual loss (EUR, log scale)")
        ax.set_ylabel("Probability of exceeding (%)")
        ax.grid(alpha=0.3)
        ax.legend()

        fig.suptitle("Norvela Pay — FAIR analysis, settlement fraud scenario")
        fig.tight_layout()
        out = "fair-settlement-fraud.png"
        fig.savefig(out, dpi=140)
        print(f"Chart written: {out}")
    else:
        print("(matplotlib not installed — skipping charts)")


if __name__ == "__main__":
    main()
