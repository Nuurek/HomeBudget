function setUpElements() {
    var startDate = $('#id_start_date');
    var endDate = $('#id_end_date');
    var brand = $('#id_brand');
    var shop = $('#id_shop_id');

    var options = {
        format: "dd.mm.yyyy",
        weekStart: 1,
        todayBtn: "linked",
        language: "pl",
        keyboardNavigation: false,
        todayHighlight: true
    };

    startDate.datepicker(options);
    endDate.datepicker(options);
    brand.select2();
    shop.select2();
};

(function($){
    setUpElements();
})(jQuery);
