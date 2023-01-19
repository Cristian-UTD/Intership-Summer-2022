#!/bin/bash

echo Ce fisier/e ati vrea sa stergeti ?
read x

rm $x 

echo _____________________________________________ >> Log.txt
echo " " >> Log.txt
echo [$(date)] A/au fost sters/e: $x ! >> Log.txt

