import sqlite3

class TableDefinition:
    def __init__(self, table_name, columns):
        self.table_name = table_name
        self.columns = columns

    def create_table_query(self):
        column_defs = []
        for column_name, column_type in self.columns.items():
            column_defs.append(f"{column_name} {column_type}")
        column_defs_str = ", ".join(column_defs)
        return f"CREATE TABLE IF NOT EXISTS {self.table_name} ({column_defs_str});" # f는 문자열에 변수를 넣을 때 사용


