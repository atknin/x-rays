
var myOpts = document.getElementById('id_source').options;
$('#id_source').val(myOpts[1].value);
var canvas = new fabric.Canvas('fabric');
// Комментрарий в расчете со временем
var dt = new Date();
var time = dt.getHours() + "." + dt.getMinutes() + "." + dt.getSeconds();
$('#id_comment_calc').val($.datepicker.formatDate('yy/mm/dd ', new Date())+ time);

//--------- добавить источник --------------

var source = new fabric.Image(document.getElementById('source'), {
  left: 450,
  top: 93,
  angle: -15,
  opacity: 0.85,
  shadow: 'rgba(0,0,0,0.3) 5px 5px 5px',
  selectable: false,
  name: 'источник, нажмите для настройки',
  class: 'source'
});
source.scale(0.5);
canvas.add(source);

// --------- добавть детектор ---------------
var detector = new fabric.Image(document.getElementById('detector'), {
  left: 50,
  top: 118,
  angle: 15,
  width: 100,
  height: 30,
  opacity: 0.85,
  shadow: 'rgba(0,0,0,0.3) 5px 5px 5px',
  selectable: false,
  name: 'детектор, нажмите для настройки',
  class: 'detector'

});
detector.scale(0.5);
canvas.add(detector);


var slit_a = new fabric.Rect({
    width: 10,
    height: 20,
    left: 120,
    top: 135,
    fill: '#949494',
});

var sample = new fabric.Image(document.getElementById('sample'), {
    left: 186,
    top: 170,
    // angle: 30,
    opacity: 0.85,
  	selectable: false,
    shadow: 'rgba(0,0,0,0.3) 5px 5px 5px',
    name: 'кристалл, перетащите для установки',
    class: 'sample_1'
  });

  sample.scale(0.5);
  sample.hasControls = sample.hasBorders = false;
  canvas.add(sample);

var slit_b = new fabric.Rect({
    width: 10,
    height: 20,
    left: 120,
    top: 160,
    fill: '#949494',
});




var slit_1 = new fabric.Group([ slit_a, slit_b ], {
	left: 300,
	top: 120,
	selectable: false,
	angle: -15,
	class: 'slit_1',
	shadow: 'rgba(0,0,0,0.3) 1px 2px 5px',
});
canvas.add(slit_1);

var slit_2 = new fabric.Group([ slit_a, slit_b ], {
	left: 120,
	top: 120,
	angle: 15,
	selectable: false,
	class: 'slit_2',
	shadow: 'rgba(0,0,0,0.3) 1px 2px 5px',
});
canvas.add(slit_2);



$('.settings').hide();
canvas.on('mouse:down', function(options) {
	if (options.target) {
		$('.settings').hide();
		$('#sign_settings').hide();
		$('#div_settings_'+options.target.class).show();
	};
});


// ---------------------------------------------------------------------
var check_array = {'X0_1':false,'Xh_1':false};

check_array['input_l_slit1'] = true;
check_array['input_l_slit2'] = true;
check_array['input_size_slit1'] = true;
check_array['input_size_slit2'] = true;

check_array['source_divergence_arc'] = true;
check_array['id_source'] = true;

check_array['teta_start'] = true;
check_array['teta_end'] = true;
// ---------------------------------------------------------------------

function error(e){
	check_array[$(e).attr('id')] = false;
  	// console.log(check_array[$(e).attr('id')]);
  	$(e).addClass('error');
};
function ok(e){
	check_array[$(e).attr('id')] = true;
  	// console.log($(e).attr('id'),check_array[$(e).attr('id')]);
  	$(e).removeClass('error');
};

// ---------------ПРОВЕРКА---------------------------------------------
// Ассиметрия
$("#check_symmetric_case_1, #check_symmetric_case_2").change(function() {
  var nnn = $(this).attr('name');
  if(this.checked) {
    $('#h_index_surface_'+nnn+',#k_index_surface_'+nnn+',#l_index_surface_'+nnn).prop( "disabled", true );
    $('#h_index_surface_'+nnn+',#k_index_surface_'+nnn+',#l_index_surface_'+nnn).val('');
    $('#id_assym_img_'+nnn).hide();
    $('#select_crystal'+nnn).attr('size', 10);
  }
  else{
    $('#h_index_surface_'+nnn+',#k_index_surface_'+nnn+',#l_index_surface_'+nnn).prop( "disabled", false );
    $('#select_crystal'+nnn).attr('size', 2);
    $('#id_assym_img_'+nnn).show();
  };
});

$("#check_symmetric_case_1, #check_symmetric_case_2").change();
// '\ Ассиметрия


$('#x0_1,#xh_1,#x0_2,#xh_2').change(function() {
	var X = $(this).val().split('+');
 	if(X.length == 2){ok(this);}
 	else{error(this);}
});

$('#id_source').change(function() {
	ok(this);
	$('#x0_1').val('');
    $('#xh_1').val('');
    $('#x0_2').val('');
    $('#xh_2').val('');
});
$('#teta_start').change(function() {
  if ($('#teta_start').val()<$('#teta_end').val()){ok(this);}
  else{error(this);}
});
$('#teta_end').change(function() {
  if ($('#teta_start').val()<$('#teta_end').val()){ok(this);}
    else{error(this);}
});



// --------\\-------ПРОВЕРКА---------------------------------------------

var compute_dict = {};
$('#id_alert_message').hide();

