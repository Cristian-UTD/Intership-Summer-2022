#!/bin/bash

cd /home/baumdev/Practica/1.Texte

for x in {1..10} 
do
if [[ $(($x+2)) == 3 || $(($x+2)) == 6 || $(($x+2)) == 9  ]]
then
mv -v $x.txt apartament$x.txt
else
mv -v $x.txt casa$x.txt
fi
done 

for y in 1 4 7 
do
mv -v apartament$y.txt .apartament$y.txt
done

rm -v -r *

for i in 1 4 7 
do
mv -v .apartament$i.txt apartament$i.txt
done
