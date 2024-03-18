
    var headerIndex = 1;
    showDivH(headerIndex);
    
    function plusDivs(h) {
      showDivH(headerIndex += h);
    }
    
    function showDivH(h) {
      var j;
      var w = document.getElementsByClassName("sub-slider");
      if (h > w.length) {headerIndex = 1}
      if (h < 1) {headerIndex = w.length}
      for (j = 0; j < w.length; j++) {
        w[j].style.display = "none";  
      }
      w[headerIndex-1].style.display = "block";  
    }






    var slideIndex = 1;
    showSlides(slideIndex);
    
    function plusSlides(n) {
      showSlides(slideIndex += n);
    }
    
    function currentSlide(n) {
      showSlides(slideIndex = n);
    }
    
    function showSlides(n) {
      var i;
      var slides = document.getElementsByClassName("myteam");
      var dots = document.getElementsByClassName("dot");
      if (n > slides.length) {slideIndex = 1}    
      if (n < 1) {slideIndex = slides.length}
      for (i = 0; i < slides.length; i++) {
          slides[i].style.display = "none";  
      }
      for (i = 0; i < dots.length; i++) {
          dots[i].className = dots[i].className.replace(" active", "");
      }
      slides[slideIndex-1].style.display = "block";  
      dots[slideIndex-1].className += " active";
    }







