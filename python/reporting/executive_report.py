def executive(df):

    return df.groupby("month")["revenue"].sum()