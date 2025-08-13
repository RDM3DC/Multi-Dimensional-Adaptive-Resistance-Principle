
import numpy as np
from dataclasses import dataclass

@dataclass
class Caps:
    G_min: float = 1e-4
    C_min: float = 1e-4
    L_min: float = 1e-4
    G_max: float = 10.0
    C_max: float = 10.0
    L_max: float = 10.0

@dataclass
class Params:
    aG: float = 1.0
    mG: float = 0.5
    aC: float = 0.25
    mC: float = 0.1
    aL: float = 0.25
    mL: float = 0.1

@dataclass
class State:
    v: float
    iL: float
    G: float
    C: float
    L: float

def current_input(t, A=1.0, f=1.0, bias=0.0):
    return bias + A*np.sin(2*np.pi*f*t)

def triangle_input(t, A=1.0, f=0.25, bias=0.0):
    # simple symmetric triangle: value in [-1,1]
    tau = (t * f) % 1.0
    x = 4*tau - 2.0
    tri = 1.0 - abs(x)
    return bias + A*(2*tri - 1.0)

def derivatives(t, y, p: Params, caps: Caps, input_fn, input_kwargs):
    v, iL, G, C, L = y
    iG = G*v
    dG = p.aG*abs(iG) - p.mG*G
    dC = p.aC*abs(v)  - p.mC*C
    dL = p.aL*abs(iL) - p.mL*L
    C_eff = max(C, caps.C_min)
    L_eff = max(L, caps.L_min)
    u = input_fn(t, **input_kwargs)
    dv  = (u - G*v - v*dC - iL)/C_eff
    diL = (v - iL*dL)/L_eff
    return np.array([dv, diL, dG, dC, dL], float)

def rk4_step(t, y, h, p, caps, input_fn, input_kwargs):
    k1 = derivatives(t, y, p, caps, input_fn, input_kwargs)
    k2 = derivatives(t + 0.5*h, y + 0.5*h*k1, p, caps, input_fn, input_kwargs)
    k3 = derivatives(t + 0.5*h, y + 0.5*h*k2, p, caps, input_fn, input_kwargs)
    k4 = derivatives(t + h, y + h*k3, p, caps, input_fn, input_kwargs)
    return y + (h/6.0)*(k1 + 2*k2 + 2*k3 + k4)

def energy(v, iL, C, L, caps: Caps):
    C_eff = max(C, caps.C_min)
    L_eff = max(L, caps.L_min)
    return 0.5*C_eff*v*v + 0.5*L_eff*iL*iL

def simulate(T=2.0, dt=8e-4, 
             params: Params=Params(),
             caps: Caps=Caps(),
             y0=(0.0,0.0,0.2,1.0,1.0),
             input_fn=current_input, input_kwargs=None,
             controller=None):
    if input_kwargs is None:
        input_kwargs = {}
    N = int(T/dt)
    t=0.0
    y=np.array(y0, float)
    hist = np.zeros((N,6))
    for k in range(N):
        v,iL,G,C,L = y
        E = energy(v,iL,C,L,caps)
        # meta-controller may modify params based on recent history
        if controller is not None:
            params = controller.update(t, y.copy(), params, E)
        hist[k] = [t,v,iL,G,C,L]
        y_next = rk4_step(t, y, dt, params, caps, input_fn, input_kwargs)
        # bounds
        y_next[2] = float(np.clip(y_next[2], caps.G_min, caps.G_max))
        y_next[3] = float(np.clip(y_next[3], caps.C_min, caps.C_max))
        y_next[4] = float(np.clip(y_next[4], caps.L_min, caps.L_max))
        if not np.isfinite(y_next).all():
            hist = hist[:k+1]
            break
        y = y_next
        t += dt
    return hist
