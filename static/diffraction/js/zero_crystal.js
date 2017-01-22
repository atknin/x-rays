
$('#btn_0_cryst').click(function(event) {
	$('#div_choose_howmanycrystals').hide(); 
	$('#div_zero_crystal').show();

});

var canvas = new fabric.Canvas('fabric');
canvas.setBackgroundImage("{% static 'diffraction/img/background.png' %}", canvas.renderAll.bind(canvas));

var crystal1 = new fabric.Rect({
  width: 30,
  height: 30,
  left: 570,
  top: 135,
  stroke: '#aaf',
  strokeWidth: 1,
  fill: '#FAFAFA',
  selectable: false,
  name: 'на это место можно установить кристалл',
  class: 'place_sample1'
});
crystal1.scale(0.5)
canvas.add(crystal1);