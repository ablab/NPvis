## Console tool usage

**NB!** This file provides hints on the [console NPvis tool](https://github.com/ablab/NPvis/releases) installation and usage. 
Please first read the [main README](../README.md) to get the general info about the tool and its inputs/outputs.

**NB!** We strongly recommend you to use the NPvis [web service](http://cab.cc.spbu.ru/npvis/) since its much more robust and user-friendly! 

### Prerequisites & Dependencies

* Linux or macOS
* Python 2.7 

You will also need [NPDtools](https://cab.spbu.ru/software/npdtools/) 2.5.0.
It can be downloaded for your platform [here](https://github.com/ablab/npdtools/releases), e.g. for Linux type

    wget https://github.com/ablab/npdtools/releases/download/npdtools-2.5.0/NPDtools-2.5.0-Linux.tar.gz
    tar -xzf NPDtools-*.tar.gz

We assume that the NPDtools package is unpacked in the current working directory. Adjust the paths accordingly if needed.

### Input data

The console version currently accepts only the MGF and mzXML formats for spectra and MDL MOL V3000 for structures.
Sample examples are in the [test data folder](https://github.com/ablab/NPvis/tree/main/test_data). 
Please convert your data to these formats using third-party software (see hints/links in the [main README](../README.md)).

### Running the tool

As an example we will use `massetolide_1252.mgf` and `massetolide_A.mol` files from the test data. 
This is not an exact match, the masses of the compound and MS/MS are different, so we will run NPvis in the "PNP with modification" mode.

**First**, we need to create the annotation file for a Peptide-Spectrum Match (`psm.ann`).

    NPDtools-*/bin/print_score -C NPDtools-*/share/npdtools/ test_data/massetolide_1252.mgf test_data/massetolide_A.mol --print_matches --print_spectrum --print_structure_summary --blind_search > psm.ann
    
For running NPvis in the "PNP" mode simply remove the `--blind_search` option.

**Second**, visualize the match!

    python2.7 visualize.py --mol test_data/massetolide_A.mol --ann psm.ann --portable_html -o my_first_visualization.html 

The resulting NPvis report is in `my_first_visualization.html` (feel free to use another filename).
Mind the option `--portable_html` that embeds everything needed (JavaScripts and CSS) inside the HTML file, so you can move it wherever you want.

### Plans for the next console release

1. Python v.3 support.
2. Single-push-of-a-button, i.e., `print_score` part would be embedded, so a user will need to run only `visualize.py`.
3. Support for SMILES, USI, and other currently unsupported data formats.

### Disclaimer

The JavaScript part of the visualizer is based on the [Lorikeet Spectrum Viewer](https://github.com/UWPR/Lorikeet) for proteomics.