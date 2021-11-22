# Tappity file JSON to CSV converter

This package converts tappit json files to 

## Install

git clone https://github.com/NickMortimer/tappity.git

move to directory

conda env create -f environment.yml

conda activate tappity

pip install .

example code 
```
import pandas as pd
import tappity
import os
import glob



files = glob.glob('./data/*.json')
for file in files:
    data = tappity.process_data(file)
    file = os.path.splitext(file)[0]+'.csv'
    data.to_csv(file)
```

Please note the file names must have the following convention

TAPPITY_NDR2019_3017_20190330T031612.json

this format

TAPPITY_{voyage}_{station/operation}_2019033003T1612.json


