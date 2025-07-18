/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

function getStripeOneTime(containerClass) {
  var stripe_public_key = $("#id_stripe_public_key").text().slice(1, -1);
  var client_secret = $("#id_stripe_public_key").text().slice(1, -1);
  var stripe = Stripe(stripe_public_key);
  var elements = stripe.elements();
  var style = {
    base: {
      color: "#000",
      fontFamily: '"Open Sans", sans-serif',
      fontSmoothing: "antialiased",
      fontSize: "16px",
      "::placeholder": {
        color: "#6c7581"
      },
    },
    invalid: {
      color: "#dc3545",
      iconColor: "#dc3545"
    }
  };
  var card = elements.create("card", { style: style });
  card.mount(`.${containerClass} .card-element`);
  // Handle realtime validation errors on the card element
  card.addEventListener('change', function (event) {
        var errorDiv = document.querySelector(`.${containerClass} .card-errors`);
        if (event.error) {
            var html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${event.error.message}</span>`;
            $(errorDiv).html(html);
        } else {
            errorDiv.textContent = '';        
        }
    });
}

window.addEventListener("resize", function (event) {
  if (document.body.clientWidth >= 992) {
    if ($(".checkout-desktop .card-element").children().length == 0) {
      getStripeOneTime("checkout-desktop");
    }
  } else {
    if ($(".checkout-mobile .card-element").children().length == 0) {
      getStripeOneTime("checkout-mobile");
    }
  }
});

  if (document.body.clientWidth >= 992) {
    if ($(".checkout-desktop .card-element").children().length == 0) {
      getStripeOneTime("checkout-desktop");
    }
  } else {
    if ($(".checkout-mobile .card-element").children().length == 0) {
      getStripeOneTime("checkout-mobile");
    }
  }
