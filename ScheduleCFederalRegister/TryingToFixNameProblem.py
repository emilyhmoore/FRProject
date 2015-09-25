import re
import csv

## create or open csv
filename = "TRYINGTOFIX.csv"
f = open(filename, "w+b")
writer = csv.writer(f)
headers=["Date","Agency", "SubAgency","RIN", "FRDOC","SignatureDate","SignatoryName","SignatoryTitle", "ImportantDates", "Addresses", "ContactforFurtherInfo", "SubjectList", "Agency2", "Action", "Summary"]
writer.writerow(headers)

#open the file
files=["FR-2010-09-13.xml"]
for file in files:
	thefile=open(file)
	##store lines in the file as a python list
	lines=thefile.readlines()
	##Find where the rules begin and end
	ruleLocations=[]
	ruleENDLocations=[]
	for j in range(len(lines)):
		if re.search("<RULE>", lines[j])!=None:
			ruleLocations.append(j)
		if re.search("</RULE>", lines[j])!=None:
			ruleENDLocations.append(j)
	
	##Put FR date in document
	stuffIWant=[]			
	stuffIWant.append(file)
	arule=lines[ruleLocations[4]:ruleENDLocations[4]]
	##There's a problem where BILCOD, NAME, and TITLE can have multiple iterations. Will need to extend to include multiple.
	MultiLineItems=["<AGENCY", "<SUBAGY>","<RIN>", "<FRDOC>","<DATED>","<NAME>","<TITLE>", "<DATES", "<ADD", "<FURINF", "<LSTSUB"]	
	MultiLineItemsEND=["</AGENCY", "</SUBAGY>","</RIN>", "</FRDOC>","</DATED>","</NAME>","</TITLE>","</DATES", "</ADD", "</FURINF", "</LSTSUB"]
	start=0
	end=0
	TF=[]
	for k in range(len(MultiLineItems)):
		for j in range(len(arule)):
			TF.append(MultiLineItems[k] in arule[j])
			if re.search(MultiLineItems[k], arule[j])!=None:
				start=j
			if re.search(MultiLineItemsEND[k], arule[j])!=None:
				end=j
			string=arule[start:(end+1)]
			##This strips out extra spacing
			new_list=[]
			for n in range(len(string)):
				new_list.append(re.split("\s{2,}",string[n]))
			new_list=[item for sublist in new_list for item in sublist]
			while'' in new_list:
				new_list.remove('')
			##
			OneString=" ".join(new_list) #Because I want multiple bits of information, I make it one string so it's one cell
			stuffIWantAsOne=" ".join(OneString)
			count=stuffIWantAsOne.count(MultiLineItems[k])
			joined=" ".join(OneString[-count:])
			del OneString[-count:]
			OneString.append(joined)
			stuffIWant.append(OneString)
			
		if any(TF)==False:
			stuffIWant.append("None")
		TF=[]
		stuffIwant=[]
			
		writer.writerow(stuffIWant)
f.close()