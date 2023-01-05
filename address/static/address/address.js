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
                $("#js-partial-address-form").html(data.html_form);
                $("#modal-address").modal("show");                
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
        var formdata = new FormData(form[0]);

        $.ajax({
            url: form.attr("action"),
            //data: form.serialize(),
            data: formdata,
            processData: false,
            contentType: false,
            type: form.attr("method"),
            dataType: 'json',
            enctype: 'multipart/form-data',
            success: function (data) {
                if (data.form_is_valid) {
                    alert(form.attr('crud') + ' Address Successfully');
                    $("#js-partial-addresses-management").html(data.html_partial_addresses_management);
                    $("#modal-address").modal("hide");  // <-- Close the modal	
                }
                else {
                    alert(form.attr('crud') + ' Address Failure')
                    $("#js-partial-address-form").html(data.html_form);
                    $("#modal-address").modal("show");
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

    $(document).on("submit", ".js-address-update", saveForm);
    $(document).on("submit", ".js-address-create", saveForm);
    
    $(document).on("click", ".js-address-create-form", loadForm);
    $(document).on("click", ".js-address-update-form", loadForm);
    
    $(document).on("submit", ".js-address-delete", saveForm);
    $(document).on("click", ".js-address-delete-form", loadForm);
});




