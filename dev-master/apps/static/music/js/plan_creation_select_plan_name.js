function PlanCreationFunction(x, y) {$('#id_category').val(y).trigger('change');$("#id_plan_name_default").show();for (var i = 0; i < $("#selectContains").find("select").length; i++) {if ($($("#selectContains").find("select")[i]).attr("id") == ("id_plan_name_" + x + "")) {$($("#selectContains").find("select")[i]).show();$("#id_plan_name_default").hide();$($("#selectContains").find("select")[i]).attr("name", "plan_name");} else {$($("#selectContains").find("select")[i]).hide();if(x!="None" &&  y != "None"){$("#id_plan_name_default").hide();}else{$("#id_plan_name_default").show();}}}}