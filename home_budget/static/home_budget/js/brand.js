function setUpBrandName() {
    var brandName = $('#id_nazwa');
    var editButton = $('#brand-name-edit');
    var removeButton = $('#brand-delete-button');
    var confirmMessage = $('#brand-delete-confirm');
    var yesButton = $('#brand-delete-yes');
    var noButton = $('#brand-delete-no');
    var icon = $(editButton.find('span'));

    editButton.click(function(){
        editButton.blur();
        icon.removeAttr('class');

        if (brandName.attr('disabled')) {
            brandName.removeAttr('disabled');
            icon.attr('class', 'glyphicon glyphicon-ok');
        } else {
            brandName.attr('disabled', '');
            icon.attr('class', 'glyphicon glyphicon-edit');
        }
    });

    removeButton.click(function() {
        console.log("Remove!");
        showModalMessage(confirmMessage.html(), 'error', 10000);
    });
}

(function($){
    setUpBrandName();

    var formset = new Formset({
        "formsetID": "shops-formset",
        "minForms": "0",
    });
})(jQuery);
