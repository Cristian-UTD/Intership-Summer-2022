#!/bin/bash 

mv -v 1.txt .1.txt
mv -v 2.txt .2.txt
mv -v 3.txt .3.txt

rm -v -r *

mv -v .1.txt 1.txt
mv -v .2.txt 2.txt
mv -v .3.txt 3.txt
