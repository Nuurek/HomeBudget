function setUpDatePicker() {
    $('#bill-date').datepicker({
        format: "dd.mm.yyyy",
        weekStart: 1,
        todayBtn: "linked",
        language: "pl",
        keyboardNavigation: false,
        todayHighlight: true
    });
    //$('#bill-date').datepicker('update', new Date());
}

function setUpElements() {
    var createBillForm = $('#create-bill-form');
    var brandSelect = $('#id_brand')[0];
    var shopSelect = $('#id_sklepy_id')[0];

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
            shopSelect.append(new Option(shop['address'], shop['id']));
        });

        checkForErrorAndDisable();
    }

    onBrandSelectChange();
    $(brandSelect).change(onBrandSelectChange);

    checkForErrorAndDisable();
}

(function($){
    setUpDatePicker();
    setUpElements();
    var formset = new Formset({
        "formsetID": "bill-records",
        "errorMessage": "<strong>Paragon musi zawierać co najmniej jeden zakup.<strong>",
    });
})(jQuery);
