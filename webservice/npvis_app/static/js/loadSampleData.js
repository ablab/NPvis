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
    eleminSpec.value = "CCCCCCCC(CC(=O)NC(CC(C)C)C(=O)NC(CCC(=O)O)C(=O)NC1C(C)OC(=O)C(C(C)CC)NC(=O)C(CO)NC(=O)C(CC(C)C)NC(=O)C(CO)NC(=O)C(CC(C)C)NC(=O)C(C(C)CC)NC1=O)O";

    var eleminMS = document.getElementById("id_inputSpectrum");
    eleminMS.value = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00004679304"
    return false;
}