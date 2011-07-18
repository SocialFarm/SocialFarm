#!/bin/bash

USERNAME=socialfarm 
PASSWORD=success 

for app in scheduler info
do
    for view in $app/* 
    do
        if ! test -d $view
        then
            continue
        fi 
        vn=$(basename $view)
        #echo found directory $view
        if test -f $app/$vn/reduce.js
        then 
            ./register.py $USERNAME $PASSWORD $app $vn $app/$vn/map.js $app/$vn/reduce.js
        else
            ./register.py $USERNAME $PASSWORD $app $vn $app/$vn/map.js
        fi 
    done
done
