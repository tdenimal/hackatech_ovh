#!/bin/bash

#Quick and dirty script to launch parallel extracts

for f in $(cat companies_url.txt); do
	docker run --detach --mount type=bind,source="$(pwd)"/scrap_data,target=/scrap_data scrap_hackhaton $f
	while [ $(docker ps -q --filter "ancestor=scrap_hackhaton" | wc -l) -gt "30" ]; do
		echo Waiting
		sleep 10
	done
	echo $f
done
