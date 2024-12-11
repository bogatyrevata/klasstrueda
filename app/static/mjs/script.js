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


  // //Test timer 3 min
  // var timer;
  // const promoMinutesEnd = 3; // Set to 3 minutes for testing
  // const timerKey = 'promoEndDate';

  // function getOrSetEndDate() {
  //   let endDate = localStorage.getItem(timerKey);
  //   if (endDate) {
  //     endDate = new Date(endDate);
  //     if (new Date() >= endDate) {
  //       // If the stored date has passed, set a new date
  //       endDate = setNewEndDate();
  //     }
  //   } else {
  //     // If there is no stored date, set a new date
  //     endDate = setNewEndDate();
  //   }
  //   return endDate;
  // }

  // function setNewEndDate() {
  //   let newEndDate = new Date();
  //   newEndDate.setMinutes(newEndDate.getMinutes() + promoMinutesEnd);
  //   localStorage.setItem(timerKey, newEndDate);
  //   return newEndDate;
  // }

  // function timeBetweenDates(toDate) {
  //   var dateEntered = toDate;
  //   var now = new Date();
  //   var difference = dateEntered.getTime() - now.getTime();

  //   if (difference <= 0) {
  //     // Timer done, set new end date and reset the timer
  //     toDate = setNewEndDate();
  //     difference = toDate.getTime() - now.getTime();
  //   }

  //   var seconds = Math.floor(difference / 1000);
  //   var minutes = Math.floor(seconds / 60);
  //   var hours = Math.floor(minutes / 60);
  //   var days = Math.floor(hours / 24);

  //   hours %= 24;
  //   minutes %= 60;
  //   seconds %= 60;

  //   $("#days").text(days);
  //   $("#hours").text(hours);
  //   $("#minutes").text(minutes);
  //   $("#seconds").text(seconds);

  //   return toDate; // Return updated end date
  // }

  // $(document).ready(function() {
  //   // Clear localStorage for testing purposes
  //   localStorage.removeItem(timerKey);

  //   var compareDate = getOrSetEndDate();

  //   timer = setInterval(function() {
  //     compareDate = timeBetweenDates(compareDate); // Update compareDate
  //   }, 1000);
  // });

  //Timer
    var timer;
    const timerKey = 'promoEndDate';
    let promoDayEnd = 5; // Изменение этой переменной автоматически меняет время акции

    function setNewEndDate() {
      let newEndDate = new Date();
      newEndDate.setDate(newEndDate.getDate() + promoDayEnd);
      localStorage.setItem(timerKey, newEndDate.toISOString());
      return newEndDate;
    }

    function getOrSetEndDate() {
      let endDate = localStorage.getItem(timerKey);
      if (endDate) {
        endDate = new Date(endDate);
        if (new Date() >= endDate) {
          // If the stored date has passed, set a new date
          endDate = setNewEndDate();
        }
      } else {
        // If there is no stored date, set a new date
        endDate = setNewEndDate();
      }
      return endDate;
    }

    function updateCompareDate() {
      compareDate = getOrSetEndDate();
    }

    function timeBetweenDates(toDate) {
      var dateEntered = toDate;
      var now = new Date();
      var difference = dateEntered.getTime() - now.getTime();

      if (difference <= 0) {
        // Timer done, set new end date and reset the timer
        toDate = setNewEndDate();
        difference = toDate.getTime() - now.getTime();
      }

      var seconds = Math.floor(difference / 1000);
      var minutes = Math.floor(seconds / 60);
      var hours = Math.floor(minutes / 60);
      var days = Math.floor(hours / 24);

      hours %= 24;
      minutes %= 60;
      seconds %= 60;

      $("#days").text(days);
      $("#hours").text(hours);
      $("#minutes").text(minutes);
      $("#seconds").text(seconds);

      return toDate; // Возвращаем обновленную дату
    }

    $(document).ready(function() {
      let compareDate = getOrSetEndDate();

      timer = setInterval(function() {
        compareDate = timeBetweenDates(compareDate);
      }, 1000);

      // Обработчик изменения promoDayEnd
      $('#promoDayEndInput').change(function() {
        promoDayEnd = parseInt($(this).val(), 10); // Парсим новое значение
        localStorage.setItem('promoDayEnd', promoDayEnd); // Сохраняем новое значение в localStorage
        updateCompareDate(); // Обновляем compareDate
      });
    });


    // Заполняем поле временной метки при загрузке формы, для того чтобы сделать проверку на бота
    document.getElementById('form_time').value = Date.now();


//Загрузка аватара в личном кабинете пользователя

const fileInput = document.getElementById("file-input");
const imagePreview = document.getElementById("img-preview");
const toast = document.getElementById("toast");

fileInput.addEventListener("change", (e) => {
  if (e.target.files.length) {
    const src = URL.createObjectURL(e.target.files[0]);
    imagePreview.src = src;
    showToast();
  }
});

function showToast() {
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 3000);
}

