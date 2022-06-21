#!/usr/bin/env python

import os
import sys
import json
from optparse import OptionParser
from os.path import abspath, dirname, realpath, join, exists, basename, splitext
from site import addsitedir

script_dirpath = abspath(dirname(realpath(__file__)))
html_aux_files_dir = join(script_dirpath, 'html_aux_files')

addsitedir(join(script_dirpath, 'python_libs'))
# from d_utils.visual_utils import parse_spectrum_annotation, embed_html_aux_files
from visual_utils import parse_spectrum_annotation, embed_html_aux_files
# from aux_json_generator import get_aux_info_from_mol  # FIXME


def parse_spectrum_metadata(spec_fpath):
    mgf_key_to_metadata_key = {'RTINSECONDS': ('retention', float), 'PEPMASS': ('mz', float),
                               'SCAN': ('scan', int), 'CHARGE': ('charge', int),
                               'FILENAME': ('filename', str), 'FILEPATH': ('filename', str)}
    parsed = {}
    with open(spec_fpath) as f:
        for line in f:
            if line[0].isdigit():
                break
            if '=' not in line:
                continue
            mgf_key, mgf_value = line.strip().split('=')
            if mgf_key in mgf_key_to_metadata_key:
                meta_key, meta_func = mgf_key_to_metadata_key[mgf_key]
                parsed[meta_key] = meta_func(mgf_value.split()[0])
    return parsed


def parse_compound_metadata(ann_fpath, compound_seq=None, spectrum_info=None, hide_mass_error=False):
    parsed = {}
    with open(ann_fpath) as f:
        for line in f:
            if line.startswith('structure'):
                # structure : C83H144N22O28S2 mass : 1870.946744
                word1, semicolon1, formula, word2, semicolon2, mass = line.strip().split()
                parsed['mass'] = float(mass)
                parsed['formula'] = str(formula)
            elif not hide_mass_error and line.startswith('mass error'):
                word1, word2, semicolon1, mass_error = line.strip().split()
                parsed['massError'] = float(mass_error)
    if 'mass' in parsed and 'formula' in parsed and compound_seq and ('+' in compound_seq or '-' in compound_seq):
        # based on https://stackoverflow.com/a/29581287
        import re
        all_mods = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", compound_seq)
        mod_mass = sum(map(float, all_mods))
        if mod_mass:
            parsed['formula'] += '%s%.3f' % ('+' if mod_mass > 0 else '', mod_mass)
    if spectrum_info and 'charge' in spectrum_info:  # only M+H, M+2H, etc adducts are supported
        parsed['adduct'] = 'M+%sH' % spectrum_info['charge']
    return parsed


def parse_metadata(metadata_fpath, ann_fpath):
    def _get_adduct_str(charge, adduct_type):
        sign = '+'
        if charge < 0:
            sign = '-'
        multiplier = ''
        if abs(charge) > 1:
            multiplier = str(abs(charge))
        return 'M%s%s%s' % (sign, multiplier, adduct_type)


    metadata_dict = {}

    with open(metadata_fpath) as f:
        raw_metadata_dict = json.load(f)

    # spectrum metadata
    try:
        metadata_dict['spectrumInfo'] = {
            'filename': os.path.basename(raw_metadata_dict['file_spectrum']) if raw_metadata_dict['file_spectrum']
                                                                             else raw_metadata_dict['gusi'],
            'scan': str(raw_metadata_dict['scanId']) if raw_metadata_dict['scanId'] else None,
            'charge': raw_metadata_dict['charge_val']
        }
        metadata_dict['spectrumInfo'].update(parse_spectrum_metadata(ann_fpath))
    except KeyError:
        pass

    # compound metadata
    try:
        metadata_dict['compoundInfo'] = {
            'name': raw_metadata_dict['compound_name'],
            # TODO: handle negative charges properly
            'adduct': None if not raw_metadata_dict['charge_val'] or not raw_metadata_dict['adduct_type']
                           else _get_adduct_str(raw_metadata_dict['charge_val'], raw_metadata_dict['adduct_type']),
            'SMILES': raw_metadata_dict['smiles']
        }
        metadata_dict['compoundInfo'].update(parse_compound_metadata(ann_fpath))
    except KeyError:
        pass

    # PSM metadata
    try:
        metadata_dict['psmInfo'] = {
            'mode': raw_metadata_dict['mode_type'],
            'error_type': raw_metadata_dict['error_type'],
            'error_thr': raw_metadata_dict['error_threshold'],
            'error_unit': 'Da' if raw_metadata_dict['error_type'] == 'absolute' else 'ppm'
        }
        if 'compoundInfo' in metadata_dict and 'massError' in metadata_dict['compoundInfo']:
            metadata_dict['psmInfo']['parentMassError'] = metadata_dict['compoundInfo']['massError']
    except KeyError:
        pass

    return metadata_dict



