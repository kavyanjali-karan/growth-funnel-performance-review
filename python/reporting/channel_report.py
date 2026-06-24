def channel(df):

    return df.groupby("channel")["paid_users"].sum()