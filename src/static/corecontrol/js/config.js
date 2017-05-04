function checkboxChange(key, checkbox) {
    $("input[name='" + key + '.' + checkbox.attr('id') + "']").val($(checkbox).is(':checked') ? 'on' : 'off');
};
