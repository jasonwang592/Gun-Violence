import pandas as pd

sg_df = pd.read_csv('files/state_gender.txt', sep = '\t')
sga_df = pd.read_csv('files/state_gender_age.txt', sep = '\t')

'''Cleaning up some redundant columns. Removed some rows where data had not been collected yet
Recalculating the rate per 100k'''
sg_df.drop(['Notes', 'Crude Rate','Gender Code', 'State Code', 'Year Code'], inplace = True, axis = 1)
sga_df.drop(['Notes', 'Crude Rate', 'Ten-Year Age Groups', 'Gender Code', 'State Code', 'Year Code'],
	inplace = True, axis = 1)

sga_df.rename(columns = {'Ten-Year Age Groups Code': 'Age Group'}, inplace = True)

sg_df.Year = sg_df.Year.astype(int).astype(str)
sg_df.Population = sg_df.Population.astype(float)
sga_df.Year = sga_df.Year.astype(int).astype(str)
sga_df.Population = sga_df.Population.astype(float)

sga_df['Rate'] = (sga_df.Deaths/sga_df.Population) * 100000
sg_df['Rate'] = (sg_df.Deaths/sg_df.Population) * 100000



