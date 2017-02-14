function checkboxClick() {
    $('#forms').on('click', 'input:checkbox', undefined, function(){
        var checkbox = $(this);

        if (!checkbox.attr("checked")) {
            checkbox.removeAttr("value");
            checkbox.attr("checked", "");
        } else {
            checkbox.removeAttr("checked");
        }
    });
};

(function($){
    var formset = new Formset({
        "formsetID": "brands-formset",
        "errorMessage": "W bazie musi istnieć co najmniej jedna kategoria.",
    });

    checkboxClick();
})(jQuery);
