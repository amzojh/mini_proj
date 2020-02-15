
from sqlalchemy.engine import ResultProxy

from typing import Any
from pandas import DataFrame

class queryMaker():

    def __init__(self, db_session):
        self.db_session = db_session
        pass

    def insert_query_from_df(self, df : DataFrame, table_name : str) -> str: 
        
        columns_tuple = tuple(df.columns[1:])
        columns = str(columns_tuple)
        
        
        columns_with_constraints = set(self.get_column_list_with_key_constraints(table_name))
        columns_set = set(columns_tuple)
        columns_set = columns_set - columns_with_constraints
        
        values = df.apply(lambda x: str(tuple(x)), axis=1)        
        values = ",".join(values)
        
        query_statement = f"""
            insert into {table_name} {columns} values {values} 
            ON DUPLICATE KEY UPDATE
            
        """

        return query_statement


    def get_column_list_with_key_constraints(self, table_name):

        query = f"""
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns where 
            TABLE_NAME='{table_name}' and 
            COLUMN_KEY in ('pri', 'uni');
        """.replace("\n", "")

        result = self.db_session.execute(query)
        dict_list = self.parse_resultproxy_to_dict(result)

        result_list = []      
        for dict_obj in dict_list:
            result_list.append(dict_obj["COLUMN_NAME"])

        return result_list

    def parse_resultproxy_to_dict(self, result_proxy : ResultProxy) -> dict:
        dictionary, result_list = {}, []
        for rowproxy in result_proxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                dictionary = {**dictionary, **{column: value}}
            result_list.append(dictionary)

        return dictionary