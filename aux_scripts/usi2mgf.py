#!/usr/bin/env python3

'''
Dependencies:
* matchms (https://github.com/matchms/matchms)
* Python 3.7, 3.8 or 3.9  (implied by matchms)


How to install via conda:

conda create --name matchms --channel nlesc --channel bioconda --channel conda-forge matchms python=3.8
conda activate

=======
Script arguments:
    USI via --usi option
    output filepath via --mgf option
Result:
    USI is converted to MGF. It is written to the output filepath if specified or to stdout otherwise.

Example:
python usi2mgf.py --usi mzspec:MASSBANK::accession:SM858102 > spec.mgf
'''


import argparse
import sys
# from matchms.importing import load_from_usi  # temporary broken, see https://github.com/matchms/matchms/issues/307
# also in the custom version, charged is downloaded and 'precursor_mz' changed to 'PEPMASS'
from custom_load_from_usi import load_from_usi
from matchms.exporting import save_as_mgf

# any metadata not in ALLOWED_MGF_FIELDS will be removed
ALLOWED_MGF_FIELDS = ['TITLE', 'PEPMASS', 'CHARGE', 'MSLEVEL', 'SCAN', 'CHARGE', 'RTINSECONDS']


def error(msg):
    sys.stderr.write(f"Error! {msg}\n")
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--usi", "-i", help="spectrum USI",
                        metavar='STRING', type=str, required=True)
    parser.add_argument("--mgf", "-o", help="output MGF filepath, will be printed to stdout if not specified",
                        metavar='FILEPATH', type=str, default=None)

    parsed_args = parser.parse_args()
    return parsed_args


def clean_spectrum_metadata(spectrum):
    cleaned_metadata = spectrum.metadata
    for k in list(cleaned_metadata.keys()):
        if k.upper() not in ALLOWED_MGF_FIELDS:
            del cleaned_metadata[k]
    spectrum.metadata = cleaned_metadata


def main(args):
    spectrum = load_from_usi(args.usi)
    if spectrum is None:
        error(f"Failed to retrieve a spectrum using the provided USI ({args.usi})")
    clean_spectrum_metadata(spectrum)
    save_as_mgf(spectrum, args.mgf)


if __name__ == "__main__":
    args = parse_args()
    main(args)
