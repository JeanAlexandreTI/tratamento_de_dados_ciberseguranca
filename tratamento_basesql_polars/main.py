#%%
import polars as pl
import mysql.connector
from datetime import datetime 

from dotenv import load_dotenv
import os

load_dotenv(override=True)

password_sql = os.getenv('PASSWORD_SQL')
user = os.getenv('USER')
host = os.getenv('LOCALHOST')
database = os.getenv('DATABASE')

print(password_sql)
print(user)
print(host)
print(database)

#%%

cx = mysql.connector.connect(
    host = host,
    database = database,
    user = user,
    password = password_sql
)   

if cx.is_connected():
    print('Conectado ao bd.')
    cursor = cx.cursor()

#%%
cursor.execute('''
    SELECT *
    FROM incident
''')


df_incidentes = {
    'incident_id':[],
    'ticket_code':[],
    'client_id':[],
    'incident_type':[],
    'severity':[],
    'resolved_at':[],
    'status':[]
}

for i in cursor:
    df_incidentes['incident_id'].append(i[0])
    df_incidentes['ticket_code'].append(i[1])
    df_incidentes['client_id'].append(i[2])
    df_incidentes['incident_type'].append(i[3])
    df_incidentes['severity'].append(i[4])
    df_incidentes['resolved_at'].append(i[5])
    df_incidentes['status'].append(i[6])

base_tratamento = pl.DataFrame(df_incidentes)

#%%
base_tratamento = base_tratamento.with_columns(
    pl.when(pl.col('status').str.contains('canceled') & pl.col('resolved_at').is_not_null()).then(pl.lit(None)).otherwise(pl.col('resolved_at')).alias('resolved_at'),
    pl.when(pl.col('status').str.contains('resolved') & pl.col('resolved_at').is_null()).then(pl.lit('in progress')).otherwise(pl.col('status')).alias('status'),
    pl.when(pl.col('incident_id') ==  3).then(pl.lit('SEC-1599')).otherwise(pl.col('ticket_code')).alias('ticket_code')
)

#%%
data_inexistente = datetime(1800, 1, 1, 0, 0, 0)

base_tratamento = base_tratamento.with_columns(
    pl.col('resolved_at').fill_null(data_inexistente).alias('resolved_at')
)

#%%
base_tratamento = base_tratamento.select(
    pl.col('incident_id'),
    pl.col('ticket_code').str.to_uppercase(),
    pl.col('client_id'),
    pl.col('incident_type').str.replace('brute-fore', 'brute-force').str.replace('pishing', 'phishing').str.to_uppercase(),
    pl.col('severity').str.to_uppercase(),
    pl.col('resolved_at'),
    pl.col('status').str.to_uppercase()
)

#%%
base_tratamento = base_tratamento.unique(subset='ticket_code')
base_tratamento = base_tratamento.sort('incident_id')
#%%
print(base_tratamento)
#%%
cx.close()
cursor.close()
# %%
