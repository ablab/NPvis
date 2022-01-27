from npvis.settings import DATA_PATH
from npvis.settings import NPVIS_PATH
from npvis.settings import PRINT_SCORE_PATH
import os

def run_npvis(in_spectrum, scanId, in_structure, error_thr, error_type):
    cmd = f'{PRINT_SCORE_PATH}/print_score -C {PRINT_SCORE_PATH}/../share/npdtools/ {in_spectrum} {in_structure} '
    cmd += " --ppm " if error_type == "relative" else ""
    cmd += f'--product_ion_thresh {error_thr} '
    cmd += f'--print_matches --print_spectrum --blind_search --scan_num {scanId} > {DATA_PATH}/psm.ann'
    print(cmd)
    os.system(cmd)

    os.system(f'python2.7 {NPVIS_PATH}/visualize.py  --mol {in_structure}  --ann {DATA_PATH}/psm.ann -o {DATA_PATH}/vis.html')
    
    script_str = ""
    with open(os.path.join(DATA_PATH, 'vis.html')) as f:
         add_line = False
         for line in f:
             if line == '<script type="text/javascript">\n':
                 add_line = True
                 continue
                 
             if line == '</script>\n':
                 add_line = False
                 continue
             
             if add_line:
                 script_str += line
             
    return script_str

def run_npvis_inline(in_spectrum, in_structure):
    os.system(
        f'{PRINT_SCORE_PATH}/print_score -C {PRINT_SCORE_PATH}/../share/npdtools/ {in_spectrum} {in_structure} --print_matches --print_spectrum --blind_search > {DATA_PATH}/psm.ann')
    os.system(
        f'python2.7 {NPVIS_PATH}/visualize.py  --mol {in_structure}  --ann {DATA_PATH}/psm.ann --portable_html -o {DATA_PATH}/vis_portable.html')

    return f'{DATA_PATH}/vis_portable.html'

