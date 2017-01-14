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


class Formset {
    constructor(config) {
        this.formsetID = config['formsetID'];
        this.formsID = config['formsID'] || 'forms';
        this.addButtonID = config['addFormID'] || 'add-form';
        this.removeButtonClass = config['removeFormClass'] || 'remove-form';
        this.minimumNumberOfForms = config['minForms'] || 1;
        this.errorMessage = config['errorMessage'];

        this.forms = $('#' + this.formsID);



        $('.' + this.removeButtonClass).click(this, this.removeFormClick);

        this.formToClone = $(this.forms.children()[0]).clone(true, true);
        $(this.formToClone).find('input').attr('value', '');
        $(this.formToClone).find('option').attr('selected', false);
        $(this.formToClone).find('select, input').prop('disabled', '');



        this.addFormButton = $('#' + this.addButtonID);


        this.addFormButton.click(this, this.addFormClick);

        //$('.' + this.removeButtonClass).click(this, this.removeFormClick);
        //var f = this.forms.on('click', '.' + this.removeButtonClass, this.removeFormClick);
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
        var numberOfRows = self.forms.children().length;
        if (numberOfRows > self.minimumNumberOfForms) {
            var rowSelector = '#' + this.formsID + " >";
            var row = $(event.target).parents(rowSelector);
            row.hide('fast', function(){
                row.remove();
                self.renumberRows();
            });
        } else {
            showErrorMessage(this.errorMessage);
        }
    }

    removeFormClick(event) {
        console.log(event);
        event.data.removeForm(event.data, event);
    }

    renumberRows() {
        var allRows = this.forms.children();

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
}

(function($){

})(jQuery);
