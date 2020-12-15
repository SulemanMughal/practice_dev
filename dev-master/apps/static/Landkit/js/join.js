$(document).ready(function () {
  var $currentFamilySize = JSON.parse(
    document.getElementById("currentFamilySize").textContent
  );
  var $plan_total_slots = JSON.parse(
    document.getElementById("plan_total_slots").textContent
  );
  var dictValues = JSON.parse(
    document.getElementById("dictValues").textContent
  );
  $currentFamilySize = parseInt($currentFamilySize) + 1;

  //   Save Total Amount Value....
  var $total = 0;
  for (var key in dictValues) {
    if (dictValues.hasOwnProperty(key)) {
    }
  }
  $("#GET_A_NUMBER, #EXISTING_CUSTOMER, #SWITCHING_CARRIER").val(
    $("#exampleFormControlSelect1").val()
  );
  // TODO:Functionality for the number of guests selected from the join-detail plan page
  $("#exampleFormControlSelect1").on("change", function () {
    $("#GET_A_NUMBER, #EXISTING_CUSTOMER, #SWITCHING_CARRIER").val(
      $("#exampleFormControlSelect1").val()
    );
    $total = 0;
    var $elem_1 = $(this).children("option:selected").val();
    for (var i = 1; i < $plan_total_slots + parseInt($elem_1) + 1; i++) {
      $total += dictValues[i];
    }
    $("#subs_Section").html(5 * parseInt($elem_1));
    $("#paymentSub").html(
      parseFloat($total / ($plan_total_slots + parseInt($elem_1))).toFixed(2)
    );
    $("#total").html(
      "$" +
        (
          parseFloat(
            parseFloat(
              $total / ($plan_total_slots + parseInt($elem_1))
            ).toFixed(2)
          ) + parseFloat(5 * parseInt($elem_1))
        ).toString() +
        " /month"
    );
  });

  var $elem_1 = $("#exampleFormControlSelect1")
    .children("option:selected")
    .val();
  $total = 0;
  for (var i = 1; i < $plan_total_slots + parseInt($elem_1) + 1; i++) {
    $total += dictValues[i];
  }
  $("#subs_Section").html(5 * parseInt($elem_1));
  $("#paymentSub").html(
    parseFloat($total / ($plan_total_slots + parseInt($elem_1))).toFixed(2)
  );
  $("#total").html(
    "$" +
      (
        parseFloat(
          parseFloat($total / ($plan_total_slots + parseInt($elem_1))).toFixed(
            2
          )
        ) + parseFloat(5 * parseInt($elem_1))
      ).toString() +
      " /month"
  );
  if ($("#total").html() == "$NaN") {
    $("#total").html("$" + "0" + "/month");
  }
});
