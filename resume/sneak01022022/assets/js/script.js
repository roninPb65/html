// function myall() {
//     document.getElementById("Web").style.display="block";
//     document.getElementById("Pho").style.display="block";
//     document.getElementById("App").style.display="block";
//     document.getElementById("Brad").style.display="block";
//   }

// function myBranding() {
//     document.getElementById("Web").style.display="none";
//     document.getElementById("Pho").style.display="none";
//     document.getElementById("App").style.display="none";
//     document.getElementById("Brad").style.display="block";
//   }


//   function myWeb() {
//     document.getElementById("Brad").style.display="none";
//     document.getElementById("Pho").style.display="none";
//     document.getElementById("App").style.display="none";
//     document.getElementById("Web").style.display="block";
//   }


//   function myPhotography() {
//     document.getElementById("Web").style.display="none";
//     document.getElementById("Brad").style.display="none";
//     document.getElementById("App").style.display="none";
//     document.getElementById("Pho").style.display="block";
//   }


//   function myApp() {
//     document.getElementById("Web").style.display="none";
//     document.getElementById("Pho").style.display="none";
//     document.getElementById("Brad").style.display="none";
//     document.getElementById("App").style.display="block";
//   }








const filterButtons = document.querySelector("#filter-btns").children;
const items = document.querySelector(".portfolio-gallery").children;
 
for (let i = 0; i < filterButtons.length; i++) {
    filterButtons[i].addEventListener("click", function () {
        for (let j = 0; j < filterButtons.length; j++) {
            filterButtons[j].classList.remove("active")
        }
        this.classList.add("active");
        const target = this.getAttribute("data-target")
 
        for (let k = 0; k < items.length; k++) {
            items[k].style.display = "none";
            if (target == items[k].getAttribute("data-id")) {
                items[k].style.display = "block";
            }
            if (target == "all") {
                items[k].style.display = "block";
            }
        }
 
    })
}





