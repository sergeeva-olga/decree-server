function jqesc( myid ) {
  return "#" + myid.replace( /(:|\.|\[|\]|,|=|@)/g, "\\$1" );
};

function generateUUID () { // Public Domain/MIT
  var d = new Date().getTime();
  if (typeof performance !== 'undefined' && typeof performance.now === 'function'){
    d += performance.now(); //use high-precision timer if available
  }
  return 'xxxxxxxx-xxxx-8xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    var r = (d + Math.random() * 16) % 16 | 0;
    d = Math.floor(d / 16);
    return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
}

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
  setGEditEnabled(false);
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
  setGEditEnabled(true);
};

function setDatabaseEnabled(val) {
  $("#app-control-database").prop('disabled', ! val);
};

function setSaveEnabled(val) {
  $("#app-control-save").prop('disabled', ! val);
  $("#app-control-save-as").prop('disabled', ! val);
  $("menu button.show").prop('disabled', ! val);
};

function setGEditEnabled(val) {
  $("#app-control-medium-editor").prop('disabled', ! val);
};


var WIDGETS={
  "xsd:admcode": function (e, t) {
    e.attr("content", t);
    var ltrs = t.split("");
    e.empty();
    ltrs.forEach(function(l, i) {
      var first = i == 0 ? "-first":"";
      e.append(`<span class="admcodebox${first}">${l}</span>`);
    });
  }
};

function showWidget(e) {
  var dt = e.attr("datatype");
  var w = WIDGETS[dt];
  if (w != undefined) {
    var text = e.text().replace(/ /g, '');
    w(e, text);
  };
};

function propagateEditable() {
  var editables = $('[datatype]');
  editables.each(function(){
    var e = $(this);
    var val = e.text();
    var id = e.attr("id");
    showWidget(e);
    if (id != undefined) {
      var eid = jqesc(id);
      $(`${eid}:not([datatype])`).each(function(){
        var disp=$(this); // tag <span ... >
        var gen=disp.attr("data-case");
        var genF=disp.attr("data-f");
        var genM=disp.attr("data-m");
        var query;
        var ajaxConf={
            type: "POST",
            url: "/api/morphy",
            data: undefined,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(answer){
              disp.text(answer.phrase);
            },
            failure: function(errMsg) {
              alert(errMsg);
            }
        };

        if (gen != undefined) {
          query = {
            "phrase": val,
            "case": gen,
            "command": "all"
          };
        } else {
          query = {
            "command":"gender",
            "phrase": val,
            "F": genF,
            "M": genM
          };
        };
        ajaxConf.data=JSON.stringify(query);
        $.ajax(ajaxConf);
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
  function saveDocument(saveas, msg) {
    var container = $("#main-document-container");
    var text;
    var apiUrl, oldUUID;
    if (saveas) {
      apiUrl="save-as";
      var docroot=container.find("#main-document");
      var newUUID=generateUUID();
      oldUUID=docroot.attr("data-uuid");
      docroot.attr("data-uuid", newUUID);
      docroot.find("#main-uuid").attr("content", newUUID);
    } else {
      apiUrl="save";
    }
    text = container.html();
    $.ajax({
      type: "POST",
      url: `/api/${apiUrl}`,
      data: text,
      contentType: "application/x-xhtml, charset=utf-8",
      dataType: "json",
      success: function(answer){
        // FIXME: User could not see the message in save-as mode.
        $("#message").html(alert_widget("success", msg));
        if (saveas) {
          location.href = location.href.replace(oldUUID, newUUID);
        }
      },
      failure: function(errMsg) {
        $("@message").html(alert_widget("alert", errMsg));
      }
      });
  };
  $('#app-control-save').click(function(){
    saveDocument(false, "Документ успешно сохранен!");
  });
  $('#app-control-save-as').click(function(){
    saveDocument(true, "Теперь вы работаете в новом документе!");
  });
  $("#app-control-medium-editor").click(function(){
    // var editor = new MediumEditor('#main-document-container', {
    var editor = new MediumEditor('.editable');

    $("#message").html(alert_widget("success", "Включен редактор."));
  });
  $("#app-control-database").click(function(){
    // $("#message").html(alert_widget("success", "Доступ к хранилищу."));
  });
  $("[datatype]").addClass("edit");
  propagateEditable();
  // setupEditMode();
});
