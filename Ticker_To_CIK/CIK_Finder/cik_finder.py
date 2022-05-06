import re, requests
headers = {"user-agent": "Safari"}
import pandas as pd
import time
import csv

t0 = time.time()

valid_tickers = ["ARCA", "BATS", "NASDAQCM", "NASDAQGM", "NASDAQGS", "NYSE", "NYSEAM", "OTCEM", "OTCPK", "OTCQB", "OTCQX", "PSGM"]

def getCIKs(TICKERS, not_found):
	URL = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany' #EDGAR Website
	CIK_RE = re.compile(r'.*CIK=(\d{10}).*')
	cik_list = []
	counter = 0 #used to print progress
	for ticker in TICKERS:
		#Ticker is formatted in this way: ticker[0] is the Ticker and ticker[1] is the name of the company
		#print(ticker)
		#print("testing")
		if(ticker[0] == "UNQ/MISX"): #if ticker has been labeled UNQ/MISX, it means it doesn't exist in the EDGAR, we can skip
			continue
		#print(URL.format(ticker))
		time.sleep(0.01) #DO NOT REMOVE, fixes Connection error 104
		f = requests.get(URL.format(ticker[0]),headers= headers, stream = True) #inputs the current CIK (ticker[0])
		#print(f.text)
		results = CIK_RE.findall(f.text) #stores all text, results[0] always stores the name (or stores nothing if not found)
		#print(results)
		if len(results):
			results[0] = int(re.sub('\.[0]*', '.', results[0])) #modifies CIK and formats it into an int
			cik_list.append([str(ticker[0]).upper(), str(ticker[1]), str(results[0])]) #appends to our final list that we'll return
		else:
			cik_list.append([str(ticker[0]).upper(), str(ticker[1]), "NOT_FOUND"]) #if not found, append "NOT_FOUND" as the CIK result
			#print(cik_list[-1])
			#not_found[str(tickers[0]).upper()] = (";;;" + str(ticker[1]) + ";;;" + "NOT_FOUND")
			#print("not found")
		
		counter += 1
		if(counter % 100 == 0): #simple counter to track progress and make sure the code isn't working
			t2 = time.time()
			print("(",counter,"/",len(TICKERS),")", " --- ", round(counter/len(TICKERS) * 100, 2), "% Complete --- Time Elapsed:", round(t2-t0, 2), "seconds  --- " ,round(counter/(t2-t0), 2), "requests/sec", " --- Time Left:", round((len(TICKERS)/(counter/(t2-t0)))/60, 2), "minutes")
	'''
	f = open('cik_dict', 'w')
	print(cik_dict)
	f.close()
	file = open("not_found","w")
	for key, value in not_found.items(): 
		file.write('%s:%s\n' % (key, value))
	file.close()
	'''
	return(cik_list) #returns list in format: [Ticker, Name, CIK from ticker]



df = pd.read_csv('data.csv') #reads csv
list_of_tickers = (df['exchangeticker'] + ";" + df['companyname']).to_list() #splits into list (; used because 

list_nyse_nasdaq = []
not_found = {}
f = open("not_found","w")
for tickers in list_of_tickers:
	#print(len(tickers))
	if not isinstance(tickers, float):
		tickers = tickers.split(';') #look at line 54 (list_of_tickers = ...), we put in the ';' to split easier
		#print(tickers)
		#time.sleep(0.5)
		#if(not(isinstance(tickers, float)) and ("NYSE" in tickers or "NASDAQGS" in tickers)): #temporary, only finds nyse and nasdaq tickers
		#print(list_of_tickers[i])
		#print(tickers)
		if(isinstance(tickers, float) or "UNQ" in tickers or "MISX" in tickers or ":" not in tickers[0]): #UNQ and MISX tickers need to be labeled separately
			not_found[str(tickers[0]).upper()] = "NOT_FOUND"
			list_nyse_nasdaq.append(["UNQ/MISX", tickers[1]])
			for x in tickers: #write everything to output file
				f.write(x)
				f.write(":")
			f.write("NOT_FOUND:NOT_FOUND:\n")			
			#print(tickers[1], "UNQ" in tickers, "MISX" in tickers, ":" not in tickers)
			#time.sleep(0.05)
		else: #else just append ticker[0] and ticker[1] to the list
			#print(tickers[0])
			#if valid_tickers (list) in tickers[0](string)
			#print(any(x in tickers[0] for x in valid_tickers))
			if(any(x in tickers[0] for x in valid_tickers)):
				list_nyse_nasdaq.append([tickers[0].split(":", 1)[1], tickers[1]])
			else:
				print("Invalid Ticker: ", tickers, " --- Not Added to Queue")
				not_found[str(tickers[0]).upper()] = "NOT_FOUND"
		
	
