// Set up Stripe.js and Elements to use in checkout form
var stripe = Stripe('pk_test_7Caol5AeV11tgvLYCf7FlGXr00hMYbhIfm');

var elements = stripe.elements();
 /* Card Element */
    var card = elements.create("card", {
      iconStyle: "solid",
      style: {
        base: {
          iconColor: "black",
          color: "black",
          fontWeight: 400,
          fontFamily: "Helvetica Neue, Helvetica, Arial, sans-serif",
          fontSize: "16px",
          fontSmoothing: "antialiased",
  
          "::placeholder": {
            color: "black"
          },
          ":-webkit-autofill": {
            color: "#fff"
          }
        },
        invalid: {
          iconColor: "#FFC7EE",
          color: "#FFC7EE"
        }
      }
    });
    card.mount("#example5-card");


var form = document.getElementById('subscription-form');
//------------------------------------------------------------------------------

var first_name = document.getElementById('example5-name');
// var last_name = document.getElementById('last_name');
var Phone_number = document.getElementById('example5-phone');
var emailid = document.getElementById('example5-email');
var City = document.getElementById('example5-city');
var State = document.getElementById('example5-state');
// var Country = document.getElementById('Country');
var Gresponse = document.getElementById("recaptcha_join");




// Addition by suleman...
var category_id = document.getElementById("category_id_join");
var plan_id = document.getElementById("plan_id_join");
var number_of_slots = document.getElementById("slots");



//-------------------------------------------------------------------------------



form.addEventListener('submit', function(event) {

  // To strop browser default behaviour
  event.preventDefault();
  event.stopPropagation();
  // Hide Device Compatibility Modal
  // $("#exampleModalDevice").modal("hide");
  
  
  $('.button-loader').button('loading');
  if ($("#subscription-form")[0].checkValidity() == true || ($("#example5-state :selected").val() == "None")  )
  {
    if($("#example5-state :selected").val() == "None")
    {
      $("#selectTagError").show(); 
      form.classList.add('was-validated');
    }
    else{
      $("#selectTagError").hide(); 
      $('.button-loader').button('loading');
      stripe.createPaymentMethod({
        type: 'card',
        card: card,
        billing_details: {
          email: emailid.value,
          name:(first_name.value),
          phone:Phone_number.value,
          address: {
            "city": City.value,
            "country": 'US',
            "postal_code": null,
            "state": State.value
          },
    
        },
    
    
      }).then(stripePaymentMethodHandler);
    }
    
  }
  
  else{
    form.classList.add('was-validated');
  }
  

 
});

