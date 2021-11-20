from os import path, listdir
from pathlib import Path
import subprocess
import sys

infra_directory = sys.argv[1]
output_directory =sys.argv[2]

for file in listdir(infra_directory):
   json_filename = path.basename(f"{infra_directory}/{file}").split('.')[0]
   with open(f"{output_directory}/{json_filename}.json", "w") as output:
      subprocess.call(["python3", f"{infra_directory}/{file}"], stdout=output);