/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/
var stripePublic_key = $("#id_stripe_public_key").text().slice(1, -1);
var clientSecret = $("#id_client_secret").text().slice(1, -1);

function getStripeOneTime() {
  var stripe = Stripe(stripePublic_key);
  var elements = stripe.elements();
  var style = {
    base: {
      color: "#000",
      fontFamily: '"Open Sans", sans-serif',
      fontSmoothing: "antialiased",
      fontSize: "16px",
      "::placeholder": {
        color: "#6c757d"
      }
    },
    invalid: {
      color: "#dc3545",
      iconColor: "#dc3545"
    }
  };
  var card = elements.create("card", { style: style });
  card.mount(`.card-element`);
  // Handle realtime validation errors on the card element
  card.addEventListener("change", function (event) {
    var errorDiv = document.querySelector(`.card-errors`);
    if (event.error) {
      var html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${event.error.message}</span>`;
      $(errorDiv).html(html);
    } else {
      errorDiv.textContent = "";
    }
  });

  // Handle form submit
  var form = document.querySelector(`.payment-form`);

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    card.update({ disabled: true });

    $(`.submit-payment-form`).attr("disabled", true);
    $(`.payment-form`).fadeToggle(100);

    $("#loading-overlay").fadeToggle(100);

    var saveInfo = Boolean($(`.info-save`).prop("checked"));
    var csrfToken = $(
      `input[name="csrfmiddlewaretoken"]`
    ).val();
    var postData = {
      csrfmiddlewaretoken: csrfToken,
      client_secret: clientSecret,
      save_info: saveInfo
    };
    var url = "/checkout/cache_checkout_data/";

    $.post(url, postData)
      .done(function () {
        stripe
          .confirmCardPayment(clientSecret, {
            payment_method: {
              card: card,
              billing_details: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                email: $.trim(form.email.value),
                address: {
                  line1: $.trim(form.street_address1.value),
                  line2: $.trim(form.street_address2.value),
                  city: $.trim(form.town_or_city.value),
                  country: $.trim(form.country.value),
                  state: $.trim(form.county.value)
                }
              }
            },
            shipping: {
              name: $.trim(form.full_name.value),
              phone: $.trim(form.phone_number.value),
              address: {
                line1: $.trim(form.street_address1.value),
                line2: $.trim(form.street_address2.value),
                city: $.trim(form.town_or_city.value),
                country: $.trim(form.country.value),
                postal_code: $.trim(form.postcode.value),
                state: $.trim(form.county.value)
              }
            }
          })
          .then(function (result) {
            if (result.error) {
              var errorDiv = document.querySelector(
                `.card-errors`
              );
              var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
              $(errorDiv).html(html);
              $(`.payment-form`).fadeToggle(100);
              $("#loading-overlay").fadeToggle(100);
              card.update({ disabled: false });
              $(`.submit-payment-form`).attr(
                "disabled",
                false
              );
            } else {
              if (result.paymentIntent.status === "succeeded") {
                form.submit();
              }
            }
          });
      })
      .fail(function () {
        location.reload();
      });
  });
}

document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("checkout-form-container");
  var mobileContainer = document.querySelector(".checkout-mobile #order-form-content .card-body");
  var desktopContainer = document.querySelector(
    ".checkout-desktop .form-container"
  );

  function moveForm() {
    const isMobile = window.innerWidth < 992;

    if (isMobile) {
      if (!mobileContainer.contains(form)) {
        mobileContainer.appendChild(form);
      }
    } else {
      if (!desktopContainer.contains(form)) {
        desktopContainer.appendChild(form);
      }
    }
  }

  // Move on load
  moveForm();
  // Get stripe element on load
  getStripeOneTime(); 

  // Move on resize
  window.addEventListener("resize", moveForm);
});
