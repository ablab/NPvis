import shutil

from django.http import HttpResponse
from django.shortcuts import render
import os
import time
from npvis.settings import DATA_PATH
from .run_app import run_npvis
from .run_app import run_npvis_inline
from .utils import get_or_create_session
from .utils import clear_session_dir
from .input_processing import process_structure_input
from .input_processing import process_spectrum_input
from .input_processing import process_error_thr
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
    if request.method == "POST":
        clear_session_dir(request)
        spect_in, scanId, struct_in, error_thr, error_type, mode_type = handle_form(request)
        print(spect_in, scanId, struct_in, error_thr, error_type)
        script_str = run_npvis(spect_in, scanId, struct_in, error_thr, error_type, mode_type, user_session)
    if request.method == "GET" and ("gusi" in request.GET):
        spect_in, scanId, struct_in, error_thr, error_type, mode_type = process_get(request)
        print(spect_in, scanId, struct_in, error_thr, error_type)
        script_str = run_npvis(spect_in, scanId, struct_in, error_thr, error_type, mode_type, user_session)

    return render(request, 'npvis_app/main_page.html', {'npvis_script': script_str})


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
