#/webservice/npvis_app/run_app.py
from npvis.settings import DATA_PATH
from npvis.settings import NPVIS_PATH
import os

def run_npvis(in_spectrum, in_structure):
    os.system(f'python2.7 {NPVIS_PATH}/visualize.py  --mol {in_structure}  --ann {in_spectrum} --portable_html -o {DATA_PATH}/vis.html')
    return f'{DATA_PATH}/vis.html'
