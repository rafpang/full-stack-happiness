import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2 as ps
from sklearn.impute import KNNImputer
from pandasql import sqldf

#additional py files in repo
import config as c 
from postgres import *


sql = lambda q: sqldf(q, globals())

def connect_db(host_name, dbname, port, username, password):
  try:
    conn = ps.connect(host= host_name , database = dbname , 
                      user = username , password = password , port = port )
  
  except ps.OperationalError as e:
    raise e
  else: 
    print('Connected!')
  return conn

if __name__ == '__main__':
    
  #Ingest data
  master_df = pd.read_csv('cleaned_datasets/happiness_data.csv', header = 1, na_values = '..')
  trust_df = pd.read_csv('cleaned_datasets/DP_LIVE_15092022141010965.csv')
  codes_df = pd.read_csv('cleaned_datasets/country_codes.csv')
  master_df= master_df.drop(master_df[master_df.Country == 'OECD - Total'].index)
  

      #Joining data using pandasql; a tool that lets us leverage sql syntax for pandas
  q_join = """SELECT *
      FROM master_df as m LEFT JOIN codes_df as c
      ON m.Country = c.name    
      
      """
  master_joined = sql(q_join)
  q_join_2 = """ WITH trust_2021 AS (
              SELECT LOCATION, value
                              FROM trust_df  
                              WHERE TIME = 2021)
              SELECT * 
              FROM master_joined as m LEFT JOIN trust_2021 as t
              on m.country_code = t.LOCATION
      
      """

  master_joined_trust = sql(q_join_2)

  #Insert manually the government trust in Luxembourg in 2021, taken from 
  # https://www.statista.com/statistics/586199/public-trust-in-the-national-government-in-luxembourg/

  master_joined_trust.loc[master_joined.Country == 'Luxembourg', 'value'] = 67.000
  
  #Deleting the region-code columnn
  master_joined_trust = master_joined_trust.drop(columns = ['region-code'])    
  
  #Fitting numeric values to KNNImputer
  numeric = master_joined_trust.select_dtypes(exclude = 'object')
  list_of_columns = list(numeric.columns) 
  knn_impute = KNNImputer(n_neighbors = 5)
  numeric_imputed = knn_impute.fit_transform(numeric)
  master_joined_trust = master_joined_trust.drop(columns = ['name', 'LOCATION'])
      
  #Creating a new data frame called final_cleaned_df; containing the "final cleaned dataframe"
  final_cleaned_df = pd.DataFrame(numeric_imputed, columns  = list(numeric.columns))

  final_cleaned_df['country'] = master_joined_trust['Country']
  final_cleaned_df['sub_region'] = master_joined_trust['sub-region']
  final_cleaned_df['intermediate_region'] = master_joined_trust['intermediate-region']
  final_cleaned_df['country_code'] = master_joined_trust['country_code']
  final_cleaned_df = final_cleaned_df[['country_code','country', 'sub_region', 'intermediate_region'] + list(numeric.columns)]
      
  #fixing a typo on the dataframe!
  final_cleaned_df['household_nadi'] = final_cleaned_df['household _nadi']
  final_cleaned_df = final_cleaned_df.drop(columns = ['household _nadi']) 

  #connecting to AWS RDS instance and creating the table to input data
  con = connect_db(host_name = c.HOST_NAME, dbname=c.DBNAME, port=c.PORT, 
                      username=c.USERNAME, password= c.PASSWORD)
  curr = con.cursor() 
  create_table(curr)
  con.commit()

  #Inserting rows into the table
  for i, row in final_cleaned_df.iterrows():
      insert_into_table(insert_command, curr, 
                      row.country_code,
                      row.country,
                      row.sub_region,
                      row.intermediate_region,
                      row.dwelings_without_percentage,
                      row.housing_expenditure,
                      row.rooms_per_person,
                      row.household_nadi,
                      row.household_net_wealth,
                      row.lmi_percentage,
                      row.employment_rate,
                      row.lt_unemplotyment_rate,
                      row.personal_earnings,
                      row.quality_support_network,
                      row.educational_attachment_percentage, 
                      row.student_scores,
                      row.years_in_edu,
                      row.mg_m3,
                      row.water_quality_percentage,
                      row.stakeholder_engagement,
                      row.voter_turnout_pct,
                      row.life_expectancy,
                      row.self_support_health,
                      row.life_satisfaction_score,
                      row.safe_at_night,  
                      row.homicide_rate,
                      row.employ_long_hours_pct,
                      row.leisure_time,
                      row.value)
  con.commit()