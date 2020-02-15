import pandas as pd


class queryMaker():

    def __init__(self):
        pass

    def insert_query_from_df(self, df=None, table_name=None, update_columns_list=None):
        
        table = "listing_table"
        df = pd.read_csv("companyList.csv")
        df["CompanyCode"] = df["CompanyCode"].astype(str).str.zfill(6)

        columns = str(tuple(df.columns[1:]))
        values = df.apply(lambda x: str(tuple(x)), axis=1)
        
        query_statement = f"""
            insert into {table} {columns} values {values} ON DUPLICATE KEY UPDATE 
        """

        return query_statement
