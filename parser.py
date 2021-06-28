import xml.dom.minidom
import mysql.connector

toParse = xml.dom.minidom.parse("uscases.xhtml")
states = ["New York", "New Jersey", "Massachusetts", "Illinois", "California", "Pennsylvania", "Michigan", "Florida", "Texas", "Connecticut", "Louisiana", "Georgia", "Maryland", "Indiana", "Ohio", "Virginia", "Colorado", "Washington", "Tennessee", "North Carolina", "Iowa", "Rhode Island", "Arizona", "Missouri", "Winsconsin", "Mississippi", "Alabama", "Minnesota", "South Carolina", "Nebraska", "Nevada", "Kansas", "Utah", "Delaware", "Kentucky", "Oklahoma", "New Mexico", "Arkansas", "Oregon", "South Dakota", "New Hampshire", "Idaho", "North Dakota", "West Virginia", "Maine", "Vermont", "Hawaii", "Wyoming", "Montana", "Wisconsin", "Alaska"]
stateList = []
valueList = []

# Parse XHTML to get order of states and their values
stateElements = toParse.getElementsByTagName("a")
valueElements = toParse.getElementsByTagName("td")
# Get list of states from table
for a in stateElements:
	if(a.getAttribute("class") == "mt_a"):
		for data in a.childNodes:
			# Check if data is a text node and isn't just whitespace
			if data.nodeType == data.TEXT_NODE and not data.nodeValue.isspace():
				stateList.append(data.nodeValue.strip())
# Get number values from table
for td in valueElements:
	if(td.getAttribute("colspan") == "1" and td.getAttribute("rowspan") == "1" and "font-weight: bold" in td.getAttribute("style")):
		for data in td.childNodes:
			# Check if data is a text node and isn't just whitespace
			if data.nodeType == data.TEXT_NODE and not data.nodeValue.isspace():
				# Check if text has a digit
				digits = False
				for char in data.nodeValue:
					if char.isdigit():
						digits = True
						break
				# Add value to element list if it's a number or N/A
				if digits == True or data.nodeValue.strip() == "N/A":
					valueList.append(data.nodeValue.strip())

# Connect to database
connection = mysql.connector.connect(host="localhost", database="us_covid_cases", user="root", password="mypassword")
cursor = connection.cursor()

# Copy current data to old data
copycmd = "UPDATE us SET oldcases = cases;"
cursor.execute(copycmd)
copycmd = "UPDATE us SET olddeaths = deaths;"
cursor.execute(copycmd)

# Narrow down data to only values we're looking for (confirmed cases and deaths)
i = 0
stateidx = 0
sqlcmd = ""
caseList = []
deathList = []
while i < 310:
	cases = ""
	deaths = ""
	# Narrow down values to total confirmed cases and total confirmed deaths
	casesStr = valueList[i]
	if "+" in valueList[i + 1]:
		i = i + 1
	deathsStr = valueList[i + 1]
	i = i + 1
	if "+" in valueList[i + 1]:
		i = i + 1
	i = i + 5
	
	# Get rid of commas from numbers
	for char in casesStr:
		if char != ",":
			cases = cases + char
	for char in deathsStr:
		if char != ",":
			deaths = deaths + char
	
	# If state is valid, add to list of values
	if(stateList[stateidx] in states):
		caseList.append(cases)
		deathList.append(deaths)
	else:
		# Remove invalid states
		stateList.remove(stateList[stateidx])
		continue
	stateidx = stateidx + 1

# Update the current data with the new data
for i in range (0, 50):
	sqlcmd = "UPDATE us SET cases = %(cases)s, deaths = %(deaths)s WHERE state = %(state)s;"
	cursor.execute(sqlcmd, {'cases': int(caseList[i]), 'deaths': int(deathList[i]), 'state': stateList[i]})
	connection.commit()
connection.close()
