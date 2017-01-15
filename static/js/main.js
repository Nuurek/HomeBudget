showModalMessage.djangoToBootstrap = {
    debug: "info",
    info: "info",
    success: "success",
    warning: "warning",
    error: "danger",
}

function showModalMessage(message, type="info", timeout=2000) {
    var modal = $('#infoModal');

    var modalMessage = modal.find("#modalMessage");

    modalMessage.removeClass("alert-success alert-info alert-warning alert-danger");
    modalMessage.addClass("alert-" + showModalMessage.djangoToBootstrap[type]);

    var modalMessageText = modalMessage.find("strong");
    modalMessageText.html(message);

    if (timeout > 0) {
        modal.on('show.bs.modal', function(){
            var modal = $(this);
            clearTimeout(modal.data('hideInterval'));
            modal.data('hideInterval', setTimeout(function(){
                modal.modal('hide');
            }, timeout));
        });
    }

    modal.modal();
}

function showErrorMessage(message) {
    showModalMessage(message, "danger");
}


class Formset {
    constructor(config) {
        this.readConfig(config);

        this.formset = $('#' + this.formsetID);
        this.forms = $('#' + this.formsID);

        this.prepareClone();

        var initialRows = this.forms.children();
        initialRows.attr('initial', true);
        this.numberOfInitials = initialRows.length;
    }

    readConfig(config) {
        this.formsetID = config['formsetID'];
        this.formsID = config['formsID'] || 'forms';
        this.addButtonID = config['addFormID'] || 'add-form';
        this.removeButtonClass = config['removeFormClass'] || 'remove-form';
        this.minimumNumberOfForms = config['minForms'] || 1;
        this.errorMessage = config['errorMessage'];
    }

    prepareClone() {
        $('.' + this.removeButtonClass).click(this, this.removeFormClick);

        this.formToClone = this.getFormPrototype();

        this.addFormButton = $('#' + this.addButtonID);
        this.addFormButton.click(this, this.addFormClick);
    }

    getFormPrototype() {
        var formToClone = $(this.forms.children()[0]).clone(true, true);
        $(formToClone).find('input').attr('value', '');
        $(formToClone).find('option').attr('selected', false);
        $(formToClone).find('select, input, button').prop('disabled', '');

        return formToClone;
    }

    addForm() {
        var newForm = this.formToClone.clone(true, true);
        newForm.hide()
        this.forms.append(newForm);
        newForm.show('fast');
        this.renumberRows();
    }

    addFormClick(event) {
        event.data.addForm(event.data);
    }

    removeForm(self, event) {
        var numberOfRowsAfterUpdate = self.forms.children().filter(':not([hidden])').length;;
        if (numberOfRowsAfterUpdate > self.minimumNumberOfForms) {
            var rowSelector = '#' + this.formsID + " >";
            var row = $(event.target).parents(rowSelector);
            var isInitialRow = row.attr('initial');
            var hiddenRowCallback = function() {};
            if (isInitialRow) {
                hiddenRowCallback = function() {
                    row.attr('hidden', true);
                    var id = $(row.find('input')).attr('name');
                    var index = id.lastIndexOf('-');
                    var deleteAttr = id.substring(0, index + 1);
                    deleteAttr += "DELETE";
                    var deleteInput = $('<input>').attr({
                        type: 'hidden',
                        id: deleteAttr,
                        name: deleteAttr,
                        value: 'on',
                    });
                    deleteInput.appendTo(self.formset);
                };
            } else {
                hiddenRowCallback = function() {
                    row.remove();
                    self.renumberRows();
                };
            }
            row.hide('fast', function() {
                hiddenRowCallback();
            });
        } else {
            showErrorMessage(this.errorMessage);
        }
    }

    removeFormClick(event) {
        event.data.removeForm(event.data, event);
    }

    renumberRows() {
        var allRows = this.forms.children();

        var numberOfRows = allRows.length;

        for (var index = this.numberOfInitials; index < numberOfRows; index++) {
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
}

(function($){

})(jQuery);
