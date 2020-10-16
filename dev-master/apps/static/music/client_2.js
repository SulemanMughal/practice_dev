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
//------------------------------------------------------------------------------

var first_name = document.getElementById('first_name');
var last_name = document.getElementById('last_name');
var email_id = document.getElementById("emailid");
var Phone_number = document.getElementById('id_contactNumber');
var City = document.getElementById('City');
var State = document.getElementById('State');
var Country = document.getElementById('Country');


//-------------------------------------------------------------------------------


form.addEventListener('submit', function(event) {
  // We don't want to let default form submission happen here,
  // which would refresh the page.
  event.preventDefault();

  stripe.createPaymentMethod({
    type: 'card',
    card: cardElement,
    billing_details: {
      email: email_id.value,
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


  }).then(stripePaymentMethodHandler);
});

function stripePaymentMethodHandler(result, email) {
  if (result.error) {
    alert(object.getOwnPropertyNames(result))
  } else {
    // Otherwise send paymentMethod.id to your server
    fetch('/charge', {
      method: 'post',
      credentials: "same-origin",
      headers: {'Content-Type': 'application/json'},

      body: JSON.stringify({
       
        payment_method: result.paymentMethod.id,
        card: result.paymentMethod.card,
        details: result.paymentMethod.billing_details,

      }),
   
    }).then(function(result) {
     //window.open('http://127.0.0.1:8000/admin/')
      window.location.replace('/profile')
      return result.json();

    }).then(function(customer) {
      // 
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