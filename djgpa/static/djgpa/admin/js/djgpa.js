(function ($) {
    $(document).ready(function () {
        $('<a href="#" id="generate"> generate</a>').insertAfter(
            '#id_android_id');

        $('#generate').click(function() {
            $.get('/get_new_android_id/', function(data) {
                if (data != 'ERROR') {
                    $('#id_android_id').val(data);
                } else {
                    alert('Can not get new android id!');
                };
            });
        });
    });
})(django.jQuery);
