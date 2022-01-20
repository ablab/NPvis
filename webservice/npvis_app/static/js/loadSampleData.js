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
    eleminSpec.value = "[H]OC(=O)C([H])([H])C([H])([H])[C@@]1([H])N([H])C(=O)C([H])([H])C([H])(OC(=O)[C@@]([H])(N([H])C(=O)[C@]([H])(N([H])C(=O)[C@@]([H])(N([H])C(=O)[C@@]([H])(N([H])C(=O)C([H])(N([H])C(=O)[C@@]([H])(N([H])C1=O)C([H])(C([H])([H])[H])C([H])([H])[H])C([H])([H])C([H])(C([H])([H])[H])C([H])([H])[H])C([H])(C([H])([H])[H])C([H])([H])[H])C([H])([H])C(=O)OC([H])([H])[H])C([H])([H])C([H])(C([H])([H])[H])C([H])([H])[H])C([H])(C([H])([H])[H])C([H])([H])[H])C([H])([H])C([H])([H])C([H])([H])C([H])([H])C([H])([H])C([H])([H])C([H])([H])C([H])([H])C([H])([H])C([H])([H])C([H])([H])[H]";

    var eleminMS = document.getElementById("id_inputSpectrum");
    eleminMS.value = "mzspec:GNPS:TASK-e026d6bd717144eaaa3745918a8276b5-spec/spec-00000.mgf:scan:1"
    return false;
}