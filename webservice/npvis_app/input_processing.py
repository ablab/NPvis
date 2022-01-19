import os

from .utils import readFile
from npvis.settings import DATA_PATH

def process_structure_input(request):
    outfile = os.path.join(DATA_PATH, 'Structure.mol')
    if request.POST['struct_input_type'] == 'smiles':
        smiles_str = request.POST['inputStructure']
        cmd = f'molconvert  mol:V3 -s "{smiles_str}" > {outfile}'
        os.system(cmd)
    elif request.POST['struct_input_type'] == 'mol':
        readFile(request.FILES['inputStructure'], outfile)

    return outfile