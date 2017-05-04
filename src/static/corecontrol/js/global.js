// FIX GLOBAL para el TOKEN en las peticiones ajaxs
function getCookie(name)
{
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         doing_ajax(true);
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     },
     complete: function () {
         doing_ajax(false);
    }
});

function doing_ajax(start) {
    if(start) {$.LoadingOverlay("show");}
    else {$.LoadingOverlay("hide");}
}


$(function() { // DOM Ready
    // Bind boton startpr
    $("[name=startpr]").bind("click", function() {
        startproc()
    });
    $("[name=stoppr]").bind("click", function() {
        stopproc()
    });
    $('[data-toggle="tooltip"]').tooltip();
});

function startproc() {
    $.ajax({ url: "/corecontrol/startproc" })
    .done(function( data ) {
        alert(data['message']);
     });
    //location.reload()
}

function stopproc() {
    $.ajax({ url: "/corecontrol/stopproc" })
    .done(function( data ) {
        alert(data['message']);
     });
    //location.reload()
}