#!/bin/bash

echo -e "\n\nTime;Test Name;Test Number;Container;CPU %;MEM Usage;MEM Limit;NET Input;NET Output;Block Input;Block Output"

while :
do
	echo -n $(date '+%Y-%m-%d %H:%M:%S;')
	echo -n $2
	echo -n ";"
	echo -n $3
	
	docker stats --no-stream --format ";{{.Container}};{{.CPUPerc}};{{.MemUsage}};{{.NetIO}};{{.BlockIO}}" $1 | sed 's/ \/ /;/g'
	sleep 1
done
