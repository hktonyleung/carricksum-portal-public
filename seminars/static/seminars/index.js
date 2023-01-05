$(document).ready(function(){
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),  
            type: 'get',
            data: { 
            },
            dataType: 'json',
            beforeSend: function () {
            },
            success: function (data) {
                $("#js-partial-seminar-form").html(data.html_form);
                $("#modal-seminar").modal("show");                
            }
        });
    };

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
                    alert('Save Seminar Successfully');
                    $("#js-partial-seminars-management").html(data.html_partial_seminars_management);
                    $("#modal-seminar").modal("hide");  // <-- Close the modal	
                }
                else {
                    alert('Save Seminar Failure')
                    $("#js-partial-seminar-form").html(data.html_form);
                    $("#modal-seminar").modal("show");
                }
            },
            complete: function(){
                // Handle the complete event
            },
            error: function (jqXHR, exception) {
                // Handle the complete event
                //console.log('error:' + jqXHR.responseText);
                //alert('error:' + jqXHR.responseText);
                alert('Server Error: ' + jqXHR.status +  ' Please contact administrator');
            }
        });
    };

    $(document).on("submit", ".js-seminar-update", saveForm);
    $(document).on("submit", ".js-seminar-create", saveForm);
    
    $(document).on("click", ".js-seminar-create-form", loadForm);
    $(document).on("click", ".js-seminar-update-form", loadForm);
    
    $(document).on("submit", ".js-seminar-delete", saveForm);
    $(document).on("click", ".js-seminar-delete-form", loadForm);
});