function stripePaymentMethodHandler(result, email) {



  $('.button-loader').button('loading');

  // **************** Billing Address **************************** //
  // var B_address_line1 = document.getElementById('B_address_line1');
  // var B_address_line2 = document.getElementById('B_address_line2');
  // var B_City = document.getElementById('B_City');
  // var B_State = document.getElementById('B_State');
  // var B_Postal_code = document.getElementById('B_Postal_Code');
  // var B_Country = document.getElementById('B_Country');

  // // **************** Shipping Address **************************** //
  var C_address_line1 = document.getElementById('example5-address');
  // var C_address_line2 = document.getElementById('address_2');
  var C_City = document.getElementById('example5-city');
  var C_State = document.getElementById('example5-state');
  var C_Postal_code = document.getElementById('example5-zip');

  var device_IMEI = [];
  var device_area_codes = [];
  // console.log(device_IMEI);
  for(var i= 0 ;i < $("[name='IMEI']").length; i++)
  {
    if(($("[name='IMEI']")[i].value.trim() != ""))
    {
      device_IMEI.push($("[name='IMEI']")[i].value);  
    }  
    
  }




  for(var i= 0 ;i < $("[name='AreaCode']").length; i++)
  {
    if(($("[name='AreaCode']")[i].value.trim() != ""))
    {
      device_area_codes.push($("[name='AreaCode']")[i].value);  
    }  
    
  }


  // Area Code Manipulations
  
  

  // var C_Country = document.getElementById('Country');
  // document.getElementById("submit_button").style.display = "nonoe";
  // document.getElementById("payment-loading").style.display = "block";

  if (result.error) {

    // On an error show Device Compatibility Modal
    $("#exampleModalDevice").modal("show");

    // Hide Processing Order Modal
    $("#exampleModalpayment_processing_waiting_modal").modal("hide");

    // Show Payment Checkout Form Modal
    $("#exampleModalPaymentError").css("z-index", "99999999");
    $("#exampleModalPaymentErrorBody").html("");
    $("#exampleModalPaymentErrorBody").append((result.error.message));
    $("#exampleModalPaymentError").modal("show");
    $('.button-loader').button('reset');
    
  } 
  else 
  {

    // ! Hide Device Compatibility Modal
    $("#exampleModalDevice").modal("hide");

    // ! Hide Payment Error
    $("#exampleModalPaymentError").modal("hide");

    // ! Hide Payment End Modal
    $("#end_payment_exampleModal").modal("hide");

    // ! Show Payment Processing Modal
    $("#exampleModalpayment_processing_waiting_modal").modal("show");
    

    $('.button-loader').button('reset');
    // ! Otherwise send paymentMethod.id to your server
    fetch('/charge', {
      method: 'post',
      credentials: "same-origin",
      headers: {'Content-Type': 'application/json'},

      body: JSON.stringify({

        payment_method: result.paymentMethod.id,
        card: result.paymentMethod.card,
        details: result.paymentMethod.billing_details,
        brand:result.paymentMethod.card.brand,
        category_id :category_id.value,
        plan_id:plan_id.value,
        C_address_line1: C_address_line1.value,
        C_address_line2: '',
        C_Postal_code:C_Postal_code.value,
        C_City: C_City.value,
        C_State:C_State.value,
        C_Country:'US',
        number_of_slots : number_of_slots.value,
        device_IMEI : device_IMEI,
        subs_contact : document.getElementById("switch_1").value,
        subs_account : document.getElementById("switch_2").value,
        subs_PIN : document.getElementById("switch_3").value,
        mobile_carrier : document.getElementById("switch_4").value,
        phone:Phone_number.value,
        Gresponse:Gresponse.value,
        joiningCondition:document.getElementById("joiningCondition").value,
        area_codes : device_area_codes,
      }),

    }).then(function(result) {
      $("#exampleModalPaymentError").modal("hide");
      $("#exampleModalDevice").modal("hide");
      $("#exampleModalpayment_processing_waiting_modal").modal("hide");
      $('.button-loader').button('reset');
      $("#exampleModalpayment_error").modal("hide");
      $("#IMEI_2").val("");
      $("#IMEI_1").val("");
      if (result.status != 200){
        $("#exampleModalpayment_error").modal("show");
        $("#exampleModalpayment_processing_waiting_modal").modal("hide");
      }
      else{
        $("#exampleModalpayment_error").modal("hide");
        $("#exampleModalpayment_processing_waiting_modal").modal("hide");
        // $("#end_payment_exampleModal").modal("show");
      }
      return result.json();
    }).then(function(data){
      $("#exampleModalpayment_error_body").val("");
      // $("#end_payment_exampleModal").modal("show");
      $("#exampleModalpayment_processing_waiting_modal").modal("hide");
      if(data["error"]){
        $("#exampleModalpayment_error_body").val(data["error"]);
        $("#exampleModalpayment_processing_waiting_modal").modal("hide");
      }
      else{
        $("#exampleModalpayment_error").modal("hide");
        $("#end_payment_exampleModal").modal("show");
        $("#exampleModalpayment_processing_waiting_modal").modal("hide");
      }
    }).catch(function(error) {
      $("#exampleModalPaymentError").modal("hide");
      $("#exampleModalDevice").modal("hide");
      $("#exampleModalpayment_processing_waiting_modal").modal("hide");
      $("#exampleModalpayment_processing_waiting_modal").modal("hide");
      // $("#end_payment_exampleModal").modal("hide");
      $("#exampleModalpayment_error").modal("show");
      $("#exampleModalpayment_error_body").val("");
      $("#exampleModalpayment_error_body").val(error);
    });
  }
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}