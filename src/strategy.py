def sma_strategy(df, short=20, long=50):
    df["SMA_short"] = df["Close"].rolling(short).mean()
    df["SMA_long"] = df["Close"].rolling(long).mean()
    df["Signal"] = 0
    df.loc[df["SMA_short"] > df["SMA_long"], "Signal"] = 1   # Buy
    df.loc[df["SMA_short"] < df["SMA_long"], "Signal"] = -1  # Sell
    return df
