
  $(document).on('ready', function() {
    $(".center").slick({
      dots: true,
      infinite: true,
      centerMode: true,
      slidesToShow: 3,
      slidesToScroll: 1
    });
  });




function makeLine(id, squiggleCount) {
  var curve;
  var lineEl = $(id);

  for (var i = 0; i < squiggleCount; i++) {
    curve = document.createElement('div');
    curve.className = 'curve-1';
    lineEl.append(curve);

    curve = document.createElement('div');
    curve.className = 'curve-2';
    lineEl.append(curve);
  }
}
$(document).ready(function(){
    makeLine('#line', 3);
});