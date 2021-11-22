import pandas as pd
import tappity
import os
import glob



files = glob.glob('./data/*.json')
for file in files:
    data = tappity.process_data(file)
    file = os.path.splitext(file)[0]+'.csv'
    data.to_csv(file)
