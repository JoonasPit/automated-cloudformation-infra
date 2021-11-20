#! /bin/bash
while getopts f:s:j: flag
do
    case "${flag}" in
        f) scriptfolder=${OPTARG};;
        s) script=${OPTARG};;
        j) cloudformation_infrastructure=${OPTARG};;
        esac
done
scripttorun=$PWD/$scriptfolder/$script
outputfolder=$PWD/$cloudformation_infrastructure
base=$(basename $scripttorun)
filerootname=${base%%.*};
filenameasjson="$filerootname.json"
python3 $scripttorun $filenameasjson $outputfolder
echo "Deploying from folder: $cloudformation_infrastructure"

aws cloudformation deploy --template-file "$PWD/$cloudformation_infrastructure/$filenameasjson" --stack-name $filerootname
