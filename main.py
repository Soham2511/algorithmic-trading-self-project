import pandas as pd
import numpy as np


df = pd.read_csv("data/reliance.csv", parse_dates=["Date"], index_col="Date")
print(df.head())

def sma_strategy(df, short=20, long=50):
    df["SMA_short"] = df["Close"].rolling(short).mean()
    df["SMA_long"] = df["Close"].rolling(long).mean()
    df["Signal"] = 0
    df.loc[df["SMA_short"] > df["SMA_long"], "Signal"] = 1   # Buy
    df.loc[df["SMA_short"] < df["SMA_long"], "Signal"] = -1  # Sell
    return df

def backtest(df, capital=1e9):
    df["Returns"] = df["Close"].pct_change() * df["Signal"].shift(1)
    df["Equity"] = (1 + df["Returns"]).cumprod() * capital
    return df

def sharpe_ratio(returns, risk_free=0.0):
    return np.mean(returns) / np.std(returns)

def max_drawdown(equity):
    peak = equity.cummax()
    dd = (equity - peak) / peak
    return dd.min()

import matplotlib.pyplot as plt

df = pd.read_csv("data/reliance.csv", parse_dates=["Date"], index_col="Date")
df = sma_strategy(df)
df = backtest(df)

plt.figure(figsize=(10,5))
plt.plot(df.index, df["Equity"], label="Equity Curve")
plt.title("Strategy Backtest - Reliance")
plt.legend()
plt.show()

print("ROI:", (df["Equity"].iloc[-1] - 1e9) / 1e9 * 100, "%")
print("Sharpe:", sharpe_ratio(df["Returns"]))
print("Max Drawdown:", max_drawdown(df["Equity"]))

with open("results/metrics.txt", "w") as f:
    f.write(f"ROI: {(df['Equity'].iloc[-1] - 1e9) / 1e9 * 100:.2f}%\n")
    f.write(f"Sharpe: {sharpe_ratio(df['Returns']):.2f}\n")
    f.write(f"Max Drawdown: {max_drawdown(df['Equity']):.2f}\n")