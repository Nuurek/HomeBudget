function showModalMessage(message, type="info", timeout=2000) {
    var modal = $('#infoModal');

    var modalMessage = modal.find("#modalMessage");
    modalMessage.removeClass("alert-success alert-info alert-warning alert-danger");
    modalMessage.addClass("alert-" + type);

    var modalMessageText = modalMessage.find("strong");
    modalMessageText.text(message);

    modal.on('show.bs.modal', function(){
        var modal = $(this);
        clearTimeout(modal.data('hideInterval'));
        modal.data('hideInterval', setTimeout(function(){
            modal.modal('hide');
        }, timeout));
    });

    modal.modal();
}

function showErrorMessage(message) {
    showModalMessage(message, "danger");
}


function setUpFormset(config) {
    var formsetID = config['formsetID'];
    var formsID = config['formsID'] || 'forms';
    var addButtonID = config['addFormID'] || 'add-form';
    var removeButtonClass = config['removeFormClass'] || 'remove-form';
    var minimumNumberOfForms = config['minForms'] || 1;
    var errorMessage = config['errorMessage'];

    var forms = $('#' + formsID);

    var formToClone = $(forms.children()[0]).clone();
    $(formToClone).find('input').attr('value', '');
    $(formToClone).find('option').attr('selected', false);
    $(formToClone).find('select, input').prop('disabled', '');

    var addFormButton = $('#' + addButtonID);

    var addForm = function() {
        var newForm = formToClone.clone();
        newForm.hide()
        forms.append(newForm);
        newForm.show('fast');
        renumberRows();
    }


    var removeForm = function() {
        var numberOfRows = forms.children().length;
        if (numberOfRows > minimumNumberOfForms) {
            var rowSelector = '#' + formsID + " >";
            var row = $(this).parents(rowSelector);
            row.hide('fast', function(){
                row.remove();
                renumberRows();
            });
        } else {
            showErrorMessage(errorMessage);
        }
    }


    function renumberRows() {
        var allRows = forms.children();

        var numberOfRows = allRows.length;

        for (var index = 0; index < numberOfRows; index++) {
            var inputs = $(allRows[index]).find("[id^='id_']");
            inputs.each(function(){
                var input = $(this)
                var newID = input.attr('id').replace(/[0-9]+/, index);
                input.attr('id', newID);
                var newID = input.attr('name').replace(/[0-9]+/, index);
                input.attr('name', newID);
            })
        }

        $('input[id$="TOTAL_FORMS"]').attr('value', numberOfRows);
    }

    addFormButton.click(addForm);
    var f = forms.on('click', '.' + removeButtonClass, removeForm);
}

(function($){

})(jQuery);
