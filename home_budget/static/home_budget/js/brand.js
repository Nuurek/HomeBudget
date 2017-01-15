function setUpBrandName() {
    var brandName = $('#id_nazwa');
    var editButton = $('#brand-name-edit');
    var icon = $(editButton.find('span'));

    editButton.click(function(){
        editButton.blur();
        icon.removeAttr('class');

        if (brandName.attr('disabled')) {
            brandName.removeAttr('disabled');
            icon.attr('class', 'glyphicon glyphicon-ok');
        } else {
            brandName.attr('disabled', '');
            icon.attr('class', 'glyphicon glyphicon-edit');
        }
    });
}

(function($){
    setUpBrandName();
})(jQuery);
