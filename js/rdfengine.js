function jqesc( myid ) {
  return "#" + myid.replace( /(:|\.|\[|\]|,|=|@)/g, "\\$1" );
};
function setupEditMode() {
  var editables = $('[datatype]');
  editables.each(function(){
    var e = $(this);
    var val = e.text();
    e.wrapInner(`<input value="${val}" class="edit-field form-inline" />`);
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
      var disps = $(`${eid}:not([datatype])`).text(val);
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
    var uri="http://irnok.net/fake-doc.html";
    var store = $rdf.graph();
    var mdoc = $("html").html();
    var mimeType = "application/xhtml+xml";
    try {
      $rdf.parse(mdoc, store, uri, mimeType);
    } catch (err) {
      alert("Error:"+err);
    }
    // var triples=store.each(undefined, undefined, undefined);
    alert (store.length);
    // alert(JSON.stringify(data));
  });
  propagateEditable();
  // setupEditMode();
});
