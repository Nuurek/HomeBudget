function setUpDatePicker() {
    $('#bill-date').datepicker({
        format: "dd/mm/yyyy",
        weekStart: 1,
        todayBtn: "linked",
        language: "pl",
        keyboardNavigation: false,
        todayHighlight: true
    });
    $('#bill-date').datepicker('update', new Date());
}

function setUpElements() {
    var createBillForm = $('#create-bill-form');
    var brandSelect = $('#id_brand')[0];
    var shopSelect = $('#id_sklepy_adres')[0];
    var billRecords = $('#bill-records-rows');
    billRecords.find('select, input').prop('required', 'required');

    var recordToClone = $(billRecords.children()[0]).clone();
    $(recordToClone).find('input').attr('value', '');
    $(recordToClone).find('option').attr('selected', false);
    $(recordToClone).find('select, input').prop('disabled', '');

    var addRecordButton = $('#add-bill-record');
    var disabledInputs = $(createBillForm).find('select, input, button').slice(2);

    var checkForErrorAndDisable = function() {
        var brand = brandSelect.value;
        var brandShops = shops[brand];

        if(brandShops != undefined) {
            $(createBillForm).find('select, input, button').slice(2).prop('disabled', '');
        } else {
            shopSelect.append(new Option("BRAK SKLEPU!", ""));
            $(createBillForm).find('select, input, button').slice(2).prop('disabled', 'disabled');
        }
    }

    var onBrandSelectChange = function() {
        var brand = brandSelect.value;
        var brandShops = shops[brand];

        $(shopSelect).find('option').remove();
        $.each(brandShops, function(index, shop){
            shopSelect.append(new Option(shop, shop));
        });

        checkForErrorAndDisable();
    }

    var addBillRecord = function() {
        var newRecord = recordToClone.clone().hide()
        billRecords.append(newRecord);
        newRecord.show('fast');
        renumberRows();
    }

    var removeBillRecord = function() {
        var numberOfRows = billRecords.children().length;
        console.log(numberOfRows);
        if (numberOfRows > 1) {
            var row = $(this).parent().parent();
            row.hide('fast', function(){
                row.remove();
                renumberRows();
            });
        } else {
            showErrorMessage("Paragon musi zawierać co najmniej jedną pozycję.");
        }
    }

    function renumberRows() {
        var allRows = billRecords.children();

        var numberOfRows = allRows.length;

        for (var index = 0; index < numberOfRows; index++) {
            var inputs = $(allRows[index]).find("[id^='id_']");
            console.log(index, inputs);
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

    onBrandSelectChange();
    $(brandSelect).change(onBrandSelectChange);
    $(addRecordButton).click(addBillRecord);
    $(billRecords).on('click', '.remove-bill-record', removeBillRecord);

    checkForErrorAndDisable();
}

(function($){
    setUpDatePicker();
    setUpElements();
})(jQuery);