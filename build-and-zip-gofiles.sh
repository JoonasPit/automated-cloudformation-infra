#! /bin/bash

lambdafolder="$PWD/lambdas/scripts"
zipfolder="$PWD/lambdas/zips"

for folder in $lambdafolder/*
do
    for file in "$folder/*.go"
    do
        cd $folder
        base=$(basename $file)
        gobuildname=${base%%.*};   
        GOOS=linux GOARCH=amd64 go build -o $folder/$gobuildname $folder/$base 
        zip $gobuildname.zip $folder/$gobuildname
        mv "$folder/$gobuildname.zip" $zipfolder
    done
done