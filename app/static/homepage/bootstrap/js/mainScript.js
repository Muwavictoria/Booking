// navbar toggle\
let navBar = document.querySelector('.navLinks');
let menuBar = document.querySelector('#menuBtn');

menuBar.onclick =() =>{
    navBar.classList.toggle('active');

}

// scroll section and sticky navbar
window.onscroll = () => {
    let header = document.querySelector('header');

    header.classList.toggle('sticky', window.scrollY > 100);
}

// swiiper 
document.addEventListener('DOMContentLoaded', function () {
  var swiper = new Swiper(".myHome", {
    spaceBetween: 30,
    centeredSlides: true,
    loop:true,
    autoplay: {
      delay: 2500,
      disableOnInteraction: false,
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });
});


// client
document.addEventListener('DOMContentLoaded', function () {
  var swiper = new Swiper(".myClient", {
    slidesPerview:1,
    spaceBetween: 10,
    centeredSlides: true,
    loop:true,
    autoplay: {
      delay: 3000,
      disableOnInteraction: false,
    },
   breakpionts:{
    640: {
      slidesPerview:1,
      spaceBetween: 20,
    },
    768: {
      slidesPerview:2,
      spaceBetween: 10,
    },
    1024: {
      slidesPerview:3,
      spaceBetween: 10,
    },
   }
  });
});


