import re, requests
import pandas as pd
import time
import csv
import pickle

t0 = time.time()

'''
chunksize = 10 ** 6
count = 0
for chunk in pd.read_csv('log.csv', chunksize=chunksize):
	#print(chunk['ip'])
	#time.sleep(1)
	count += 1
print(count)
time.sleep(5)
'''



df = pd.read_csv('data.csv')
set_of_names = df[['sp_entity_name', 'sp_address1', 'sp_address2', 'sp_zip', 'sp_location']]

name_dict = {}
address_dict = {}

temp_list_name = []
temp_list_address = []

cur_orgID = ""
cur_org = ""
cur_street = ""
cur_city = ""

with open('arin_db.txt','r') as data_file:
	for line in data_file:
		
		data = line.split(':')
		if(len(data) == 2):
			#print(data[0].strip()," : " , data[1].strip())
			d = data[0].strip()

			if d == "OrgID":
				cur_orgID = (data[1].strip())
			if d == "OrgName":
				d_first = data[1].strip()
				d_first = list(filter(None, data[1].split(" ")))
				#print(d_first[0].strip(), ": D First")
				cur_org = (d_first[0].strip())
			if d == "Street":
				cur_street = (data[1].strip())
			if d == "City":
				cur_city = (data[1].strip())		
				name_dict[cur_street] = [cur_orgID, cur_org, cur_city]
	

#ADD LATER, SAVED DICT PKL DUMPS (not compatible w/ for loop below becuase keyerrors, need to fix)
		
#with open('name_dict.pkl', 'wb') as f:
#    pickle.dump(name_dict, f)

#with open('name_dict.pkl', 'rb') as f:
#    loaded_dict = pickle.load(f)


for i in range(len(set_of_names['sp_entity_name'])):
	if(not isinstance(set_of_names['sp_entity_name'][i], float)):
		names_first = (set_of_names['sp_entity_name'][i].strip().split(" "))
		#print(names_first[0].strip())
		if(names_first[0].strip() in name_dict.keys()):
			print(names_first, " : ", name_dict[names_first[0]], " FOUND")
		else:
			#print("Nope: ", names_first[0].strip())
			pass

