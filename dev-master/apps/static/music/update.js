// Set up Stripe.js and Elements to use in checkout form
var stripe = Stripe('pk_test_7Caol5AeV11tgvLYCf7FlGXr00hMYbhIfm');

var elements = stripe.elements();

var style = {
  base: {
    color: '#32325d',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4',
    },
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a',
  },
};

var cardElement = elements.create('card', { style: style });
cardElement.mount('#card-element');
var form = document.getElementById('subscription-form');
var emailid = document.getElementById("emailid");

form.addEventListener('submit', function(event) {
  // We don't want to let default form submission happen here,
  // which would refresh the page.
  event.preventDefault();
  event.stopPropagation();
  if ($("#subscription-form")[0].checkValidity() == true || ($("#State :selected").val() == "None")  )
  {
    if($("#State :selected").val() == "None")
    {
      $("#selectTagError").show(); 
      form.classList.add('was-validated');
    }
    else{
      $("#selectTagError").hide(); 
      stripe.createPaymentMethod({
        type: 'card',
        card: cardElement,
        billing_details: {
          email: emailid.value,
          name:(first_name.value).concat(last_name.value) 
          ,
          phone:Phone_number.value,
          address: {
            "city": City.value,
            "country": Country.value,
            "postal_code": null,
            "state": State.value
          },
         
        },
    
      }).then(change);
    }
  }
  else{
    form.classList.add('was-validated');
  }

  
});

function change(result, email) {
  if (result.error) {
    // $("#exampleModalAdd_paymen_method_errorLabelBody").append(result.error.message);
    // $("#exampleModalAdd_paymen_method_error").show();

    $("#exampleModalPayment").modal("show");

    // Hide Processing Order Modal
    

    // Show Payment Checkout Form Modal
    $("#exampleModalAdd_paymen_method_error").css("z-index", "99999999");
    $("#exampleModalAdd_paymen_method_errorLabelBody").append((result.error.message));
    $("#exampleModalAdd_paymen_method_error").modal("show");
    
    
  } else {
    // Hide Payment Method Modal
    $("#exampleModalPayment").modal("hide");

    // Hide Payment Error
    $("#exampleModalAdd_paymen_method_error").modal("hide");

    // Show Payment Processing Modal
    $("#exampleModaladd_payment_method_waiting").modal("show");

    // Otherwise send paymentMethod.id to your server
    fetch('/add_card', {
      method: 'post',
      credentials: "same-origin",
      headers: {'Content-Type': 'application/json'},

      body: JSON.stringify({
       
        payment_method: result.paymentMethod.id,
        card: result.paymentMethod.card,
        details: result.paymentMethod.billing_details,
        brand:result.paymentMethod.card.brand,
      }),
   
    }).then(function(result) {
      window.location.replace('/profile-payment')

      return result.json();
    }).then(function(customer) {
      
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