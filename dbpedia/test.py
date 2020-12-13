from DB_as_table import *

db_as_tab=DBpediaAsTable(r'F:\Datasets\DBpedia\complex_table\Comedian.csv')

marked_table=db_as_tab.table_marked(save_dir=r'./')

marked_table.table_decompose(name=db_as_tab.table_type)