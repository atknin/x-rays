
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

var check_array = {'input_l_slit1':'true','input_l_slit2':'true', 'input_size_slit1':'true', 'input_size_slit2':'true','source_divergence_arc':'true','source_to_backend':'false'}


function error(e){
	check_array[$(e).attr('id')] = 'false';
  	console.log(check_array[$(e).attr('id')]);
  	$(e).addClass('error');
};
function ok(e){
	check_array[$(e).attr('id')] = 'true';
  	console.log($(e).attr('id'),check_array[$(e).attr('id')]);
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


$("#compute").prop( "disabled", false );
$("#compute").click(function(){
	for (var key in check_array){
		if (check_array['key']==='false'){
			console.log('error ', key);
		}
		else{
			console.log('ok ', key);
		};
	}


	// if(!false in )
	// compute_dict['edit'] = 'true';
	// compute_dict['crystal_id'] = $("#crystal_id").val();
	// $.ajaxSetup({data: {
	// csrfmiddlewaretoken: '{{ csrf_token }}'
	// }});
	// $.post("/polarizability/add_crystal/", compute_dict ,function(data) {
	// var info_2 = info
	// info_2 +=data.status+'\n'
	// $( '#info_geometry' ).val(info_2);
	// aler('Успешно');
	// window.location.replace("/polarizability/");
	// });

});

