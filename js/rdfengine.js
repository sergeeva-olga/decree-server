function jqesc( myid ) {
  return "#" + myid.replace( /(:|\.|\[|\]|,|=|@)/g, "\\$1" );
};
function setupEditMode() {
  var editables = $('.edit');
  editables.each(function(){
    var e = $(this);
    var val = e.text();
    var eid = e.attr("id");
    e.wrapInner(`<input value="${val}" id="${eid}-editable" class="edit-field"/>`);
  });
};
function setupDispMode() {
  var editables = $('.edit-field');
  editables.each(function(){
    var f = $(this);
    var e = f.parent();
    var eid = e.attr("id");
    var val = f.val();
    e.empty();
    e.text(val);
  });
  propagateEditable();
};
function propagateEditable() {
  var editables = $('.edit');
  editables.each(function(){
    var e = $(this);
    var val = e.text();
    var eid = jqesc(e.attr("id")); // # is already added.
    var disps = $(`${eid}.disp`).text(val);
  });
};

$(document).ready(function(){
  $("#app-control-button").click(function(){
    // $("p").hide();
    // $("#person").text($("#person_name").val());
    var b = $(this);
    var phase=b.attr("data-phase");
    if (phase == "edit") {
      b.text("Редактировать");
      b.attr("data-phase", "disp");
      setupDispMode();
    } else {
      b.text("Посмотреть");
      b.attr("data-phase", "edit");
      setupEditMode();
    }
  });
  $('#app-control-save').click(function(){
    var jsdata=new Object();
    var docroot=$("#main-document");
    var editables = docroot.find(".edit");
    data = jsdata["main-document"] = new Object();
    editables.each(function(){
      var e = $(this);
      var val = e.text();
      var eid = e.attr("id");
      var parts = eid.split(".");
      var d = data;
      parts.slice(0, -1).forEach(function(part, idx, arr){
        if (part in d) {
        } else {
          d[part]=new Object();
        };
        d=d[part];
      });

      d[parts[parts.length - 1]]=val;

    });
    alert(JSON.stringify(data));
  });
  propagateEditable();
  // setupEditMode();
});
