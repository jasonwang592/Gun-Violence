import pandas as pd
import itertools
import plotly.graph_objs as go
import visualization as vs
import sys

# Fill in below with proper paths:
#     download_path = Directory where browser downloads plots from plotly into
#     output_path = Directory where output files are stored
download_path = '/Users/jason.wang/Downloads/'
output_path = '/Users/jason.wang/Documents/Analytics Projects/Gun Control/output/'

main_df = pd.read_csv('files/state_gender.txt', sep = '\t')

# * Filling DataFrame with all possible combinations of State, Year and Gender so we can infer some values
# later during aggregation by taking the average there is missing data. Marking columns that were previously missing
# so we can denote that on US map representation
# * Cleaning up some redundant columns. Removed some rows where data had not been collected yet
# Recalculating the rate per 100k
all_years = [1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
all_genders = ['Male', 'Female']
all_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
	'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
	'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska',
	'Nevada', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
	'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
state_map = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}
inverted = {state:abbrev for abbrev,state in state_map.items()}
combined = [all_states, all_years, all_genders]
df1 = pd.DataFrame(columns = ['State', 'Year', 'Gender'], data=list(itertools.product(*combined)))

#Drop some useless data and left merge so we don't have missing keys on year and state
main_df.drop(['Notes', 'Crude Rate','Gender Code', 'Year Code', 'State Code'], inplace = True, axis = 1)
main_df = df1.merge(main_df, how = 'left').fillna(0)

#Use District of Columbia to hold dummy data about the max Death value for each gender so
#colorbar in choropleth is consistent
main_df.loc[(main_df['State'] == 'District of Columbia') & (main_df['Gender'] == 'Male'),['Deaths']]\
    = max(main_df[main_df['Gender'] == 'Male']['Deaths'])
main_df.loc[(main_df['State'] == 'District of Columbia') & (main_df['Gender'] == 'Female'),['Deaths']]\
    = max(main_df[main_df['Gender'] == 'Female']['Deaths'])


#Populate State Code and compute firearm death rate
main_df['State Code'] = main_df['State'].map(inverted)
main_df.Year = main_df.Year.astype(int).astype(str)
main_df.Population = main_df.Population.astype(float)
main_df['Rate'] = (main_df['Deaths'] / main_df['Population']) * 100000
main_df['Missing'] = (main_df['Deaths'] == 0)
main_df = main_df[['State', 'State Code', 'Year', 'Gender', 'Deaths', 'Population', 'Rate', 'Missing']]

#Heatmap analysis of trends
#Filter out any states that don't have complete data
#Calculate percent change in deaths since base year of 1999
complete_df = main_df.groupby(['State', 'Gender']).filter(lambda x: x['Rate'].isnull().sum() < 1).copy()
complete_df = complete_df[complete_df['State'] != 'District of Columbia']
complete_df['Net Percent Change'] = complete_df.groupby(['State', 'Gender'])['Rate'].apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))
complete_df['Rolling Percent Change'] = complete_df.groupby(['State', 'Gender'])['Rate'].pct_change() * 100
trend_df = complete_df.sort_values(by = ['State', 'Gender', 'Year'])


for gender in ['Male', 'Female']:
    vs.scatterLine(complete_df, 'Male', 'Rolling Percent Change')

# for gender in ['Male', 'Female']:
#   for metric in ['Net Percent Change', 'Rolling Percent Change']:
#     vs.heatmapper(trend_df, gender, metric)

sys.exit()
#Choropleth analysis by State, Year and Gender
year_list = list(main_df['Year'].unique())
gender_list = ['Male' , 'Female']
split_gender = True
metric = 'Rate'
metric_dir = output_path + metric + '/'
gender_list = ['Female']
for year in year_list:
    if split_gender:
        for gender in gender_list:
            output_dir = metric_dir + gender + '/'
            vs.choropleth(main_df, year, gender, metric, download_path, output_dir)
    else:
        output_dir = metric_dir + 'Combined/'
        vs.choropleth(main_df, year, gender_list, metric, download_path, output_dir)