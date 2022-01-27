import os

from .utils import readFile
from .utils import get_or_create_session
from npvis.settings import DATA_PATH
from npvis.settings import NPVIS_SCRIPT_PATH

def process_spectrum_input(request):
    user_session = get_or_create_session(request)

    outfile = os.path.join(DATA_PATH, user_session, 'Spectrum.mgf')
    scanID = 0
    if request.POST['ms_input_type'] == "mgf":
        filename = request.FILES['inputSpectrum'].name
        outfile = os.path.join(DATA_PATH, user_session, 'Spectrum.' + filename.split('.')[-1])
        readFile(request.FILES['inputSpectrum'], outfile)
        scanID = request.POST["inputScanId"]
    elif request.POST['ms_input_type'] == "gusi":
        gusi = request.POST['inputSpectrum']
        #gusi.replace(':', '%3A')
        #gusi_url = "https://metabolomics-usi.ucsd.edu/json/?usi1=" + gusi
        #cmd = f'wget {gusi_url} -O {os.path.join(DATA_PATH, "Spectrum.json")}'
        cmd = f'python3 {os.path.join(NPVIS_SCRIPT_PATH, "usi2mgf.py")} --usi {gusi} > {outfile}'
        os.system(cmd)

    return outfile, scanID

def process_structure_input(request):
    user_session = get_or_create_session(request)

    outfile = os.path.join(DATA_PATH, user_session, 'Structure.mol')
    if request.POST['struct_input_type'] == 'smiles':
        smiles_str = request.POST['inputStructure']
        cmd = f'molconvert  mol:V3 -s "{smiles_str}" > {outfile}'
        os.system(cmd)
    elif request.POST['struct_input_type'] == 'mol':
        readFile(request.FILES['inputStructure'], outfile)

    return outfile


def process_error_thr(request):
    error_thr = float(request.POST['error_thr'])
    error_type = request.POST['error_type']

    print(error_thr, error_type)

    return error_thr, error_type