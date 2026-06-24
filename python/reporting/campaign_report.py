def campaign(df):

    return df.groupby("campaign")["revenue"].sum()