
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
  class: 'source_settings'
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


var rect1 = new fabric.Rect({
    width: 10,
    height: 25,
    left: 320,
    top: 155,
    fill: '#949494',
    selectable: false
});

var rect2 = new fabric.Rect({
    width: 10,
    height: 25,
    left: 320,
    top: 110,
    fill: '#949494',
    selectable: false
});

var group1 = new fabric.Group([ rect1, rect2 ], {
	angle: 45
	left: 320,
	top: 110,
});

canvas.add(group1);
