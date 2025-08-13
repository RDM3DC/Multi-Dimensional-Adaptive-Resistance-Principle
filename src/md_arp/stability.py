
import numpy as np
from numpy.linalg import eigvals
from md_arp.simulator import Params, Caps, derivatives, current_input

def jacobian(t, y, p: Params, caps: Caps, input_fn=current_input, input_kwargs=None, eps=1e-6):
    """
    Finite-difference Jacobian of the 5D ODE: f = [dv, diL, dG, dC, dL].
    """
    if input_kwargs is None: input_kwargs = {}
    f0 = derivatives(t, y, p, caps, input_fn, input_kwargs)
    n = len(y)
    J = np.zeros((n, n), dtype=float)
    for i in range(n):
        y_ = y.copy()
        dy = eps*(1.0 + abs(y_[i]))
        y_[i] += dy
        fi = derivatives(t, y_, p, caps, input_fn, input_kwargs)
        J[:, i] = (fi - f0) / dy
    return J

def local_eigs(t, y, params: Params, caps: Caps, input_fn=current_input, input_kwargs=None):
    J = jacobian(t, y, params, caps, input_fn, input_kwargs)
    return eigvals(J)

def settle_equilibrium(y0, params: Params, caps: Caps, input_fn=current_input, input_kwargs=None, dt=8e-4, T=3.0):
    """
    Run the simulator without controller and return the last state as an approximate fixed point.
    """
    from md_arp.simulator import simulate
    arr = simulate(T=T, dt=dt, params=params, caps=caps, y0=y0, input_fn=input_fn, input_kwargs=input_kwargs, controller=None)
    return arr[-1], arr
