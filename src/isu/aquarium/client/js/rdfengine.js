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
  setDatabaseEnabled(false);
  setSaveEnabled(false);
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
  setDatabaseEnabled(true);
  setSaveEnabled(true);
};

function setDatabaseEnabled(val) {
  $("#app-control-database").prop('disabled', ! val);
};

function setSaveEnabled(val) {
  $("#app-control-save").prop('disabled', ! val);
  $("#app-control-save-as").prop('disabled', ! val);
  $("menu button.show").prop('disabled', ! val);
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

function alert_widget(level, message) {
  var icon = {
    "danger":"ban",
    "success":"check"
  }[level];
  return `<div class="alert alert-${level} alert-dismissible" role="alert">
<button type="button" class="close" data-dismiss="alert" aria-label="Close">
    <span aria-hidden="true">&times;</span>
  </button>
  <i class="icon fa fa-${icon}"></i>&nbsp;&nbsp;&nbsp;
  ${message}
</div>`
}

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
    var container = $("#main-document-container");
    var text = container.html();
    $.ajax({
      type: "POST",
      url: "/api/save",
      data: text,
      contentType: "application/x-xhtml, charset=utf-8",
      dataType: "json",
      success: function(answer){
        $("#message").html(alert_widget("success", "Документ успешно сохранен!"));
      },
      failure: function(errMsg) {
        alert(errMsg);
      }
      });

  });
  $("#app-control-database").click(function(){
    alert("Save");
  });
  $("[datatype]").addClass("edit");
  propagateEditable();
  // setupEditMode();
});
