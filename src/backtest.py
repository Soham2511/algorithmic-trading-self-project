def backtest(df, capital=1e9):
    df["Returns"] = df["Close"].pct_change() * df["Signal"].shift(1)
    df["Equity"] = (1 + df["Returns"]).cumprod() * capital
    return df
