$(document).ready(function() {
  $("#myForm").submit(function(e) {
    // prevent from normal form behaviour
    e.preventDefault();
    // serialize the form data
    var serializedData = $(this).serialize();
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $.ajax({
      type: "POST",
      url: "/items/post-item",
      headers: {
        "X-CSRFToken": csrftoken
      },
      data: serializedData,

      dataType: "json",
      contentType: "application/json",
      success: function(response) {
        //reset the form after successful submit
        $("#myForm")[0].reset();
      },
      error: function(response) {
        console.log(response);
      }
    });
  });
});
