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
            $("#js-partial-branch-form").html(data.html_form);
            $("#modal-branch").modal("show");
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
                    alert(form.attr('crud') + ' Branch Successfully');
                    $("#js-partial-branches-management").html(data.html_partial_branches_management);
                    $("#modal-branch").modal("hide");  // <-- Close the modal	
                }
                else {
                    alert(form.attr('crud') + ' Branch Failure');
                    $("#js-partial-branch-form").html(data.html_form);
                    $("#modal-branch").modal("show");
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

    $(document).on("submit", ".js-branch-delete", saveForm);
    $(document).on("submit", ".js-branch-create", saveForm);
    $(document).on("submit", ".js-branch-update", saveForm);

    $(document).on("click", ".js-branch-delete-form", loadForm);
    $(document).on("click", ".js-branch-create-form", loadForm);
    $(document).on("click", ".js-branch-update-form", loadForm);

    $("#modal-branch").on('hidden.bs.modal', function (e) {
        // do something...
        $("#js-partial-branch-form").html('');

    })
    $("#modal-branch").on('shown.bs.modal', function(){
        console.log('shown');
        setTimeout(function () {
            map.invalidateSize();
        }, 100);
        
        if (typeof $('#geojson_branch').val() === 'undefined' 
            || $('#geojson_branch').val() == ''
            || $('#geojson_branch').val() == 'None' ) {
            
                console.log('is None');
                map.locate()
                .on('locationfound', e => map.setView(e.latlng, 16))
                .on('locationerror', () => map.setView([22.302711, 114.177216], 8));
        } else {
            console.log($('#geojson_branch').val());
            var geojson_branch = JSON.parse($('#geojson_branch').val());
            var geoJSONgroup = L.geoJSON(geojson_branch, {
                onEachFeature: onEachFeature
            }).addTo(map);
            geoJSONgroup.eachLayer(function (layer) {
                    map.fitBounds(layer.getBounds());
            });            
        }


    });


});
