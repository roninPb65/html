/* faq script*/
var que = document.getElementsByClassName("question");
var i;

for (i = 0; i < que.length; i++) {
    
  que[i].addEventListener("click", function() {
    this.classList.toggle("active-faq");
    var answer = this.nextElementSibling;
    if (answer.style.maxHeight){
        answer.style.maxHeight = null;
    } else {
        answer.style.maxHeight = answer.scrollHeight + "px";
    } 
  });
}


const splash = document.querySelector('.splash');

document.addEventListener('DOMContentLoaded', (e)=>{
  
  setTimeout(()=>{
      splash.classList.add('display-none');
      console.log("hello")
  }, 2000);
})


