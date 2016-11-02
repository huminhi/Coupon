// Countdown
$(function() {
	$('.countdown').each(function(){
		var count = $(this);
		$(this).countdown({
			zeroCallback: function(options) {
				var newDate = new Date(),
					newDate = newDate.setHours(newDate.getHours() + 130);

				$(count).attr("data-countdown", newDate);
				$(count).countdown({
					unixFormat : true
				});
			}
		});
	});
});

$(document).ready(function() {
    $('.carousel').carousel({
      interval: 6000
    });
});


$(window).load(function() {
    $('#nivo-slider').nivoSlider({
    	prevText: '',
    	nextText: ''
    });
});

$(function(){
	$('#flexnav').flexNav();
});

// Lighbox gallery
$('#popup-gallery').each(function () {
    $(this).magnificPopup({
        delegate: 'a.popup-gallery-image',
        type: 'image',
        gallery: {
            enabled: true
        }
    });
});

// Lighbox gallery
$('#popup-gallery').each(function () {
    $(this).magnificPopup({
        delegate: 'a.popup-gallery-image',
        type: 'image',
        gallery: {
            enabled: true
        }
    });
});

// Lighbox image
$('.popup-image').magnificPopup({
    type: 'image'
});

// Lighbox text
$('.popup-text').magnificPopup({
    removalDelay: 500,
    closeBtnInside: true,
    callbacks: {
        beforeOpen: function () {
            this.st.mainClass = this.st.el.attr('data-effect');
        }
    },
    midClick: true
});

// Lightbox iframe
$('.popup-iframe').magnificPopup({
    dispableOn: 700,
    type: 'iframe',
    removalDelay: 160,
    mainClass: 'mfp-fade',
    preloader: false
});


// Bootstrap tooltips
$('[data-toggle="tooltip"]').tooltip();
	$(function($){
     $("#twitter").tweet({
       username: "remtsoy", //!paste here your twitter username!
       count: 3
     });
   });


// Bootstrap accordion
$('.accordion').on('show', function (e) {
    $(e.target).prev('.accordion-heading').find('.accordion-toggle').addClass('active');
});

$('.accordion').on('hide', function (e) {
    $(e.target).prev('.accordion-heading').find('.accordion-toggle').removeClass('active');
});

$("#accordion-toggle .collapse").collapse();


$(function ($) {
    $("#twitter").tweet({
        username: "remtsoy",
        count: 3
    });
});


$(function($){
  $("#twitter-ticker").tweet({
    username: "remtsoy", //!paste here your twitter username!
    page: 1,
    count: 20
  });
});

$(document).ready(function(){
var ul = $('#twitter-ticker').find(".tweet-list");
  var ticker = function() {
    setTimeout(function() {
      ul.find('li:first').animate( {marginTop: '-9em', opacity: 0}, 700, function() {
        $(this).detach().appendTo(ul).removeAttr('style');
      });
      ticker();
    }, 5000);
  };
  ticker();
});
$(function(){
  $('#gmap').gmap3({
    marker:{
      address: "Haltern am See, Weseler Str. 151" // ENTER YOUR ADDRESS HERE!
    },
    map:{
      options:{
        zoom: 14
      }
    }
  });
});
 $(function() {
      $('#wilto-slider-wrap').wiltoSlider();
    });

// Self Hosted video plugin
$('audio,video').mediaelementplayer();

// Responsive videos
$(document).ready(function () {
    $("body").fitVids();
});

// Sticky navigation
$(document).ready(function() {
    if($('body').hasClass('sticky-header')) {
      var theLoc = $('header.main').position().top;
      $(window).scroll(function() {
          if(theLoc >= $(window).scrollTop()) {
              if($('header.main').hasClass('fixed')) {
                  $('header.main').removeClass('fixed');
              }
          } else {
              if(!$('header.main').hasClass('fixed')) {
                  $('header.main').addClass('fixed');
              }
          }
      });
    }
});

$(document).ready(function() {
    if($('body').hasClass('sticky-search')) {
      var theLoc = $('.search-area').position().top;
      if($('body').hasClass('sticky-header')) {
        var header_h = $('header.main').outerHeight();
      } else {
        header_h = 0;
      }

      $(window).scroll(function() {
          if(theLoc >= $(window).scrollTop()) {
              if($('.search-area').hasClass('fixed')) {
                  $('.search-area').removeClass('fixed').css({top: 0});
              }
          } else {
              if(!$('.search-area').hasClass('fixed')) {
                  $('.search-area').addClass('fixed').css({top: header_h});
              }
          }
      });
    }
});

$(document).ready(function(){
    $("img.lazy").lazyload({
        event : "sporty",
        effect : "fadeIn"
    });
});

// $(window).bind("load", function() {
//     var timeout = setTimeout(function() {
//         $("img.lazy").trigger("sporty")
//     }, 5000);
// });