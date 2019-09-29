import pandas as pd

from typing import Any
from pandas import DataFrame

class queryMaker():

    def __init__(self):
        pass

    def insert_query_from_df(self, df : DataFrame, table_name : str) -> str: 
        
        columns = str(tuple(df.columns[1:]))
        values = str(df.apply(lambda x: str(tuple(x)), axis=1))
        
        query_statement = f"""
            insert into {table_name} {columns} values {values} ON DUPLICATE KEY UPDATE
        """

        return query_statement
