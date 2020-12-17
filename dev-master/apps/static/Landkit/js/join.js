$(document).ready(function () {
  var $plan_total_slots = JSON.parse(
    document.getElementById("plan_total_slots").textContent
  );
  var dictValues = JSON.parse(
    document.getElementById("dictValues").textContent
  );
  var $currentFamilySize = JSON.parse(
    document.getElementById("currentFamilySize").textContent
  );
  var $plan_price = JSON.parse(document.getElementById("plan_price").textContent);
  var $average_switch_status = JSON.parse(document.getElementById("average_switch_status").textContent);
    // console.debug();
  if($average_switch_status){
    //   Save Total Amount Value....
  var $total = 0;
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
    $total = dictValues[ parseInt($currentFamilySize) +  parseInt($elem_1)]* parseInt($elem_1);
    $("#subs_Section").html(5 * parseInt($elem_1));
    $("#paymentSub").html(
      parseFloat($total ).toFixed(2)
    );
    $("#plan-join-badge").html("$" + parseFloat($total ).toFixed(2).toString() + "/MO");
    $("#total").html(
      "$" +
        (
          parseFloat(
            parseFloat(
              $total
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
  $total = dictValues[ parseInt($currentFamilySize) +  parseInt($elem_1)]* parseInt($elem_1);
  
  $("#subs_Section").html(5 * parseInt($elem_1));
  $("#paymentSub").html(
    parseFloat($total ).toFixed(2)
  );
  $("#plan-join-badge").html("$" + parseFloat($total).toFixed(2).toString() + "/MO");
  
  $("#total").html(
    "$" +
      (
        parseFloat(
          parseFloat($total ).toFixed(
            2
          )
        ) + parseFloat(5 * parseInt($elem_1))
      ).toString() +
      " /month"
  );
  if ($("#total").html() == "$NaN") {
    $("#total").html("$" + "0" + "/month");
  }
  }
  else if(!$average_switch_status){
    // TODO:  console.info("FALSE");
    $("#GET_A_NUMBER, #EXISTING_CUSTOMER, #SWITCHING_CARRIER").val($("#exampleFormControlSelect1").val());
    
  // TODO:  Functionality for the number of guests selected from the join-detail plan page
  $("#exampleFormControlSelect1").on("change", function () {
    $("#GET_A_NUMBER, #EXISTING_CUSTOMER, #SWITCHING_CARRIER").val($("#exampleFormControlSelect1").val());
    var $elem_1 = $(this).children("option:selected").val();
    // $total = dictValues[ parseInt($currentFamilySize) +  parseInt($elem_1)]* parseInt($elem_1);
    $("#subs_Section").html(5 * parseInt($elem_1));
    $("#paymentSub").html(parseFloat($plan_price ).toFixed(2) * parseInt($elem_1)) ;
    $("#plan-join-badge").html("$" + parseFloat($plan_price).toFixed(2).toString()* parseInt($elem_1)+ "/MO");
    $("#total").html(
      "$" +(parseFloat(5 * parseInt($elem_1)) + parseFloat($plan_price ).toFixed(2) * parseInt($elem_1) )+" /month");
    });



    var $elem_1 = $("#exampleFormControlSelect1").children("option:selected").val();
    // $total = dictValues[ parseInt($currentFamilySize) +  parseInt($elem_1)]* parseInt($elem_1);
    $("#subs_Section").html(5 * parseInt($elem_1));
    $("#paymentSub").html(parseFloat($plan_price ).toFixed(2) * parseInt($elem_1)) ;
    $("#plan-join-badge").html("$" + parseFloat($plan_price).toFixed(2).toString()* parseInt($elem_1)+ "/MO");
    $("#total").html(
      "$" +(parseFloat(5 * parseInt($elem_1)) + parseFloat($plan_price ).toFixed(2) * parseInt($elem_1) )+" /month");

  }

  
});
