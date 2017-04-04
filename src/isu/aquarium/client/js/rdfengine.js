function jqesc( myid ) {
  return "#" + myid.replace( /(:|\.|\[|\]|,|=|@)/g, "\\$1" );
};
function setupEditMode() {
  var editables = $('[datatype]');
  editables.each(function(){
    var e = $(this);
    var val = e.text();
    var size = val.trim().length;
    if (size < 5) { size = 5; };
    size = Number(size * 1.2);
    e.wrapInner(`<input value="${val}" class="edit-field form-inline" size="${size}" />`);
  });
};
function setupDispMode() {
  var editables = $('.edit-field');
  editables.each(function(){
    var f = $(this);
    var e = f.parent();
    var val = f.val();
    e.empty();
    e.text(val);
  });
  propagateEditable();
};


function propagateEditable() {
  var editables = $('[datatype]');
  editables.each(function(){
    var e = $(this);
    var val = e.text();
    var id = e.attr("id");
    if (id != undefined) {
      var eid = jqesc(id);
      $(`${eid}:not([datatype])`).each(function(){
        var disp=$(this); // tag <span ... >
        var gen=disp.attr("data-case");
        if (gen != undefined) {
          var query = {
            "phrase": val,
            "case": gen,
            "all": true
          };
          $.ajax({
            type: "POST",
            url: "/api/morphy",
            data: JSON.stringify( query ),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(answer){
              disp.text(answer.phrase);
            },
            failure: function(errMsg) {
              alert(errMsg);
            }
          });
        };
      });
    };
  });
};

$(document).ready(function(){
  $("#app-control-button").click(function(){
    // $("p").hide();
    // $("#person").text($("#person_name").val());
    var b = $(this);
    var phase=b.attr("data-phase");
    var icon=$("#app-control-button-icon");
    icon.attr("class","fa");
    if (phase == "edit") {
      icon.addClass("fa-edit");
      b.attr("data-phase", "disp");
      setupDispMode();
    } else {
      icon.addClass("fa-eye");
      b.attr("data-phase", "edit");
      setupEditMode();
    }
  });
  $('#app-control-save').click(function(){
    var docroot=$("#main-document");
    var text = docroot.html();
    $.ajax({
      type: "POST",
      url: "/api/save",
      data: text,
      contentType: "application/x-xhtml, charset=utf-8",
      dataType: "json",
      success: function(answer){
        $("#message").html(`<div class="alert alert-success"
                            role="alert">Документ успешно сохранен!</div>&nbsp;&nbsp;&nbsp;`);
      },
      failure: function(errMsg) {
        alert(errMsg);
      }
    });
  });
  $("[datatype]").addClass("edit");
  propagateEditable();
  // setupEditMode();
});
