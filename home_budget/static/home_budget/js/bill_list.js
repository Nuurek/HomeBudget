function setUpElements() {
    var startDate = $('#id_start_date');
    var endDate = $('#id_end_date');

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
};

(function($){
    setUpElements();
})(jQuery);
