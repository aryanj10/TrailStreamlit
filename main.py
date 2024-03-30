import requests as r
import pandas as pd

def get_data(url):
  api = r.get(url)
  api_status_code = api.status_code #200

  api_data = api.json() #converting into json format
  api_data_normal = pd.json_normalize(api_data) #converting into dataframe
  
  return api_data_normal

get_data('https://api.tfl.gov.uk/AccidentStats/2019')

api_data_normal = get_data('https://api.tfl.gov.uk/AccidentStats/2019')

api_casualities = pd.json_normalize(api_data_normal['casualties'])
api_casualities_col  = pd.json_normalize(api_casualities[0])
#api_casualities_col['$type'][0]
api_casualities_col = api_casualities_col.drop(columns = '$type')
casuality_cols = api_casualities_col.columns
age = pd.Series(api_casualities_col['age'], name = 'age')
casualities_class = pd.Series(api_casualities_col['class'], name = 'class')
severity = pd.Series(api_casualities_col['severity'], name = 'severity')
mode = pd.Series(api_casualities_col['mode'], name = 'mode')
ageBand = pd.Series(api_casualities_col['ageBand'], name = 'ageBand')

api_vehicles = pd.json_normalize(api_data_normal['vehicles'])
api_vehicles_col = pd.json_normalize(api_vehicles[0])
api_vehicles_col = pd.Series(api_vehicles_col['type'], name = 'vehicles')

api_data_normal = api_data_normal.drop(columns = ['$type','casualties', 'vehicles'])
api_data_modified = pd.concat([api_data_normal,age, casualities_class, mode, ageBand, api_vehicles_col], axis=1)


class_dict = dict(api_data_modified['class'].value_counts())
class_df = pd.DataFrame(class_dict.items(), columns = ['class', 'count'])

mode_dict = dict(api_data_modified['mode'].value_counts())
mode_df = pd.DataFrame(mode_dict.items(), columns = ['mode', 'count'])

age_dict = dict(api_data_modified['age'].value_counts())
age_df = pd.DataFrame(age_dict.items(), columns = ['age', 'count'])

drop_cols = ['id', 'location', 'date', 'severity', 'borough', 'age', 'class', 'mode', 'ageBand', 'vehicles']
map_df = api_data_modified.drop(columns = drop_cols)

import streamlit as st

dataExploration = st.container()

with dataExploration:
  st.title('Transport for London')
  st.subheader('Keeping London moving...')
  st.header('Dataset: Transport for London')
  st.markdown('I found this dataset at... https://tfl.gov.uk/info-for/open-data-users/')
  st.markdown('**Basically, it is a "London AccidentStats" dataset for the year 2019**')
  st.text('Below is the sample DataFrame')
  st.write(api_data_modified.head())


map_con = st.container()

drop_cols = ['id', 'location', 'date', 'severity', 'borough', 'age', 'class', 'mode', 'ageBand', 'vehicles']
map_df = api_data_modified.drop(columns = drop_cols)

with map_con:
  st.header('A simple map of the accident zones in london')
  st.map(map_df, use_container_width =  True)

@st.cache
def get_data():
  api = r.get('https://api.tfl.gov.uk/AccidentStats/2019')
  api_status_code = api.status_code

  api_data = api.json()
  api_data_normal = pd.json_normalize(api_data)
  cols = api_data_normal.columns
  return api_data_normal
