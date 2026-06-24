def growth(df):

    return df.groupby("channel")["signups"].sum()