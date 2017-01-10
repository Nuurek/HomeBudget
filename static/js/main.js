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

(function($){

})(jQuery);
