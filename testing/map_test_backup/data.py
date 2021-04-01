# Import packages
import pandas as pd
import requests
import io

# Scrape/access data from https://github.com/dsfsi/covid19za and add to dataframe
# "https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_confirmed.csv"
def retrieve_data(url_str):
    req = requests.get(url_str).content.decode("utf-8")
    df = pd.read_csv(io.StringIO(req))
    return(df)