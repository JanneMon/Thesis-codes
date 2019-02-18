#!/bin/bash


for filename in LOGS/*.GYRE; do 
	LOGS/gyre_tofreqs_44tau.sh "$filename" -r
done 

