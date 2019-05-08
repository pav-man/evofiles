function logUpload(data) {
  $('#log-upload').html(data);
}

function formClick(async){
    $( 'form' ).submit(function ( e ) {
        var data;
        data = new FormData();
        data.append( 'file', $( '#file' )[0].files[0] );
        data.append( 'expiry', $( '#expiry' ).val() );
        $.ajax({
            xhr: function()
                {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", function(evt){
                  if (evt.lengthComputable) {
                      logUpload(evt.loaded + ' / ' + evt.total);
                  }
                }, false);
                return xhr;
                },
            url: '/',
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            type: 'POST',
            success: function ( data ) {
                $("#container").html(data);
                formClick(true);
            }
        });
        e.preventDefault();
    });
}

$(document).ready(function (){
    formClick(true);
});




