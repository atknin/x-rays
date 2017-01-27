
var myOpts = document.getElementById('id_source').options;
$('#id_source').val(myOpts[1].value);
var canvas = new fabric.Canvas('fabric');

//--------- добавить источник --------------

var source = new fabric.Image(document.getElementById('source'), {
  left: 450,
  top: 177,
  angle: 15,
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

var sample1 = new fabric.Image(document.getElementById('sample'), {
    left: 186,
    top: 170,
    // angle: 30,
    opacity: 0.85,
  	selectable: false,
    shadow: 'rgba(0,0,0,0.3) 5px 5px 5px',
    name: 'кристалл, перетащите для установки',
    class: 'sample_1'
  });

  sample1.scale(0.5);
  sample1.hasControls = sample1.hasBorders = false;
  canvas.add(sample1);

 var sample2 = new fabric.Image(document.getElementById('sample'), {
    left: 380,
    top: 90,
    angle: 180,
    opacity: 0.85,
  	selectable: false,
    shadow: 'rgba(0,0,0,0.3) 5px 5px 5px',
    name: 'кристалл, перетащите для установки',
    class: 'sample_1'
  });

  sample2.scale(0.5);
  sample2.hasControls = sample2.hasBorders = false;
  canvas.add(sample2);

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
var check_array = {'input_l_slit1':true,'input_l_slit2':true, 'input_size_slit1':true, 'input_size_slit2':true,'source_divergence_arc':true,'id_source':true,'X0':false,'Xh':false}


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
$("#check_symmetric_case").change(function() {
  if(this.checked) {
  	console.log('ok')
    $('#h_index1_surface,#k_index1_surface,#l_index1_surface').prop( "disabled", true );
    $('#h_index1_surface,#k_index1_surface,#l_index1_surface').val('');
  }
  else{
    $('#h_index1_surface,#k_index1_surface,#l_index1_surface').prop( "disabled", false );
  }
});
$("#check_symmetric_case").change();

$('#input_l_slit1, #input_l_slit2').keyup(function() {
  if( parseFloat($(this).val()) < 2 && parseFloat($(this).val()) > 0){ok(this);}
  else{error(this);}
});

$('#input_size_slit1, #input_size_slit2').keyup(function() {
  if( parseFloat($(this).val()) < 100 && parseFloat($(this).val()) > 0){ok(this);}
  else{error(this);}
});

$('#source_divergence_arc').change(function() {
  if( parseFloat($(this).val()) < 2000 && parseFloat($(this).val()) > 0){ok(this);}
  else{error(this);}
});

$('#X0,#Xh').change(function() {
	var X = $(this).val().split('+');
 	if(X.length == 2){ok(this);}
 	else{error(this);}
});

$('#id_source').change(function() {
	ok(this);
	$('#x0_1').val('');
    $('#xh_1').val('');

});
var compute_dict = {};

$('#id_alert_message').hide();
$("#compute").click(function(){
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
		compute_dict['X0'] = $('#X0').val();
		compute_dict['Xh'] = $('#Xh').val();
		compute_dict['scan'] = $('input[name=schem_radio]').filter(':checked').val()


		
		$.post("/diffraction/compute/", compute_dict)
		.done(function(msg) {
			alert( msg.status);
		});
	};


});

$("#getX1").click(function() {
	console.log('compute');
  	var compute_dict_X = {};
  	var cryst_num = $(this).attr( "name" );
  	var flag = false
 

   if (!$.isNumeric($('#select_crystal1').val())){ // проверка, выбран ли источник
    flag = true;   
    $("#check_crystal"+cryst_num).addClass("has-error");
  };
  if ($("#check_symmetric_case").is(":checked")){
      $('#h_index1_surface').val($('#h_index1').val());
      $('#k_index1_surface').val($('#k_index1').val());
      $('#l_index1_surface').val($('#l_index1').val());
    };

  if (flag != true) { 
    $("#loader_addon"+cryst_num).addClass("loader"); //анимациая загрузки
    $.ajaxSetup({data: {
    	csrfmiddlewaretoken: $('#abracadabraa').val()
    }});
    compute_dict_X["h"] = $('#h_index1').val();
    compute_dict_X["k"] = $('#k_index1').val();
    compute_dict_X["l"] = $('#l_index1').val();
    compute_dict_X["h_surface"] = $('#h_index1_surface').val();
    compute_dict_X["k_surface"] = $('#k_index1_surface').val();
   	compute_dict_X["l_surface"] = $('#l_index1_surface').val();

    compute_dict_X["crystal_id"] = $('#select_crystal1').val();

    compute_dict_X["wavelength"] = $('#id_source').find('option:selected').attr("name");

    $.post("/polarizability/compute/", compute_dict_X ,function(data) {
      $('#X0').val(data.X0_real + " + "+data.X0_imag+"j");
      $('#Xh').val(data.Xh_real + " + "+data.Xh_imag+"j");
      ok($('#X0'));
      ok($('#Xh'));
      $("#loader_addon"+cryst_num).removeClass("loader");//убрать анимациая загрузки
    });
  }; 

});
// как только мы прикаснемся к одному из .. окон удалится класс окрасски
$("#check_crystal1").click(function(){
  $(this).removeClass("has-error");
});
$("#new_compute").click(function(){
  $("#compute").prop( "disabled", false );
});

      

