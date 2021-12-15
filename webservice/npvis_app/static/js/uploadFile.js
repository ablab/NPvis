var file_api = ( window.File && window.FileReader && window.FileList && window.Blob ) ? true : false;

function changeFileName(selid) {
    var file_name;
    var inp = $(selid);
    console.log(inp);
    console.log($(selid)[0].parentNode);
    var lbl = $(selid)[0].parentNode.getElementsByClassName("upload-input")[0];
    console.log(lbl);
    if( file_api && inp[ 0 ].files[ 0 ] )
        file_name = inp[ 0 ].files[ 0 ].name;
    else
        file_name = inp.val().replace( "C:\\fakepath\\", '' );

    if( ! file_name.length )
        return;

    lbl.innerHTML = file_name;
}
