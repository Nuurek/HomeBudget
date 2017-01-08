(function($){
    var brandSelect = jQuery('#id_brand')[0];
    var shopSelect = jQuery('#id_shop_address')[0];

    var onBrandSelectChange = function() {
        var brand = brandSelect.value;
        var brandShops = shops[brand];

        $(shopSelect).find('option').remove();
        $.each(brandShops, function(index, shop){
            shopSelect.append(new Option(shop, shop));
        });
        if(brandShops != undefined) {
            $(shopSelect).prop('disabled', '');
        } else {
            shopSelect.append(new Option("BRAK SKLEPU!", ""));
            $(shopSelect).prop('disabled', 'disabled');
        }
    }

    $(brandSelect).change(onBrandSelectChange);
})(jQuery);
