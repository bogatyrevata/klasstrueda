(function ($) {
  "use strict";

  // Spinner
  var spinner = function () {
      setTimeout(function () {
          if ($('#spinner').length > 0) {
              $('#spinner').removeClass('show');
          }
      }, 1);
  };
  spinner();

  // Initiate the wowjs
  new WOW().init();

  // Sticky Navbar
  $(window).scroll(function () {
      if ($(this).scrollTop() > 300) {
          $('.sticky-top').addClass('shadow-sm').css('top', '0px');
      } else {
          $('.sticky-top').removeClass('shadow-sm').css('top', '-100px');
      }
  });


  // Back to top button
  $(window).scroll(function () {
      if ($(this).scrollTop() > 300) {
          $('.back-to-top').fadeIn('slow');
      } else {
          $('.back-to-top').fadeOut('slow');
      }
  });

  $('.back-to-top').click(function () {
      $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
      return false;
  });


  // Testimonials carousel
  $(".testimonial-carousel").owlCarousel({
      autoplay: true,
      smartSpeed: 1000,
      items: 1,
      dots: true,
      loop: true,
  });
})(jQuery);


  // Workphoto carousel
$(".workphoto-carousel").owlCarousel({
    autoplay: true,
    smartSpeed: 1000,
    dots: true,
    loop: true,
    responsiveClass:true,
    responsive:{
        0:{
            items:1,
        },
        768:{
            items:2,
        },
        1200:{
            items:3,
        }
    }
  });

  // Workphoto-single-carousel
  $(".workphoto-single-carousel").owlCarousel({
    autoplay: true,
    smartSpeed: 1000,
    items: 1,
    dots: true,
    loop: true,
    responsiveClass:true,
});

// Получаем формы с помощью querySelector
const registrationForm = document.querySelector("#registration");
const paymentForm = document.querySelector("#payment");

// Функция для установки текущего времени в input
function setFormTime(form) {
    const formTimeInput = form.querySelector("input[name='form_time']");
    if (formTimeInput) {
        formTimeInput.value = Date.now();
    }
}

// Проверяем наличие каждой формы и устанавливаем время
if (registrationForm) {
    setFormTime(registrationForm);
}

if (paymentForm) {
    setFormTime(paymentForm);
}

//Загрузка аватара в личном кабинете пользователя

const fileInput = document.getElementById("file-input");
const imagePreview = document.getElementById("img-preview");
const toast = document.getElementById("toast");

if (fileInput) {
  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length) {
      const src = URL.createObjectURL(e.target.files[0]);
      imagePreview.src = src;
      showToast();
    }
  });
}

function showToast() {
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 3000);
}

