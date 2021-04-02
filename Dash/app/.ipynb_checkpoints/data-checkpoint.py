# Import packages
import pandas as pd
import requests
import os
import io
import json

# province full and short names
prov_name_lst = [
    'Eastern Cape',
    'Free State',
    'Gauteng',
    'KwaZulu-Natal',
    'Limpopo',
    'Mpumalanga',
    'Northern Cape',
    'North West',
    'Western Cape',
    'Total'
]

prov_name_dict = {
    'EC':'Eastern Cape',
    'FS':'Free State',
    'GP':'Gauteng',
    'KZN':'KwaZulu-Natal',
    'LP':'Limpopo',
    'MP':'Mpumalanga',
    'NC':'Northern Cape',
    'NW':'North West',
    'WC':'Western Cape',
    'total':'Total'
}

# names of mobility areas
mob_name_lst = [
    'province',
    'date',
    'Retail and Recreation',
    'Grocery and Pharmacy',
    'Parks',
    'Transit stations',
    'Workplaces',
    'Residential'
]

# get working directory
#working_path = os.getcwd() # use for Jupyter
working_path = os.path.dirname(os.path.abspath(__file__)) #use for .py scripts

# define url strings for default values in function
cases_url_str = "https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_confirmed.csv"
deaths_url_str = "https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_deaths.csv"
recoveries_url_str = "https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_recoveries.csv"
mobility_url_str = "https://raw.githubusercontent.com/dsfsi/covid19za/master/data/mobility/google_mobility/mobility_report_ZA.csv"

# define map file name
map_file = '/south_africa_administrative_state_province_boundary_edited.geojson'

# Function for retrieving CSVs from online source
def retrieve_data(url_str):
    req = requests.get(url_str).content.decode("utf-8")
    df = pd.read_csv(io.StringIO(req))
    return(df)

# Function for calculating difference between top and bottom of cumulative dataframe
def delta_estimate(x):
    return pd.Series(index=['delta_infected'],data=[((x.max()+x.tail(2).mean())/2)-((x.min()+x.head(2).mean())/2)])

# Import necessary data
prov_keys_df = pd.read_csv(working_path+'/province_pop.csv', index_col='province')
cases_df = retrieve_data(cases_url_str)
deaths_df = retrieve_data(deaths_url_str)
recoveries_df = retrieve_data(recoveries_url_str)
mobility_df = retrieve_data(mobility_url_str)

def stats_get(cases_df=cases_df, deaths_df=deaths_df, recoveries_df=recoveries_df, mobility_df=mobility_df, prov_keys_df=prov_keys_df, day_window_size=7):
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

def map_get(file_name=map_file):
    with open(working_path+file_name) as json_file:
        geojson_za = json.load(json_file)
    return geojson_za

def za_stats_get():
    df = stats_get()
    rsa_means = df[['population_density', 'norm_delta_cases', 'window_avg_mobility', 'avg_infected_per_area', 'infection_prob']].mean()
    rsa_sums = df[['population', 'area', 'window_infected_count']].sum()
    rsa_stats_df = pd.DataFrame(rsa_sums.append(rsa_means), columns=['Values']).round(3)
    rsa_stats_df['RSA COVID Statistics'] = ['Population size', 'Area (Square km)', 'Current Active Carriers', 'Population Density', 'Current Estimated Slope of Carrier Growth', 'Mobility of Citizens (0.5=Normal)', 'Carriers per Square km', 'Estimated Probability of Infection (EPI)']
    rsa_stats_df = rsa_stats_df[['RSA COVID Statistics', 'Values']]
    return rsa_stats_df

def mobility_get(url=mobility_url_str):
    df = retrieve_data(url)
    df[df.columns[2:]] = (df[df.columns[2:]]+100)/200
    df['province'] = pd.Categorical(df['province'], categories=prov_name_lst, ordered=True)
    df = df.sort_values(['date','province'])
    df['date'] = pd.to_datetime(df['date'],format="%Y-%m-%d")
    df.columns = mob_name_lst
    return df

def covid_data_get():
    # retrieve data from github
    cases_df = retrieve_data(cases_url_str)
    deaths_df = retrieve_data(deaths_url_str)
    recoveries_df = retrieve_data(recoveries_url_str)
    prov_keys_df = pd.read_csv(working_path+'/province_pop.csv', index_col='province')
    prov_keys_dict = prov_keys_df.population.to_dict()
    # remove columns that arent needed
    cases_clean_df = cases_df.drop(['YYYYMMDD','UNKNOWN','source'],axis=1)
    death_clean_df = deaths_df.drop(['YYYYMMDD','UNKNOWN','source'],axis=1)
    recov_clean_df = recoveries_df.drop(['YYYYMMDD','UNKNOWN','source'],axis=1)
    # melt dataframes
    covid_df = cases_clean_df.melt('date', var_name='province', value_name='Cumulative Cases')
    death_long_df = death_clean_df.melt('date', var_name='province', value_name='Cumulative Deaths')
    recov_long_df = recov_clean_df.melt('date', var_name='province', value_name='Cumulative Recoveries')
    # Merge dataframes into one
    covid_df = pd.merge(covid_df, death_long_df,  how='left', left_on=['date','province'], right_on = ['date','province'])
    covid_df = pd.merge(covid_df, recov_long_df,  how='left', left_on=['date','province'], right_on = ['date','province'])
    # replace province short names with full ones
    covid_df = covid_df.replace({'province':prov_name_dict})
    covid_df['province'] = pd.Categorical(covid_df['province'], categories=prov_name_lst, ordered=True)
    # Calculate more columns of information
    covid_df['Daily Active Cases'] = covid_df['Cumulative Cases']-(covid_df['Cumulative Deaths']+covid_df['Cumulative Recoveries'])
    covid_df['Daily New Cases'] = covid_df['Cumulative Cases'].diff()
    mask = covid_df['Daily New Cases'] < 0
    covid_df.loc[mask, 'Daily New Cases'] = 0
    covid_df['Daily Deaths'] = covid_df['Cumulative Deaths'].diff()
    covid_df['Daily Recoveries'] = covid_df['Cumulative Recoveries'].diff()
    # add population size column
    for i,j in prov_keys_dict.items():
        covid_df.loc[covid_df.province == i, ['population']] = j
    # Rescale cumulative cases to be per 1000 people
    covid_df['Cumulative Cases per 1000'] = (covid_df['Cumulative Cases']/covid_df['population'])*1000
    covid_df['Cumulative Deaths per 1000'] = (covid_df['Cumulative Deaths']/covid_df['population'])*1000
    covid_df['Cumulative Recoveries per 1000'] = (covid_df['Cumulative Recoveries']/covid_df['population'])*1000
    # convert date to datetime pandas
    covid_df['date'] = pd.to_datetime(covid_df['date'],format="%d-%m-%Y")
    return covid_df