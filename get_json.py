import pandas as pd
import json
import requests
import streamlit as st

cod_data_url = "https://api.tracker.gg/api/v1/cold-war/matches/xbl/Cording%20Xx?type=mp&next=null"
headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/50.0.2661.102 Safari/537.36'}
result = requests.get(cod_data_url, headers=headers)
data = json.loads(result.content.decode())

df = pd.json_normalize(data["data"]["matches"], sep="_")

# newresp = pd.json_normalize(data["data"]["matches"]["segments"], sep="_")

st.title("CoD:Cold War data")
st.write(df)
