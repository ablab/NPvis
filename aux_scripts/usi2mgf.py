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
      or
    JSON previously resolved from USI, dowloaded and provided via --json option
    MGF output filepath via --mgf option
Result:
    USI is resolved and converted to MGF. It is written to the output filepath if specified or to stdout otherwise.

Examples:
python usi2mgf.py --usi mzspec:MASSBANK::accession:SM858102 > spec.mgf
python usi2mgf.py --json test_data/test_spec.json --mgf spec.mgf
'''


import argparse
import sys
import json
import numpy as np
import requests
import os

from matchms.Spectrum import Spectrum
from matchms.exporting import save_as_mgf

# any metadata not in ALLOWED_MGF_FIELDS will be removed
ALLOWED_MGF_FIELDS = ['TITLE', 'PEPMASS', 'CHARGE', 'MSLEVEL', 'SCAN', 'CHARGE', 'RTINSECONDS']


def error(msg):
    sys.stderr.write(f"Error! {msg}\n")
    sys.exit(1)


# partially based on matchms.importing.load_from_usi
def load_json_from_usi(usi: str, server: str = "https://metabolomics-usi.ucsd.edu"):
    # Create the url
    url = server + "/json/?usi1=" + usi

    response = requests.get(url)

    if response.status_code == 404:
        return None
    try:
        spectral_data = response.json()
        if spectral_data is None or "peaks" not in spectral_data:
            return None
        return spectral_data

    except json.decoder.JSONDecodeError:
        # failed to unpack json
        return None


# partially based on matchms.importing.load_from_usi
def json_to_spectrum(spectral_data: object):
    peaks = spectral_data["peaks"]
    if len(peaks) == 0:
        return None
    mz_list, intensity_list = zip(*peaks)
    mz_array = np.array(mz_list)
    intensity_array = np.array(intensity_list)

    metadata = {}
    metadata["PEPMASS"] = spectral_data.get("precursor_mz", None)
    metadata["CHARGE"] = spectral_data.get("precursor_charge", None)

    s = Spectrum(mz_array, intensity_array, metadata)
    return s


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--usi", help="spectrum USI",
                       metavar='STRING', type=str, default=None)
    group.add_argument("--json", help="spectrum in the JSON format (resolved from USI)",
                       metavar='FILEPATH', type=str, default=None)
    parser.add_argument("--mgf", "-o", help="output MGF filepath, will be printed to stdout if not specified",
                        metavar='FILEPATH', type=str, default=None)

    parsed_args = parser.parse_args()
    if parsed_args.usi is None and parsed_args.json is None:
        error("Either --usi or --json should be specified!")
    return parsed_args


def clean_spectrum_metadata(spectrum):
    cleaned_metadata = spectrum.metadata
    for k in list(cleaned_metadata.keys()):
        if k.upper() not in ALLOWED_MGF_FIELDS:
            del cleaned_metadata[k]
    spectrum.metadata = cleaned_metadata


def main(args):
    if args.usi is not None:
        spectrum_json = load_json_from_usi(args.usi)
        if spectrum_json is None:
            error(f"Failed to retrieve a spectrum using the provided USI ({args.usi})")
    else:
        if os.path.isfile(args.json):
            with open(args.json) as f:
                spectrum_json = json.loads(f.read())
        else:
            error(f"Provided JSON files does not exist ({args.json})")

    spectrum = json_to_spectrum(spectrum_json)
    clean_spectrum_metadata(spectrum)
    save_as_mgf(spectrum, args.mgf)


if __name__ == "__main__":
    args = parse_args()
    main(args)