// ------------------------------отправка расчта в Телеграмм
$("#compute").click(function(){
  $("#loader_addon").addClass("loader"); //анимациая загрузки
	$('#getX1').click();
	$('#getX2').click();
	$("#compute").prop( "disabled", true );
	var flag = true;
	var mes = '';
	for (var key in check_array){
		if (check_array[key]==false){
			error($('#'+key));
			flag = false;
			mes+=' |'+$('#'+key).attr('name')+'| ';
		}
		else{
			ok($('#'+key));
			compute_dict[key] = $('#'+key).val();
			console.log( $('#'+key).val());
		};
	};

	if (!flag){
		$('#id_alert_message').show();
		$('#id_alert_message').html('<span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span><span class="sr-only">Error:</span>'+mes)
	}
	else {
		$('#id_alert_message').hide();
		$.ajaxSetup({data: {
			csrfmiddlewaretoken: $('#abracadabraa').val()
		}});


		compute_dict['schem'] = 'single_crystal';
		compute_dict['id_email'] = $('#id_email').val();
		compute_dict['X0_1'] = $('#X0_1').val();
		compute_dict['Xh_1'] = $('#Xh_1').val();

		compute_dict['X0_2'] = $('#X0_2').val();
		compute_dict['Xh_2'] = $('#Xh_2').val();
		compute_dict['scan'] = $('input[name=schem_radio]').filter(':checked').val();

    compute_dict['teta_start'] = $('#teta_start').val();
    compute_dict['teta_end'] = $('#teta_end').val();
    compute_dict['computer_calculate'] = $('#id_pc').val();
    compute_dict["id_comment_calc"] = ' ' + $('#id_comment_calc').val();

    compute_dict['step_shag_teta'] = $('#step_shag_teta').val();
    compute_dict['step_teta'] = $('#step_teta').val();
    compute_dict['step_lambda'] = $('#step_lambda').val();

    if(document.getElementById('logarifm_scale').checked) {
        compute_dict['logarifm_scale'] = 'log';
    } else {
        compute_dict['logarifm_scale'] = 'Nonlog';
    };



		$.post("/diffraction/compute/", compute_dict)
		.done(function(msg) {
			alert( msg.status);
       $("#loader_addon").removeClass("loader");//убрать анимациая загрузки
		});
	};
});

// ------------------------------Расчет поляризуемости
$("#getX2, #getX1").click(function() {
  	var compute_dict_X = {};
  	var cryst_num = $(this).attr( "name" );
  	var flag = false

   if (!$.isNumeric($('#select_crystal'+cryst_num).val())){ // проверка, выбран ли источник
    flag = true;
    $("#check_crystal"+cryst_num).addClass("has-error");
  };
  if ($("#check_symmetric_case_"+cryst_num).is(":checked")){
      $('#h_index'+cryst_num+'_surface').val($('#h_index'+cryst_num).val());
      $('#k_index'+cryst_num+'_surface').val($('#k_index'+cryst_num).val());
      $('#l_index'+cryst_num+'_surface').val($('#l_index'+cryst_num).val());
    };

  if (flag != true) {
    $("#loader_addon"+cryst_num).addClass("loader"); //анимациая загрузки
    $.ajaxSetup({data: {
    	csrfmiddlewaretoken: $('#abracadabraa').val()
    }});
    compute_dict_X["h"] = $('#h_index'+cryst_num).val();
    compute_dict_X["k"] = $('#k_index'+cryst_num).val();
    compute_dict_X["l"] = $('#l_index'+cryst_num).val();

    if ($("#check_symmetric_case_"+cryst_num).is(":checked")){
      $('#h_index_surface_'+cryst_num).val($('#h_index'+cryst_num).val());
      $('#k_index_surface_'+cryst_num).val($('#k_index'+cryst_num).val());
      $('#l_index_surface_'+cryst_num).val($('#l_index'+cryst_num).val());
    }
    else if(!$.isNumeric($('#l_index_surface_'+cryst_num).val()) || !$.isNumeric($('#k_index_surface_'+cryst_num).val()) || !$.isNumeric($('#l_index_surface_'+cryst_num).val()) ) {
      console.log('индекс surface не задан')
      $('#h_index_surface_'+cryst_num).val($('#h_index'+cryst_num).val());
      $('#k_index_surface_'+cryst_num).val($('#k_index'+cryst_num).val());
      $('#l_index_surface_'+cryst_num).val($('#l_index'+cryst_num).val());
    }

    compute_dict_X["assym_alfa_then_beta"] = $('input[name=assym_alfa_then_beta_'+cryst_num+']').filter(':checked').val();

    compute_dict_X["h_surface"] = $('#h_index_surface_'+cryst_num).val();
    compute_dict_X["k_surface"] = $('#k_index_surface_'+cryst_num).val();
    compute_dict_X["l_surface"] = $('#l_index_surface_'+cryst_num).val();

    compute_dict_X["crystal_id"] = $('#select_crystal'+cryst_num).val();




    compute_dict_X["wavelength"] = $('#id_source').find('option:selected').attr("name");

    $.post("/polarizability/compute/", compute_dict_X ,function(data) {
      $('#X0_'+cryst_num).val(data.X0_real + " + "+data.X0_imag+"j");
      $('#Xh_'+cryst_num).val(data.Xh_real + " + "+data.Xh_imag+"j");
      ok($('#X0_'+cryst_num));
      ok($('#Xh_'+cryst_num));
      compute_dict['bragg_'+cryst_num] = data.bragg;
      compute_dict['fi_'+cryst_num] = data.fi;

      $("#loader_addon"+cryst_num).removeClass("loader");//убрать анимациая загрузки
    });
  };

});
// как только мы прикаснемся к одному из .. окон удалится класс окрасски
$("#check_crystal1,#check_crystal2").click(function(){
  $(this).removeClass("has-error");
});
$("#new_compute").click(function(){
  $("#compute").prop( "disabled", false );
});
