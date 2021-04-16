$(function() {
  /* Functions */

  var loadForm = function() {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: "get",
      dataType: "json",
      beforeSend: function() {
        $("#modal-book .modal-content").html("");
        $("#modal-book").modal("show");
      },
      success: function(data) {
        $("#modal-book .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function() {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: "json",
      success: function(data) {}
    });
    return false;
  };

  /* Binding */

  // Create book
  $(".js-create-book").click(loadForm);
  // $("#modal-book").on("submit", ".js-book-create-form", saveForm);

  // Update book
  $("#table_id").on("click", ".js-update-book", loadForm);
  // $("#modal-book").on("submit", ".js-book-update-form", saveForm);

  // Delete book
  $("#table_id").on("click", ".js-delete-book", loadForm);
  // $("#modal-book").on("submit", ".js-book-delete-form", saveForm);
});
