from npvis.settings import DATA_PATH
from npvis.settings import NPVIS_PATH
from npvis.settings import PRINT_SCORE_PATH
import os

def run_npvis(in_spectrum, scanId, in_structure, error_thr, error_type, mode_type, user_session):
    out_ann = os.path.join(DATA_PATH, user_session, "psm.ann")
    out_vis = os.path.join(DATA_PATH, user_session, "vis.html")

    cmd = f'{PRINT_SCORE_PATH}/print_score -C {PRINT_SCORE_PATH}/../share/npdtools/ {in_spectrum} {in_structure} '
    cmd += " --ppm " if error_type == "relative" else ""
    cmd += f'--product_ion_thresh {error_thr} '
    cmd += f'--print_matches --print_spectrum '
    cmd += "--blind_search " if mode_type == "PNPmd" else ""
    cmd += f'--scan_num {scanId} > {out_ann}'
    print(cmd)
    os.system(cmd)

    os.system(f'python2.7 {NPVIS_PATH}/visualize.py  --mol {in_structure}  --ann {out_ann} -o {out_vis}')
    
    script_str = ""
    with open(out_vis) as f:
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

def run_npvis_inline(in_spectrum, in_structure, user_session):
    out_ann = os.path.join(DATA_PATH, user_session, "psm.ann")
    out_vis = os.path.join(DATA_PATH, user_session, "vis_portable.html")

    os.system(f'python2.7 {NPVIS_PATH}/visualize.py  --mol {in_structure}  --ann {out_ann} --portable_html -o {out_vis}')

    return out_vis

