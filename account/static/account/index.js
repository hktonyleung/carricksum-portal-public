$(document).ready(function(){
    var saveForm = function (e) {
        e.preventDefault();
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    alert('Profile Update Successfully');
                    $("#js-profile-form").html(data.html_form);
                }
                else {
                    alert('Profile Update Failure')
                    $("#js-profile-form").html(data.html_form);
                }
            }
        });
    };

    $(document).on("submit", ".js-profile-update", saveForm);
});