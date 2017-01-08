(function($){
    $('#bill-date').datepicker({
        format: "dd/mm/yyyy",
        weekStart: 1,
        todayBtn: "linked",
        language: "pl",
        keyboardNavigation: false,
        todayHighlight: true
    });
    $('#bill-date').datepicker('update', new Date());

    var createBillForm = $('#create-bill-form');
    var brandSelect = $('#id_brand')[0];
    var shopSelect = $('#id_shop_address')[0];
    var disabledInputs = $(createBillForm).find('select, input').slice(2);

    var onBrandSelectChange = function() {
        var brand = brandSelect.value;
        var brandShops = shops[brand];

        $(shopSelect).find('option').remove();
        $.each(brandShops, function(index, shop){
            shopSelect.append(new Option(shop, shop));
        });
        if(brandShops != undefined) {
            $(disabledInputs).prop('disabled', '');
        } else {
            shopSelect.append(new Option("BRAK SKLEPU!", ""));
            $(disabledInputs).prop('disabled', 'disabled');
        }
    }

    $(brandSelect).change(onBrandSelectChange);
})(jQuery);
