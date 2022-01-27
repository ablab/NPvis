function updateSpectrumInputType() {
    var elem = document.getElementById("id_ms_input_type");
    if (elem.value === 'mgf') {
        document.getElementById("spect-upload-file-id").innerHTML =
            '<div class="upload-file">' +
            '    <button class="upload btn"> Upload</button>' +
            '    <div class="upload-input"> Choose file...</div>' +
            '    <input type="file" name="inputSpectrum" required="" id="id_inputSpectrum"' +
            '           onChange="changeFileName(this)" title="Choose file in mgf format...">' +
            '</div>' +
            '<div class="oneline">' +
            '    <p class="input-name-p">Scan ID:</p> <input type="number" class="custom-input" value="0" id="id_inputScanID" name="inputScanId">' +
            '</div>';
    } else if (elem.value === 'gusi') {
        document.getElementById("spect-upload-file-id").innerHTML =
                '   <input type="text" class="custom-input-text" name="inputSpectrum" required="" id="id_inputSpectrum">';
    }

    lookAfterSelectElem();
}

function updateStructureInputType() {
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

function updateErrorType() {
    var elem = document.getElementById("id_error_type")
    if (elem.value === "absolute") {
        document.getElementById("error_thr_unit").innerHTML = "<p class=\"fl_label\">Da</p>"
    } else if (elem.value === "relative") {
        document.getElementById("error_thr_unit").innerHTML = "<p class=\"fl_label\">ppm</p>"
    }
}

