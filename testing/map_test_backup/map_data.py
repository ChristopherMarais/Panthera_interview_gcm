# Import packages
import pandas as pd
import requests
import os
import io
import json

# Function for retrieving CSVs from online source
def retrieve_data(url_str):
    req = requests.get(url_str).content.decode("utf-8")
    df = pd.read_csv(io.StringIO(req))
    return(df)

# Function for calculating difference between top and bottom of cumulative dataframe
def delta_estimate(x):
    return pd.Series(index=['delta_infected'],data=[((x.max()+x.tail(2).mean())/2)-((x.min()+x.head(2).mean())/2)])

# get working directory
#working_path = os.getcwd() # use for Jupyter
working_path = os.path.dirname(os.path.abspath(__file__)) #use for .py scripts

# define url strings for default values in function
cases_url_str = "https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_confirmed.csv"
deaths_url_str = "https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_deaths.csv"
recoveries_url_str = "https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_recoveries.csv"
mobility_url_str = "https://raw.githubusercontent.com/dsfsi/covid19za/master/data/mobility/google_mobility/mobility_report_ZA.csv"

def stats_get(cases_url=cases_url_str, deaths_url=deaths_url_str, recoveries_url=recoveries_url_str, mobility_url=mobility_url_str, day_window_size=7):
    # Import necessary data
    prov_keys_df = pd.read_csv(working_path+'/province_pop.csv', index_col='province')
    cases_df = retrieve_data(cases_url)
    deaths_df = retrieve_data(deaths_url)
    recoveries_df = retrieve_data(recoveries_url)
    mobility_df = retrieve_data(mobility_url)

    # collect and average mobility data for the past day_window_size days
    public_mobility_lst = ['retail and recreation','grocery and pharmacy','parks','transit stations', 'workplaces']
    mobility_df = mobility_df.sort_values(['date'])
    mobility_df = mobility_df.tail(n=10*day_window_size)
    mobility_df['total'] = mobility_df.loc[:,public_mobility_lst].sum(axis=1)
    mobility_window_avg_df = mobility_df.groupby(['province']).sum()/(5*day_window_size)
    mobility_window_avg_df = mobility_window_avg_df.drop(['Total'])

    # collect and average COVID data for the past day_window_size days
    cases_sort_df = cases_df.tail(n=day_window_size)[prov_keys_df['short_name']].reindex(sorted(prov_keys_df['short_name']), axis=1)
    cases_arr = cases_sort_df.values
    deaths_arr = deaths_df.tail(n=day_window_size)[prov_keys_df['short_name']].reindex(sorted(prov_keys_df['short_name']), axis=1).values
    recoveries_arr = recoveries_df.tail(n=day_window_size)[prov_keys_df['short_name']].reindex(sorted(prov_keys_df['short_name']), axis=1).values
    infected_df = pd.DataFrame((cases_arr - (deaths_arr + recoveries_arr)), columns=prov_keys_df['short_name'])
    infected_lst = infected_df.mean().values.tolist()

    #calcualte change in cumulative cases per province population for every 1000 people
    delta_cumulative_cases_df = cases_sort_df.apply(delta_estimate)*1000 # make number bigger and useable
    population_df = prov_keys_df.set_index(prov_keys_df.short_name)['population']
    norm_delta_cases_lst = (delta_cumulative_cases_df/population_df).values.tolist()[0] # normalize cases according to population size

    # Calculate statistics used for map
    prov_keys_df['window_infected_count'] = infected_lst # add change in number of infected in last day_window_size days
    prov_keys_df['norm_delta_cases'] = norm_delta_cases_lst
    prov_keys_df['window_avg_mobility'] = (mobility_window_avg_df['total']+100)/200 # normalise the mobility scores to range from 0 to 1 instead of -100 to 100 and add to table
    prov_keys_df['avg_infected_per_area'] = prov_keys_df['window_infected_count']/prov_keys_df['area'] #calculate number of infected people per square km
    prov_keys_df['infection_prob'] = prov_keys_df['window_avg_mobility']*prov_keys_df['avg_infected_per_area']*prov_keys_df['norm_delta_cases']  #estimnate infection probability score
    prov_keys_df = prov_keys_df.reset_index()

    return prov_keys_df

# define map file name
map_file = '/south_africa_administrative_state_province_boundary_edited.geojson'

def map_get(file_name=map_file):
    with open(working_path+file_name) as json_file:
        geojson_za = json.load(json_file)
    return geojson_za

def za_stats_get():
    df = stats_get()
    rsa_means = df[['population_density', 'norm_delta_cases', 'window_avg_mobility', 'avg_infected_per_area', 'infection_prob']].mean()
    rsa_sums = df[['population', 'area', 'avg_infected_per_area', 'window_infected_count']].sum()
    rsa_stats_df = pd.DataFrame(rsa_sums.append(rsa_means), columns=['RSA stats'])
    return rsa_stats_df