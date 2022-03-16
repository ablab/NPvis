import shutil

from django.http import HttpResponse
from django.shortcuts import render
import os
import time
from npvis.settings import DATA_PATH
from .forms import NPvisForm
from .run_app import run_npvis
from .run_app import run_npvis_inline
from .utils import get_or_create_session
from .utils import clear_session_dir
from .input_processing import handle_form
from .input_processing import process_get

def clear_unused_folders():
    clearlist = []
    for dirname in os.listdir(DATA_PATH):
        dn = os.path.join(DATA_PATH, dirname)
        if os.path.isdir(dn):
            mtime = os.path.getmtime(dn)
            ctime = time.time()
            print("Modified time:",  (ctime - mtime)/60)
            if (ctime - mtime)/60 > (7*24*60):
                clearlist.append(dn)

    for dn in clearlist:
        shutil.rmtree(os.path.join(DATA_PATH, dn))


# Create your views here.
def main_page(request):
    clear_unused_folders()

    user_session = get_or_create_session(request)

    script_str = ""
    mode_type = "PNP"
    ms_input_type = "mgf"
    struct_input_type = "mol"
    error_type = "absolute"
    error_thr = 0.03
    adduct_type = "H"
    charge_val = 1
    input_struct = ""
    input_spectrum = ""
    scanId = 0
    compound_name = ""

    if request.method == "POST":
        clear_session_dir(request)

        ms_input_type = request.POST['ms_input_type']
        struct_input_type = request.POST['struct_input_type']
        input_struct = request.POST['smiles'] if 'smiles' in request.POST else ""
        input_spectrum = request.POST['gusi'] if 'gusi' in request.POST else ""
        adduct_type = request.POST['adduct_type']
        charge_val = request.POST['charge_val']
        compound_name = request.POST['compound_name']

        spect_in, scanId, struct_in, error_thr, error_type, mode_type = handle_form(request)
        print(spect_in, scanId, struct_in, error_thr, error_type)
        script_str = run_npvis(spect_in, scanId, struct_in, error_thr, error_type, mode_type, adduct_type, charge_val, user_session)

        form = NPvisForm(request.POST, request.FILES)
        form.save_json(os.path.join(DATA_PATH, user_session, "form.json"))

    if request.method == "GET" and ("gusi" in request.GET):
        ms_input_type = "gusi"
        struct_input_type = "smiles"
        input_struct = request.GET["smiles"]
        input_spectrum = request.GET["gusi"]

        spect_in, scanId, struct_in, error_thr, error_type, mode_type = process_get(request)
        print(spect_in, scanId, struct_in, error_thr, error_type)
        script_str = run_npvis(spect_in, scanId, struct_in, error_thr, error_type, mode_type, adduct_type, charge_val, user_session)

        form = NPvisForm(request.GET, request.FILES)
        form.save_json(os.path.join(DATA_PATH, user_session, "form.json"))

    return render(request, 'npvis_app/main_page.html', {'npvis_script': script_str,
                                                        'mode_type': mode_type,
                                                        'ms_input_type': ms_input_type,
                                                        'input_spectrum': input_spectrum,
                                                        'struct_input_type': struct_input_type,
                                                        'input_struct': input_struct,
                                                        'scanid': scanId,
                                                        'error_type': error_type,
                                                        'error_thr': error_thr,
                                                        'adduct_type': adduct_type,
                                                        'charge_val': charge_val,
                                                        'compound_name': compound_name})


def downloadreport(request):
    user_session = get_or_create_session(request)
    print("User session:", user_session)

    file_path = run_npvis_inline(os.path.join(DATA_PATH, user_session, 'Spectrum.mgf'), os.path.join(DATA_PATH, user_session, 'Structure.mol'), user_session)
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response


def help_page(request):
    return render(request, 'npvis_app/help.html')
