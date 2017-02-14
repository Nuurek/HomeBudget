function setUpBrandName() {
    var brandName = $('#id_name');
    brandName.attr('readonly', '');
    var editButton = $('#brand-name-edit');
    var removeButton = $('#brand-delete-button');
    var confirmMessage = $('#brand-delete-confirm');
    var yesButton = $('#brand-delete-yes');
    var noButton = $('#brand-delete-no');
    var editIcon = $(editButton.find('span'));
    var submitButton = $('#submit-button');

    editButton.click(function(){
        editButton.removeAttr('class').blur();
        editIcon.removeAttr('class');

        if (brandName.attr('readonly')) {
            brandName.removeAttr('readonly');
            editButton.attr('class', 'btn btn-success');
            editIcon.attr('class', 'glyphicon glyphicon-ok');
            submitButton.attr('disabled', '');
        } else {
            brandName.attr('readonly', '');
            editButton.attr('class', 'btn btn-info');
            editIcon.attr('class', 'glyphicon glyphicon-edit');
            submitButton.removeAttr('disabled');
        }
    });

    removeButton.click(function() {
        showModalMessage(confirmMessage.html(), 'error', 10000);
    });
}

(function($){
    setUpBrandName();

    var formset = new Formset({
        "formsetID": "shops-formset",
        "minForms": "0"
    });
})(jQuery);
