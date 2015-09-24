
		##Maybe save SUPLINF as a separate note pad document <SUPLINF
		day=re.split(".xml",days[i])[0]
		title=[day]
		title.append(str(i))
		title.append(".txt")
		title=' '.join(title)
		textf = open(title, "w")
	
		start=0
		end=0
		for j in range(len(arule)):
			if re.search("<SUPLINF", arule[j])!=None:
				start=j
			if re.search("</SUPLINF", arule[j])!=None:
				end=j

		for l in arule[start:end]:
			textf.write(l)
		
		textf.close()
		
		
##Multiple Occurances
##MultipleOccItems=["<PRTPAGE", "<CFR>"]
##For Printed page, I only need the first iteration and the last. For CFR I only need the first.