#print((list_nyse_nasdaq))
f.close()

print("DONE")
time.sleep(1)

print("Starting")
time.sleep(0.5)

punc = '''!()-[]{};'"\,<>./?@#$%^&*_~''' #for punctiation removal

matcher = open('cik-lookup-data.txt', 'r')

data = matcher.read()

matcher_list = data.split("\n")



matcher.close


punc_changed = False

tickers_removed_dupes = set()
dupe_count = 0
	
#Remove punctuation from set of names
for i in range(len(list_nyse_nasdaq)):
	#print(list_nyse_nasdaq[i])
	if(not(isinstance(list_nyse_nasdaq[i][1], float))):
		#print(list_nyse_nasdaq[i])
		punc_changed = False
		for ele in list_nyse_nasdaq[i][1]:
			if ele in punc:
				punc_changed = True
				punc_removed = re.sub(r'[^\w\d\s\:]+', '', list_nyse_nasdaq[i][1])
		#print(list_nyse_nasdaq[i])
		if(punc_changed == True):
			list_nyse_nasdaq[i][1] = punc_removed
			if (list_nyse_nasdaq[i][0], punc_removed) in tickers_removed_dupes:
				#print("Dupe Found")
				dupe_count += 1
				#time.sleep(1)
			tickers_removed_dupes.add((list_nyse_nasdaq[i][0], punc_removed))
		#print(list_nyse_nasdaq[i])
		else:
			tickers_removed_dupes.add((list_nyse_nasdaq[i][0], punc_removed))
		
		#print(list_nyse_nasdaq[i])
		#print(temp_set)

print("Done w/ punctuation changes & Dupe removal")
print(dupe_count, " Duplicate Tickers Removed")
print("Before: ", len(list_nyse_nasdaq), " --- After", len(tickers_removed_dupes))
	
#Remove punctuation from cik set of names in matcher list	
for i in range(len(matcher_list)):
	if(not(isinstance(matcher_list[i], float))):
		punc_changed = False
		for ele in matcher_list[i]:
			if ele in punc:
				punc_changed = True
				punc_removed = re.sub(r'[^\w\d\s\:]+', '', matcher_list[i])
		if(punc_changed == True):
			matcher_list[i] = punc_removed

#print(list_nyse_nasdaq)

#for x in list_nyse_nasdaq:
#	print(x)
#	time.sleep(0.25)


returned_info = getCIKs((tickers_removed_dupes), not_found) #get the CIK's from the ticker
#print(d)

#print(matcher_list)
d = {}
for item in matcher_list: #split into names and CIKs & store in dictionary
	#print(item)
	item = item.split(':')
	#print(len(item))
	#print(item)
	if(len(item) > 1):
		d[item[0]] = item[1]

counter = 0
f = open("out.txt","w")
for names in returned_info:
	#print(names)
	#time.sleep(0.5)
	cur_cik = ""
	for k, v in d.items(): #iterate through items of matcher_list
		if(not(isinstance(names, float))):
			if(names[1].lower()) in k.lower(): #if the name matches any matcher_list key
				#l.append([names[1], k.lower(), v])
				cur_cik = v
			else:
				#print(names, "was not found") 
				pass
	if(cur_cik != ""):
		names.append(cur_cik)
	else:
		names.append("NOT_FOUND")
	#print(names)
	for x in names: #write everything to output file
		f.write(x)
		f.write(":")
	f.write("\n")
	counter += 1
	if(counter % 100 == 0): #counter to keep track of progress
		t2 = time.time()
		print(counter/len(returned_info) * 100, "% Complete --- Time Elapsed:", t2-t0, "seconds  --- " ,counter/(t2-t0), "requests/sec")

for x in returned_info:
	#print(x[2], len(x[2]), x[3], len(x[3]))
	if(x[2] != "NOT_FOUND"):
		if (x[3] == "NOT_FOUND"):
			print("Discrepancy", x[2], x[3])
			continue
		else:
			if int(x[2]) != int(x[3]):
				print("Discrepancy", x[2], x[3])
			else:
				print("All good!")

	if(x[3] != "NOT_FOUND"):
		if (x[2] == "NOT_FOUND"):
			print("Discrepancy")
			continue
		else:
			if int(x[2]) != int(x[3]):
				print("Discrepancy", x[2], x[3])	
			else:
				print("All good!")

print(returned_info)

t1 = time.time()
print("Total Time: ", t1-t0)


'''
#Separate code for saving to CSV (Old)

file = open("cik_dict","w")
for key, value in d.items(): 
	file.write('%s:%s\n' % (key, value))
file.close()
'''

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
