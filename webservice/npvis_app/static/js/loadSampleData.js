function loadSampleData() {
    console.log("Load sample data");
    var elem = document.getElementById("id_struct_input_type");
    elem.value="smiles";
    elem.selectedIndex = 1;

    var elemms = document.getElementById("id_ms_input_type");
    elemms.value="gusi";
    elemms.selectedIndex = 1;

    lookAfterSelectElem();
    updateStructureInputType();
    updateSpectrumInputType();

    var eleminSpec = document.getElementById("id_inputStructure");
    eleminSpec.value = "CCC(C)C1C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)NC(C(=O)N1)C)C(C)CC)CC(C)C)CC2=CC=CC=C2)C(C)CC)CCCCN)C(C)CC";

    var eleminMS = document.getElementById("id_inputSpectrum");
    eleminMS.value = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00000839197"

    var elemName = document.getElementById("id_compound_name");
    elemName.value = "Surugamide A"

    var elemMode = document.getElementById("id_mode_type");
    elemMode.value = "PNPmd";
    elemMode.selectedIndex = 2;

    return false;
}