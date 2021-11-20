#! /bin/bash
cd "$(dirname "$0")"
while getopts t:j: flag
do
    case "${flag}" in
        t) templatecreation=${OPTARG};;
        j) jsonfolder=${OPTARG};;
        esac
done

echo "Creating templates from $templatecreation"
python3 $PWD/$templatecreation.py

echo "Deploying from folder: $jsonfolder"
for file in $PWD/$jsonfolder/*.json
do
    base=$(basename $file)
    stackname=${base%%.*};
    aws cloudformation deploy --template-file $file --stack-name $stackname 
done