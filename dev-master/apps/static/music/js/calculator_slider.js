function updateSlider() {
  var z = $('[name="totalcostAmount"]');
  var w = $("#savings_amount");
  var w1 = $('div#mobileView>#savings_amount');
  var results = 0;
  if ($("#options1").is(":checked")) {
    if ($("#options_accounts1").is(":checked")) {
      results = parseFloat(parseFloat(z.val()) - 1 * 30) * 12;
    } else if ($("#options_accounts2").is(":checked")) {
      results = parseFloat(parseFloat(z.val()) - 2 * 30) * 12;
    } else if ($("#options_accounts3").is(":checked")) {
      results = parseFloat(parseFloat(z.val()) - 3 * 30) * 12;
    } else if ($("#options_accounts4").is(":checked")) {
      results = parseFloat(parseFloat(z.val()) - 4 * 30) * 12;
    }
  }
  if ($("#options2").is(":checked")) {
    if ($("#options_accounts1").is(":checked")) {
      results = parseFloat(parseFloat(z.val()) - 1 * 30) * 12;
    } else if ($("#options_accounts2").is(":checked")) {
      results = parseFloat(parseFloat(z.val()) - 2 * 30) * 12;
    } else if ($("#options_accounts3").is(":checked")) {
      results = parseFloat(parseFloat(z.val()) - 3 * 30) * 12;
    } else if ($("#options_accounts4").is(":checked")) {
      results = parseFloat(parseFloat(z.val()) - 4 * 30) * 12;
    }
  }
  if ($("#options3").is(":checked")) {
    if ($("#options_accounts1").is(":checked")) {
      results = parseFloat(parseFloat(z.val()) - 1 * 35) * 12;
    } else if ($("#options_accounts2").is(":checked")) {
      results = parseFloat(parseFloat(z.val()) - 2 * 35) * 12;
    } else if ($("#options_accounts3").is(":checked")) {
      results = parseFloat(parseFloat(z.val()) - 3 * 35) * 12;
    } else if ($("#options_accounts4").is(":checked")) {
      results = parseFloat(parseFloat(z.val()) - 4 * 35) * 12;
    }
  }
  if ($("#options4").is(":checked")) {
    if ($("#options_accounts1").is(":checked")) {
      results = parseFloat(parseFloat(z.val()) - 1 * 35) * 12;
    } else if ($("#options_accounts2").is(":checked")) {
      results = parseFloat(parseFloat(z.val()) - 2 * 35) * 12;
    } else if ($("#options_accounts3").is(":checked")) {
      results = parseFloat(parseFloat(z.val()) - 3 * 35) * 12;
    } else if ($("#options_accounts4").is(":checked")) {
      results = parseFloat(parseFloat(z.val()) - 4 * 35) * 12;
    }
  }
  if (results < 0) {
    $("#negative_results,  div#mobileView>#negative_results").removeClass("d-none");
    $("#dollar_results, #year_results, #savings_amount, div#mobileView>#dollar_results, div#mobileView>#year_results, div#mobileView>#savings_amount").addClass("d-none");
  } else {
    if (isNaN(results)) {
      results = 0;
    }
    var R = results;
    String(R).replace(/(.)(?=(\d{3})+$)/g, "$1,");
    w.html(String(R).replace(/(.)(?=(\d{3})+$)/g, "$1,"));
    w1.html(String(R).replace(/(.)(?=(\d{3})+$)/g, "$1,"));
    $("#negative_results, div#mobileView>#negative_results").addClass("d-none");
    $("#dollar_results, #savings_amount, #year_results, div#mobileView>#dollar_results, div#mobileView>#year_results, div#mobileView>#savings_amount").removeClass("d-none");
  }
}
