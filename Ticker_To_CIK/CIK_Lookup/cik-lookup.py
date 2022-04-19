import re, requests
headers = {"user-agent": "Safari"}
import pandas as pd
import time
import csv

t0 = time.time()

df = pd.read_csv('data.csv')
set_of_names = df['companyname'].to_list()

punc = '''!()-[]{};'"\,<>./?@#$%^&*_~'''

matcher = open('cik-lookup-data.txt', 'r')

data = matcher.read()

matcher_set = data.split("\n")



matcher.close

not_found = {}


#Remove punctuation from set of names
for names in range(len(set_of_names)):
	if(not(isinstance(set_of_names[names], float))):
		for ele in set_of_names[names]:
			if ele in punc:
				punc_removed = re.sub(r'[^\w\d\s\:]+', '', set_of_names[names])
		set_of_names[names] = punc_removed

	
	
#Remove punctuation from cik set of names	
for names in range(len(matcher_set)):
	if(not(isinstance(matcher_set[names], float))):
		for ele in matcher_set[names]:
			if ele in punc:
				punc_removed = re.sub(r'[^\w\d\s\:]+', '', matcher_set[names])
		matcher_set[names] = punc_removed

#print(set_of_names, "NAMES")
#print(matcher_set, "SET")

#time.sleep(2)

#Remove duplicates & makes it faster to access
set_of_names = set(set_of_names)	
matcher_set = set(matcher_set)

d = {}

#Split into dictionary w/ key being name and val being CIK
for item in matcher_set:
	#print(item)
	item = item.split(':')
	#print(len(item))
	#print(item)
	if(len(item) > 1):
		d[item[0]] = item[1]
#print(d.keys())


file = open("temp_dict","w")
counter = 0
for names in set_of_names:
	l = []
	for k, v in d.items():
		if(not(isinstance(names, float))):
			if(names.lower()) in k.lower():
				l.append([names, k.lower(), v])
			else:
				#print(names, "was not found") 
				pass
	if(len(l) > 0):
		for fax in l:
			#print(fax)
			file.write("[")
			file.write(" - ".join(fax))
			file.write("] ")
		file.write("\n")
	counter += 1
	if(counter % 100 == 0):
		t2 = time.time()
		print(counter/len(set_of_names) * 100, "% Complete --- Time Elapsed:", t2-t0, "seconds  --- " ,counter/(t2-t0), "requests/sec")
		
#file = open("temp_dict","w")
#for key, value in d.items(): 
#	file.write('%s:%s\n' % (key, value))
file.close()

t1 = time.time()
print("Total Time: ", t1-t0)

#file = open("cik_dict_2","w")
#for key, value in d.items(): 
#	file.write('%s:%s\n' % (key, value))
#file.close()

