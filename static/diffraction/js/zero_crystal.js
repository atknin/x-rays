
$('#btn_0_cryst').click(function(event) {
	$('#div_choose_howmanycrystals').hide(); 
	$('#div_zero_crystal').show();
var canvas = new fabric.Canvas('fabric');

var crystal1 = new fabric.Rect({
  width: 30,
  height: 30,
  left: 10,
  top: 10,
  stroke: '#aaf',
  strokeWidth: 1,
  fill: '#eee',
  selectable: false,
  name: 'на это место можно установить кристалл',
  class: 'place_sample1'
});
crystal1.scale(0.5)
canvas.add(crystal1);

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
});

