from django.http import HttpResponse
from django.shortcuts import render
import os
from npvis.settings import DATA_PATH
from .run_app import run_npvis
from .run_app import run_npvis_inline
from .utils import get_or_create_session
from .utils import clear_session_dir
from .input_processing import process_structure_input
from .input_processing import process_spectrum_input

def handle_form(request):
    print(request.FILES)
    print(request.POST)

    spectrum_in = process_spectrum_input(request)
    struct_in = process_structure_input(request)

    return spectrum_in, struct_in


# Create your views here.
def main_page(request):
    script_str = ""
    if request.method == "POST":
        clear_session_dir(request)
        spect_in, struct_in = handle_form(request)
        script_str = run_npvis(spect_in, struct_in)

    return render(request, 'npvis_app/main_page.html', {'npvis_script': script_str})


def downloadreport(request):
    user_session = get_or_create_session(request)
    print("User session:", user_session)

    file_path = run_npvis_inline(os.path.join(DATA_PATH, user_session, 'Spectrum.mgf'), os.path.join(DATA_PATH, user_session, 'Structure.mol'))
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
