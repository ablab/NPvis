function updateStructureInputType() {
    console.log("update");
    var elem = document.getElementById("id_struct_input_type");
    if (elem.value === 'mol') {
        document.getElementById("struct-input-file-header-id").innerHTML = "Mol file:"
        document.getElementById("struct-upload-file-id").innerHTML =
            '<div class="upload-file">' +
            '    <button class="upload btn"> Upload</button>' +
            '    <div class="upload-input"> Choose file in mol format...</div>' +
            '    <input type="file" name="inputStructure" required="" id="id_inputStructure"' +
            '           onChange="changeFileName(this)" title="Choose file in mol format...">' +
            '</div>';
    } else if (elem.value === 'smiles') {
        document.getElementById("struct-input-file-header-id").innerHTML = "SMILES string:"
        document.getElementById("struct-upload-file-id").innerHTML =
                '   <input type="text" class="custom-input-text" name="inputStructure" required="" id="id_inputStructure">';
    }

    lookAfterSelectElem();
}
