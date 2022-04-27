from npvis.settings import DATA_PATH
from npvis.settings import NPVIS_PATH
from npvis.settings import PRINT_SCORE_PATH
import os

def run_npvis(in_spectrum, scanId, in_structure, error_thr, error_type, mode_type, adduct_type, charge_val, user_session):
    in_metadata = os.path.join(DATA_PATH, user_session, "metadata.json")
    out_ann = os.path.join(DATA_PATH, user_session, "psm.ann")
    out_vis = os.path.join(DATA_PATH, user_session, "vis.html")

    if error_type == "relative":
        error_thr = format(float(error_thr)/10**6, '.20f')

    cmd = f'{PRINT_SCORE_PATH}/print_score -C {PRINT_SCORE_PATH}/../share/npdtools/ {in_spectrum} {in_structure} '
    cmd += " --print_structure_summary "
    cmd += " --ppm " if error_type == "relative" else ""
    cmd += f'--product_ion_thresh {error_thr} '
    cmd += f'--print_matches --print_spectrum '
    cmd += f'--adduct {adduct_type} '
    cmd += f'--charge {charge_val} '
    cmd += "--blind_search " if mode_type == "PNPmd" else ""
    cmd += "--use_input_scan " if int(scanId) > 0 else ""
    cmd += f'--scan_num {scanId} > {out_ann}'
    print(cmd)
    if os.system(cmd) != 0:
        raise Exception("error in print score")

    if os.system(f'python2.7 {NPVIS_PATH}/visualize.py  --mol {in_structure}  --ann {out_ann} --metadata {in_metadata} -o {out_vis}') != 0:
        raise Exception("error in visualization")
    
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
    in_metadata = os.path.join(DATA_PATH, user_session, "metadata.json")
    out_ann = os.path.join(DATA_PATH, user_session, "psm.ann")
    out_vis = os.path.join(DATA_PATH, user_session, "vis_portable.html")

    os.system(f'python2.7 {NPVIS_PATH}/visualize.py  --mol {in_structure}  --ann {out_ann} --metadata {in_metadata} --portable_html -o {out_vis}')

    return out_vis

