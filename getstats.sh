#!/bin/bash

while true
do
	# Get sources as argument, convert html to xhtml, and run through parser
	filename="$1"
	ussourcetaken=false
	while IFS= read -r file; do
		if [ "$ussourcetaken" != true ]; then
			ussource=$file
			ussourcetaken=true
		else
			njsource=$file
		fi
	done < "$filename"
	
	echo $ussource
	echo $njsource
	
	curl -o uscases.html https://www.worldometers.info/coronavirus/country/us/
	curl -o njcases.html https://www.worldometers.info/coronavirus/usa/new-jersey/
	java -jar tagsoup-1.2.1.jar --files uscases.html
	java -jar tagsoup-1.2.1.jar --files njcases.html
	python3 parser.py

	# Cleaning up spare files
	rm uscases.html uscases.xhtml njcases.html njcases.xhtml
	sleep 1800
done
