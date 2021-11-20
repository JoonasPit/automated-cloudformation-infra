from os import path, listdir
from pathlib import Path
import subprocess
import sys

template_dir = sys.argv[1]

for file in listdir(template_dir): 
   json_filename = path.basename(f"{template_dir}/{file}").split('.')[0]
   subprocess.run(["python3", f"{template_dir}/{file}", f"{json_filename}.json"])