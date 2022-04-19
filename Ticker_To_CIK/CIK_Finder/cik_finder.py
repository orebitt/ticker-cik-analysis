import re, requests
headers = {"user-agent": "Safari"}
import pandas as pd
import time
import csv

t0 = time.time()


def getCIKs(TICKERS, not_found):
	URL = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
	CIK_RE = re.compile(r'.*CIK=(\d{10}).*')    
	cik_dict = {}
	counter = 0
	for ticker in TICKERS:
		#print("testing")
		#print(URL.format(ticker))
		time.sleep(0.01) #DO NOT REMOVE, fixes Connection error 104
		f = requests.get(URL.format(ticker),headers= headers, stream = True)
		#print(f.text)
		results = CIK_RE.findall(f.text)
		#print(results)
		if len(results):
			results[0] = int(re.sub('\.[0]*', '.', results[0]))
			cik_dict[str(ticker).upper()] = str(results[0])
		else:
			cik_dict[str(ticker).upper()] = "NOT_FOUND"
			not_found[str(tickers).upper()] = "NOT_FOUND"
		
		counter += 1
		if(counter % 100 == 0):
			t2 = time.time()
			print(counter/len(TICKERS) * 100, "% Complete --- Time Elapsed:", t2-t0, "seconds  --- " ,counter/(t2-t0), "requests/sec")
	f = open('cik_dict', 'w')
	print(cik_dict)
	f.close()
	file = open("not_found","w")
	for key, value in not_found.items(): 
		file.write('%s:%s\n' % (key, value))
	file.close()
	
	return(cik_dict)



df = pd.read_csv('data.csv')
list_of_tickers = df['exchangeticker'].to_list()

list_nyse_nasdaq = []
not_found = {}

for tickers in list_of_tickers:
	#print(len(tickers))
	print(tickers)
	#if(not(isinstance(tickers, float)) and ("NYSE" in tickers or "NASDAQGS" in tickers)): #temporary, only finds nyse and nasdaq tickers
	#print(list_of_tickers[i])
	if(isinstance(tickers, float) or "UNQ" in tickers or "MISX" in tickers):
		not_found[str(tickers).upper()] = "NOT_FOUND"
	else:
		list_nyse_nasdaq.append(tickers.split(":", 1)[1])
	
print(len(list_nyse_nasdaq))
print(len(set(list_nyse_nasdaq)))



d = getCIKs(set(list_nyse_nasdaq), not_found)
print(d)


t1 = time.time()
print("Total Time: ", t1-t0)

file = open("cik_dict","w")
for key, value in d.items(): 
	file.write('%s:%s\n' % (key, value))
file.close()



'''
csv_columns = ['Ticker','CIK']
csv_file = "Ticker_CIK.csv"
try:
	with open(csv_file, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
		writer.writeheader()
		for data in d:
			print(data)
			#writer.writerow(data)
except IOError:
	print("I/O error")

# returns:
# {'WMT': '104169', 'AMZN': '1018724', 'NFLX': '1065280'}
'''