def main(args):
    parser = OptionParser(description='')
    parser.add_option('--mol', dest='mol_fpath')
    parser.add_option('--ann', dest='ann_fpath',
                      help='To get it, please run "./bin/print_score spectrum.mgf compound.mol'
                           ' --print_matches --print_spectrum [--blind_search] [--print_structure_summary] > your.ann')
    parser.add_option('-s', '--seq_in', dest='protein_seq', help='Protein sequence')
    parser.add_option('--portable_html', dest='portable_html', action='store_true', default=False,
                      help='Create portable HTML with embedded JS and CSS files')
    parser.add_option('-o', '--output', help='Output HTML filepath (default: in CWD, based on compound name). '
                                             'Hint: you should probably use --protable_html if the output is not in CWD')
    parser.add_option('--metadata', dest='metadata', help='Spectrum and compound metadata in a JSON file '
                                                          '(see sample npvis_metadata.json as an example)')
    parser.add_option('--spectrum', dest='spec_fpath', help='Input spectum in MGF (used for extracting metadata only)')
    parser.add_option('--compound', help='Compound name (for metadata)')
    parser.add_option('--hide-mass-error', help='Do not show "Mass error" even if present in metadata',
                      action='store_true', default=False)
    # parser.add_option('-m', '--multi', dest='is_multi', action='store_true', default=False)
    (opts, args) = parser.parse_args()
    if not opts.ann_fpath or (not opts.mol_fpath and not opts.protein_seq):
        print 'Usage: python', sys.argv[0], ' --ann ann_file [--mol mol_file] [-s seq]' \
                                            '[--mod mod_component --mass_shift mod_component]'
        exit(0)

    if not exists(opts.ann_fpath):
        print 'Error! ' + opts.ann_fpath + ' does not exist (annotation file)'

    aux_data = dict()

    if opts.protein_seq:
        aux_data['sequence'] = opts.protein_seq
        opts.mol_fpath = os.path.splitext(opts.ann_fpath)[0] + '.mol'
    elif opts.mol_fpath and exists(opts.mol_fpath):
        mol_fpath = abspath(opts.mol_fpath)
        # aux_data = get_aux_info_from_mol(mol_fpath)  # FIXME!
    else:
        print 'Error! ' + opts.mol_fpath + ' does not exist (MOL file)'
        exit(1)

    spectrum, annotation, modification, _ = parse_spectrum_annotation(opts.ann_fpath)
    psm_details = {'spectrum': spectrum,
                   'annotation': annotation}
    if modification:
        psm_details['modification'] = modification

    psm_details.update(aux_data)

    if opts.metadata and os.path.isfile(opts.metadata):
        psm_details.update(parse_metadata(opts.metadata, opts.ann_fpath))
    # if False:  # demo filling
    #     psm_details['spectrumInfo'] = {'filename': 'spectrum.mgf', 'scan': 1, 'charge': 1, 'mz': 101.500}
    #     psm_details['compoundInfo'] = {'name': 'Surfactin', 'mass': 100.500, 'adduct': 'M+H'}
    # # additional parsing of metadata from available sources
    # if opts.spec_fpath and os.path.isfile(opts.spec_fpath) and os.path.splitext(opts.spec_fpath)[1].lower() == '.mgf':
    #     if 'spectrumInfo' not in psm_details:
    #         psm_details['spectrumInfo'] = {}
    #     psm_details['spectrumInfo'].update(parse_spectrum_metadata(opts.spec_fpath))
    # if opts.compound:
    #     if 'compoundInfo' not in psm_details:
    #         psm_details['compoundInfo'] = {}
    #     psm_details['compoundInfo']['name'] = opts.compound
    #     psm_details['compoundInfo'].update(parse_compound_metadata(opts.ann_fpath, opts.protein_seq,
    #                                                                psm_details['spectrumInfo'],
    #                                                                opts.hide_mass_error))

    template_fpath = os.path.join(script_dirpath, 'template.html')
    with open(template_fpath) as template_file:
        html = template_file.read()

        html = html.replace('{{ JSON }}', json.dumps(psm_details))
        html = html.replace('\\n', '\\\\n')
        if opts.portable_html:
            html = embed_html_aux_files(html, html_aux_files_dir)

    mol_name = splitext(basename(opts.mol_fpath))[0]
    if opts.output:
        html_fpath = opts.output
    else:
        html_fpath = os.path.join(script_dirpath, mol_name + '.html')
    if os.path.exists(html_fpath):
        os.remove(html_fpath)
    with open(html_fpath, 'w') as f_html:
        f_html.write(html)
    print('Result is in ' + html_fpath)


if __name__ == '__main__':
    main(sys.argv[1:])
