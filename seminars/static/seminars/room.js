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
                $("#js-partial-room-form").html(data.html_form);
                $("#modal-room").modal("show");                
            },
            complete: function(){
                // Handle the complete event
            },
            error: function (jqXHR, exception) {
                // Handle the complete event
                alert('Please contact administrator');
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
                    alert(form.attr('crud') + ' Room Successfully');
                    $("#js-partial-rooms-management").html(data.html_partial_rooms_management);
                    $("#modal-room").modal("hide");  // <-- Close the modal	
                }
                else {
                    alert(form.attr('crud') + ' Room Failure')
                    $("#js-partial-room-form").html(data.html_form);
                    $("#modal-room").modal("show");
                }
            },
            complete: function(){
                // Handle the complete event
            },
            error: function (jqXHR, exception) {
                // Handle the complete event
                alert('Server Error: ' + jqXHR.status + ' Please contact administrator');
            }
        });
    };

    $(document).on("submit", ".js-room-update", saveForm);
    $(document).on("submit", ".js-room-create", saveForm);
    
    $(document).on("click", ".js-room-create-form", loadForm);
    $(document).on("click", ".js-room-update-form", loadForm);
    
    $(document).on("submit", ".js-room-delete", saveForm);
    $(document).on("click", ".js-room-delete-form", loadForm);
});




