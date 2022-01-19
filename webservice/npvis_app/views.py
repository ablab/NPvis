from django.http import HttpResponse
from django.shortcuts import render
import os
from npvis.settings import DATA_PATH
from .run_app import run_npvis
from .run_app import run_npvis_inline
from .utils import readFile
from .input_processing import process_structure_input

def handle_form(request):
    print(request.FILES)
    print(request.POST)
    readFile(request.FILES['inputSpectrum'], os.path.join(DATA_PATH, 'Spectrum.mgf'))
    struct_in = process_structure_input(request)

    return os.path.join(DATA_PATH, 'Spectrum.mgf'), struct_in


# Create your views here.
def main_page(request):
    script_str = ""
    if request.method == "POST":
        spect_in, struct_in = handle_form(request)
        script_str = run_npvis(spect_in, struct_in)
    return render(request, 'npvis_app/main_page.html', {'npvis_script': script_str})


def downloadreport(request):
    file_path = run_npvis_inline(os.path.join(DATA_PATH, 'Spectrum.mgf'), os.path.join(DATA_PATH, 'Structure.mol'))
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
