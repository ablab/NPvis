from django.shortcuts import render
import os
from npvis.settings import DATA_PATH
from .forms import UploadSpectStructForm
from .run_app import run_npvis

def readFile(in_file, out_filename):
    with open(out_filename, "wb") as fw:
        for chunk in in_file.chunks():
            fw.write(chunk)


def handle_form(request):
    form = UploadSpectStructForm(request.POST, request.FILES)
    print(request.FILES)
    print(request.POST)
    if form.is_valid():
        readFile(request.FILES['inputSpectrum'], os.path.join(DATA_PATH, 'Spectrum.mgf'))
        readFile(request.FILES['inputStructure'], os.path.join(DATA_PATH, 'Structure.mol'))


# Create your views here.
def main_page(request):
    script_str = ""
    if request.method == "POST":
        handle_form(request)
        script_str = run_npvis(os.path.join(DATA_PATH, 'Spectrum.mgf'), os.path.join(DATA_PATH, 'Structure.mol'))
    return render(request, 'npvis_app/main_page.html', {'npvis_script': script_str})
