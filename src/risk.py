import numpy as np

def sharpe_ratio(returns, risk_free=0.0):
    return np.mean(returns) / np.std(returns)

def max_drawdown(equity):
    peak = equity.cummax()
    dd = (equity - peak) / peak
    return dd.min()
