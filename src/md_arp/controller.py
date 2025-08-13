
from dataclasses import dataclass
import numpy as np
from .simulator import Params

@dataclass
class Targets:
    E_star: float = 0.05
    varG_star: float = 1e-4
    varC_star: float = 1e-4
    varL_star: float = 1e-4

@dataclass
class Gains:
    kE: float = 1.0
    kV: float = 0.5
    clamp_alpha: tuple = (1e-4, 5.0)   # min,max multiplier on alpha
    clamp_mu: tuple    = (1e-3, 2.0)   # min,max multiplier on mu

class MetaController:
    """
    Online adaptation of (alpha, mu) to keep energy and parameter variance
    within targets. Uses exponential moving stats over a short window.
    """
    def __init__(self, p0: Params, targets: Targets = Targets(), gains: Gains = Gains(), beta=0.98):
        self.p0 = p0
        self.t = 0.0
        self.targets = targets
        self.gains = gains
        self.beta = beta
        # EMA stats
        self.E_ema = targets.E_star
        self.G_ema = 0.0; self.G2_ema = 0.0
        self.C_ema = 0.0; self.C2_ema = 0.0
        self.L_ema = 0.0; self.L2_ema = 0.0

    def _var(self, m, m2):
        return max(m2 - m*m, 0.0)

    def update(self, t, state, params: Params, E):
        v,iL,G,C,L = state
        b = self.beta
        # update EMAs
        self.E_ema = b*self.E_ema + (1-b)*E
        self.G_ema = b*self.G_ema + (1-b)*G; self.G2_ema = b*self.G2_ema + (1-b)*G*G
        self.C_ema = b*self.C_ema + (1-b)*C; self.C2_ema = b*self.C2_ema + (1-b)*C*C
        self.L_ema = b*self.L_ema + (1-b)*L; self.L2_ema = b*self.L2_ema + (1-b)*L*L
        varG = self._var(self.G_ema, self.G2_ema)
        varC = self._var(self.C_ema, self.C2_ema)
        varL = self._var(self.L_ema, self.L2_ema)

        # control signals
        g = self.gains
        tar = self.targets
        # scalar multipliers
        alpha_scale = 1.0 + g.kE*(self.E_ema - tar.E_star) + g.kV*((varG - tar.varG_star)+(varC - tar.varC_star)+(varL - tar.varL_star))
        mu_scale    = 1.0 - 0.5*g.kE*(self.E_ema - tar.E_star)  # raise mu when energy > target

        # clamp multipliers
        a_lo,a_hi = g.clamp_alpha; m_lo,m_hi = g.clamp_mu
        alpha_scale = float(np.clip(alpha_scale, a_lo, a_hi))
        mu_scale    = float(np.clip(mu_scale,    m_lo, m_hi))

        # apply to all three
        new = Params(
            aG = self.p0.aG * alpha_scale,
            mG = self.p0.mG * mu_scale,
            aC = self.p0.aC * alpha_scale,
            mC = self.p0.mC * mu_scale,
            aL = self.p0.aL * alpha_scale,
            mL = self.p0.mL * mu_scale,
        )
        return new
