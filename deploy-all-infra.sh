#! /bin/bash
while getopts i:o: flag
do
    case "${flag}" in
        i) infrafolder=${OPTARG};;
        o) outputfolder=${OPTARG};;
        esac
done

python3 $PWD/create_templates.py $PWD/$infrafolder $PWD/$outputfolder

echo "Deploying from folder: $outputfolder"
for file in $PWD/$outputfolder/*.json
do
    base=$(basename $file)
    stackname=${base%%.*};
    aws cloudformation deploy --template-file $file --stack-name $stackname  --capabilities CAPABILITY_IAM
done