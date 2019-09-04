import quandl, datetime, csv
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf
from pandas.plotting import register_matplotlib_converters

def get_data(start_date, end_date, code): #retrives the data
	sma_start_date= start_date - datetime.timedelta(days= 200)
	data= quandl.get(code, start_date= start_date.isoformat(), end_date= end_date.isoformat()) # need to change the WIKI/AAPL for different firms
	return data

def inter_3keys(key1, key2, key3): #gets the intersections of 3 keys
	keys= []
	for item in key1:
		if item in key2 and item in key3:
			keys.append(item)
	return keys

def inter_2keys(key1, key2): #gets the intersections of 2 keys
	keys= []
	for item in key1:
		if item in key2:
			keys.append(item)
	return keys

def average(datas, keys):
	data= {"Open": {}, "Close": {}}
	for key in keys:
		d0 =datas[0].loc[key, ["Open", "Close"]]
		d1= datas[1].loc[key, ["Open", "Close"]]
		d2= datas[2].loc[key, ["Open", "Close"]]
		open= (d0["Open"] + d1["Open"] + d2["Open"])/3
		close= (d0["Close"] + d1["Close"] + d2["Close"])/3

		data["Open"][key]= open
		data["Close"][key]= close
	return data

def main():
	API_key=""
	quandl.save_key(API_key) #API KEY
	#print(quandl.ApiConfig.api_key)

	start_date_str= "2001-12-31"
	end_date_str= "2018-12-31"
	start_date= datetime.date.fromisoformat(start_date_str)
	end_date= datetime.date.fromisoformat(end_date_str)
	register_matplotlib_converters()

	data1= []
	data1.append(get_data(start_date, end_date, "EOD/GOOGL")) #Google
	data1.append(get_data(start_date, end_date, "EOD/AAPL")) #Apple
	data1.append(get_data(start_date, end_date, "EOD/MSFT")) #Microsoft

	keys1= inter_3keys(data1[0].index.tolist(),data1[1].index.tolist(),data1[2].index.tolist())
	av1= average(data1, keys1)

	data2= []
	data2.append(get_data(start_date, end_date, "EOD/TM"))
	data2.append(get_data(start_date, end_date, "EOD/GM"))
	data2.append(get_data(start_date, end_date, "EOD/F"))

	keys2= inter_3keys(data2[0].index.tolist(),data2[1].index.tolist(),data2[2].index.tolist())
	av2= average(data2, keys2)

	inter= {}
	interkeys= []
	with open('INTDSRUSM193N.csv', 'r') as csvFile:
	    reader = csv.reader(csvFile)
	    for row in reader:
	    	if row[0]!="DATE":
	    		key= pd.Timestamp(row[0])
	    		inter[key]= float(row[1])
	    		interkeys.append(key)

	keyx1= inter_2keys(interkeys, keys1)
	keyx2= inter_2keys(interkeys, keys2)

	interest1= [ (av1["Close"][key] - av1["Open"][keyx1[0]])/av1["Open"][keyx1[0]] for key in keyx1]
	interest2= [ (av2["Close"][key] - av2["Open"][keyx2[0]])/av2["Open"][keyx2[0]] for key in keyx2]

	# plt.plot(keys1, interest1, keys2, interest2)
	# plt.show()

	# print(keyx)
	df1= pd.DataFrame({"x": interest1, "y": [ inter[key] for key in keyx1]})
	mod1 = smf.ols('y ~ x', data=df1)
	res1 = mod1.fit()
	print(res1.summary())

	df2= pd.DataFrame({"x": interest2, "y": [ inter[key] for key in keyx2]})
	mod2 = smf.ols('y ~ x', data=df2)
	res2 = mod2.fit()
	print(res2.summary())

if __name__ == '__main__':
	main()
