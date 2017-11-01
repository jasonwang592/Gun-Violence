import pandas as pd
import itertools

sg_df = pd.read_csv('files/state_gender.txt', sep = '\t')
sga_df = pd.read_csv('files/state_gender_age.txt', sep = '\t')

'''
* Filling DataFrame with all possible combinations of State, Year and Gender so we can infer some values
later during aggregation by taking the average there is missing data. Marking columns that were previously missing
so we can denote that on US map representation
* Cleaning up some redundant columns. Removed some rows where data had not been collected yet
Recalculating the rate per 100k
'''
all_years = [1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
all_genders = ['Male', 'Female']
all_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
	'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
	'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska',
	'Nevada', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
	'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
combined = [all_states, all_years, all_genders]
df1 = pd.DataFrame(columns = ['State', 'Year', 'Gender'], data=list(itertools.product(*combined)))

sg_df.drop(['Notes', 'Crude Rate','Gender Code', 'State Code', 'Year Code'], inplace = True, axis = 1)
sga_df.drop(['Notes', 'Crude Rate', 'Ten-Year Age Groups', 'Gender Code', 'State Code', 'Year Code'],
	inplace = True, axis = 1)

sga_df.rename(columns = {'Ten-Year Age Groups Code': 'Age Group'}, inplace = True)
sg_df = df1.merge(sg_df, how = 'left').fillna(0)
sg_df.Year = sg_df.Year.astype(int).astype(str)
sg_df.Population = sg_df.Population.astype(float)
sga_df.Year = sga_df.Year.astype(int).astype(str)
sga_df.Population = sga_df.Population.astype(float)

sga_df['Rate'] = (sga_df.Deaths/sga_df.Population) * 100000
sg_df['Rate'] = (sg_df.Deaths/sg_df.Population) * 100000
sg_df['Missing'] = sg_df['Deaths'] == 0



