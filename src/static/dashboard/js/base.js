$(function() { // DOM Ready
    $('form').submit(function() {
       $.LoadingOverlay("show");
       return true;
    });
});