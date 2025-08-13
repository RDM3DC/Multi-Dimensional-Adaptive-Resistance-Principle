# md-arp
**Multi-Dimensional Adaptive Resistance Principle** — unified adaptive **G (conductance)**, **C (capacitance)**, and **L (inductance)** dynamics for neuromorphic, superconducting-adjacent, and optimization systems.

This repo contains:
- A reference simulator for an adaptive parallel RLC (current-driven).
- A **meta-controller** that automatically steers (α, μ) to hold stability/energy targets.
- Reproducible experiments: phase scan, DC-step, hysteresis (memory), and noise robustness.
- CSV outputs + figures ready for papers/threads.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

# Run a demo with the meta-controller enabled
python src/main.py demo --plot
```

## Experiments
```bash
# Phase scan over shared alpha/mu ratios
python src/experiments/phase_scan.py --ratios 0.5 1 2 3.5 5 7 8 --T 2.0

# DC step input (u=1) equilibrium & stability check
python src/experiments/dc_step.py --T 2.0

# Hysteresis under triangle input
python src/experiments/hysteresis.py --T 2.0 --freq 0.25

# Noise robustness (adds Gaussian noise to sine input)
python src/experiments/noise_test.py --noise_sigma 0.1 --T 2.0
```

Outputs are saved under `out/` (CSV and PNG).

## Model
State: \(x=[v, i_L, G, C, L]\). Current source input \(u(t)\).

**KCL (variable C):**
\[
u = Gv + C\dot v + v\dot C + i_L \quad \Rightarrow \quad
\dot v = \frac{u - Gv - v\dot C - i_L}{C}.
\]

**Inductor (variable L):**
Flux \(\lambda = L i_L\Rightarrow v = \dot\lambda = L\dot i_L + i_L\dot L\)  
\[
\dot i_L = \frac{v - i_L\dot L}{L}.
\]

**ARP laws:**
\[
\dot G = \alpha_G |Gv| - \mu_G G,\quad
\dot C = \alpha_C |v| - \mu_C C,\quad
\dot L = \alpha_L |i_L| - \mu_L L.
\]

**Energy candidate:** \(E=\tfrac12 C v^2 + \tfrac12 L i_L^2\).

## Meta-Controller
We adapt \(\alpha,\mu\) online to hold a target energy and bound parameter variance:
\[
\alpha_X(t)=\alpha_X^0\,\big(1+k_E(E-E^*)+k_V(\mathrm{Var}[X]-\sigma_X^{2*})\big)_{+},
\]
with clamping and decay floors; similarly for \(\mu\). This keeps the system in the **convergent** regime while retaining responsiveness.

## Citation
If this repo helps your research, please cite:
> McKenna, R. (2025). *Multi-Dimensional ARP (md-arp): Unified adaptive G, C, L dynamics.*

