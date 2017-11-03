def choropleth(year, gender, metric_name, chart_title, bar_title, output_folder):
	year = str(year)
	sg_df = sg_df.loc[(sg_df['Year'] == year) & (sg_df['Gender'] == gender)]

	scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
	        [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

	data = dict(type='choropleth',
	        locations = sg_df['State Code'],
	        locationmode ='USA-states',
	        z = sg_df[metic_name].astype(int),
			colorscale = scl,
			autocolorscale = False,
	        colorbar = dict(title = bar_title)
	        )

	layout = dict(
		geo = dict(scope='usa', projection = dict(type = 'albers usa'),
					showlakes= False),
		title = chart_title,
	         )

	choromap = go.Figure(data=[data], layout=layout)
	fname = year + gender + metric_name
	plot(choromap, image_filename = fname, image_width = 1200, image_height = 1000)
	# shutil.move(download_path + fname + '.png', output_path + fname + '.png')