
$('#btn_0_cryst').click(function(event) {
	$('#div_choose_howmanycrystals').hide(); 
	$('#div_zero_crystal').show();

});

var canvas = new fabric.Canvas('fabric');

//--------- добавить источник --------------

var source = new fabric.Image(document.getElementById('source'), {
  left: 650,
  top: 125,
  // angle: 30,
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
  left: 250,
  top: 135,
  // angle: 30,
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
    left: 320,
    top: 135,
    fill: '#949494',
});

var slit_b = new fabric.Rect({
    width: 10,
    height: 20,
    left: 320,
    top: 160,
    fill: '#949494',
});




var slit_1 = new fabric.Group([ slit_a, slit_b ], {
	left: 500,
	top: 120,
	selectable: false,
	class: 'slit_1',
	shadow: 'rgba(0,0,0,0.3) 1px 2px 5px',
});
canvas.add(slit_1);

var slit_2 = new fabric.Group([ slit_a, slit_b ], {
	left: 320,
	top: 120,
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

var check_array = {'input_l_slit1':true,'input_l_slit2':true, 'input_size_slit1':true, 'input_size_slit2':true,'source_divergence_arc':true,'source_to_backend':false}


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
$('#source_to_backend').change(function() {
	ok(this);

});
var compute_dict = {}

$('#id_alert_message').hide();
$("#compute").prop( "disabled", false );
$("#compute").click(function(){
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
		
		// $.ajaxSetup({data: {
		// 	csrfmiddlewaretoken: '{{ csrf_token }}'
		// }});
		compute_dict['csrfmiddlewaretoken'] = '{{ csrf_token }}'
		$.ajax({

		  type: "POST",
		  url: "/diffraction/compute/",
		  data: compute_dict,
		  success: function(msg){
		        alert( "Status: " + msg );
		  },
		  error: function(XMLHttpRequest, textStatus, errorThrown) {
		     alert("some error");
		  }
		});

		// $.post("/diffraction/compute/", compute_dict)
		// 	.done(function(msg) {
		// 	    alert( msg.status);
		// 	});
	};


});

