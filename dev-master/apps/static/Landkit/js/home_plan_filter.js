$(document).ready(function () {var $grid = $("#portfolio").isotope({ layoutMode: "fitRows" });$('[data-target="#portfolio"]').on("click", function () {var i = $(this).attr("id");if (i == "all") {for (var j = 0; j < $(".plan_name").length; j++) {$("#" + $($(".plan_name")[j]).attr("id") + "").addClass("d-none").hide().css("visibility", "none");}} else {$("#btn_" + i + "").removeClass("d-none");$("#btn_" + i + "").show();}var filterValue = $(this).attr("data-filter");$grid.isotope({ filter: filterValue });});$("#id_category").on("change", function () {var i = $('[data-target="plan_name"]');for (var j = 0; j < i.length; j++) {$(i[j]).hide();$(i[j]).removeAttr("name", "plan_name");}$("#id_plan_name_" + $("#id_category :selected").attr("data-slug") + "").show().attr("name", "plan_name");$("#id_category_invalid-feedback").hide();$("#id_category").removeClass("border border-danger");});});