var myModal = new bootstrap.Modal(document.getElementById("documentModal"), {});

$(document).ready(function(){
    var searchAddress = function (e) {
        e.preventDefault();
        var form = $(this);

        $.ajax({
            url: form.attr("search-action"),
            data: 'query=' + $('#search').val(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid){
                    $(".result").html(data.html_form);
                } else {
                    $(".result").html("Empty result");
                }

            },
            complete: function(){
                // Handle the complete event
            },
            error: function (jqXHR, exception) {
                // Handle the complete event
                //console.log('error:' + jqXHR.responseText);
                //alert('error:' + jqXHR.responseText);
                alert('Server Error: ' + jqXHR.status + ' Please contact administrator');
            }
        });
    };

    $('#search').autocomplete({
        delay: 500,
        minLength: 3,
        source: function (request, response) {
            $.ajax( {
                url: $('#search-form').attr("action"),
                data: 'query=' + $('#search').val(),
                type: 'get',
                dataType: 'json',
                success: function (data) { 
                    //if (data.count >0){
                        response($.map(data.results, function (item) {
                            return {
                                label: item.fullAddress,
                                value: item.fullAddress,            
                            };
                        }));                        
                    //}

                }
              })
        }
    });

    var loadPopup = function (e) {
        e.preventDefault();
        $('#modalFrame').attr('src', 'about:blank');
        url = 'https://docs.google.com/gview?url=' + $(this).attr('href') +'&embedded=true'
        setTimeout(function() {
            $('#modalFrame').attr('src', url);
        }, 500);
        myModal.show();
    };

    $(document).on("submit", "#search-form", searchAddress);
    $(document).on("click", ".js-address-document", loadPopup);
    
});