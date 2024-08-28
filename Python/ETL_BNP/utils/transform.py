import pandas as pd
import datacompy
#import pyodbc
import config as cfg
import sqlalchemy
from sqlalchemy import text

def transform_data(df: pd.DataFrame):
    """
    Function to transfrom dataframe
    """
    df.columns= df.columns.str.lower()
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    
    df = df.rename(columns={'date_bnp': 'test_date'})
    
    #remove pace labids
    df = df[~(df['labid'].str[:2].str.contains('UT'))]
    
    connexion_str = sqlalchemy.engine.URL.create(
    "mssql+pyodbc",
    username=cfg.sql['user'],
    host=cfg.sql['server'],
    database=cfg.sql['db'],
    query={
        "driver": cfg.sql['driver'],
        "authentication": cfg.sql['authentication'],
    },
    )

    engine = sqlalchemy.create_engine(connexion_str)
    
    
    #Bring in the lab information
    query = 'SELECT * from [dbo].[ImpactLab_A]'
    df_lab = pd.read_sql_query(sql=text(query), con=engine.connect())
    
    #compare datasets
    compare = datacompy.Compare(df_lab,df,join_columns=['LABID'])
    df_notincchc=compare.df2_unq_rows
    #df_matches=df.loc[~df.labid.isin(df_notincchc['labid'])]
    

    return df,df_notincchc