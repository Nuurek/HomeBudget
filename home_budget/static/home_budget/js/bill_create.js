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
    var shopSelect = $('#id_shop_address')[0];
    var billRecords = $('#bill-records-rows');

    var recordToClone = $(billRecords.children()[0]).clone();
    $(recordToClone).find('select, input').prop('disabled', '');

    var addRecordButton = $('#add-bill-record');
    var disabledInputs = $(createBillForm).find('select, input, button').slice(2);

    var checkForErrorAndDisable = function() {
        var brand = brandSelect.value;
        var brandShops = shops[brand];

        if(brandShops != undefined) {
            $(disabledInputs).prop('disabled', '');
        } else {
            shopSelect.append(new Option("BRAK SKLEPU!", ""));
            $(disabledInputs).prop('disabled', 'disabled');
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
        billRecords.append(recordToClone.clone());
    }

    var removeBillRecord = function() {
        var numberOfRows = $(billRecords).children().length;
        if (numberOfRows > 1) {
            $(this).parent().parent().remove();
        } else {
            showErrorMessage("Paragon musi zawierać co najmniej jedną pozycję.");
        }
    }

    $(brandSelect).change(onBrandSelectChange);
    $(addRecordButton).click(addBillRecord);
    $(billRecords).on('click', '.remove-bill-record', removeBillRecord);

    checkForErrorAndDisable();
}

(function($){
    setUpDatePicker();
    setUpElements();
})(jQuery);
