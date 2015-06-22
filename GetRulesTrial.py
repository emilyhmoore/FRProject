import re
import csv

## create or open csv
filename = "rules.csv"
f = open(filename, "w+b")
writer = csv.writer(f)
headers=["Date","Agency", "SubAgency","RIN", "BILCOD", "FRDOC","SignatureDate","SignatoryName","SignatoryTitle", "ImportantDates", "Addresses", "ContactforFurtherInfo", "SubjectList", "Agency2", "Action", "Summary"]
writer.writerow(headers)


#open the file
file=open("FR-2010-09-03.xml")

##store lines in the file as a python list
lines=file.readlines()

##Find where the rules begin and end
ruleLocations=[]
ruleENDLocations=[]
for j in range(len(lines)):
	if re.search("<RULE>", lines[j])!=None:
		ruleLocations.append(j)
	if re.search("</RULE>", lines[j])!=None:
		ruleENDLocations.append(j)
	
##Put FR date in document
	
for m in range(len(ruleLocations)):
	stuffIWant=[]			
	stuffIWant.append("3Sept09")
	arule=lines[ruleLocations[m]:ruleENDLocations[m]]

	MultiLineItems=["<AGENCY", "<SUBAGY>","<RIN>", "<BILCOD>", "<FRDOC>","<DATED>","<NAME>","<TITLE>", "<DATES", "<ADD", "<FURINF", "<LSTSUB"]	
	MultiLineItemsEND=["</AGENCY", "</SUBAGY>","</RIN>", "</BILCOD>", "</FRDOC>","</DATED>","</NAME>","</TITLE>","</DATES", "</ADD", "</FURINF", "</LSTSUB"]
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
				stuffIWant.append(OneString)
		if any(TF)==False:
			stuffIWant.append("None")
		TF=[]
			
			
##get multi-line stuff where I only need the last line of the multiline
	LastLineItems=["<AGY>", "<ACT>", "<SUM>"]
	LastLineItemsEND=["</AGY", "</ACT>", "</SUM>"]		
	start=0 ##This will mark the start of the multi line string 
	end=0 ##And this will mark the end
	TF=[] #This will help me tell if the line type I need is there at all.
	for k in range(len(LastLineItems)):
		for j in range(len(arule)):
			TF.append(LastLineItems[k] in arule[j])
			if re.search(LastLineItems[k], arule[j])!=None:
				start=j
			if re.search(LastLineItemsEND[k], arule[j])!=None:
				end=j
				string=re.split("\s{2,}",arule[start:end][-1])[1]
				stuffIWant.append(string) ##append the last line
		if any(TF)==False:
			stuffIWant.append("None")
		TF=[]
		
##Removing extra white space now. Have to do this again in the part below because of the multistring aspect.			
	#new_list=[]
	##This splits the strings into parts
	#for j in range(len(stuffIWant)):
	#	new_list.append(re.split("\s{2,}",stuffIWant[j])) ##split by multiple white space characters

	##This flattens the list
	#stuffIWant=[item for sublist in new_list for item in sublist]

	#This removes blank list items.
	#while'' in stuffIWant:
	#	stuffIWant.remove('')
			
	
	writer.writerow(stuffIWant)
f.close()
