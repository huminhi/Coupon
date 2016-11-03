$(function () {
    $('.countdown').countdown({
        until: +103600,
        format: 'DHMS',
        layout: '<div class="days"><span class="count"></span>{dn}<span class="title">Days</span></div>' +
                '<div class="hours"><span class="count"></span>{hn}<span class="title">Hours</span></div>' +
                '<div class="minutes"><span class="count"></span>{mn}<span class="title">Minutes</span></div>' +
                '<div class="seconds"><span class="count"></span>{sn}<span class="title">Seconds</span></div>'
    });
});

// $(function() {
//     $(".lazy").lazyload({
//         effect : "fadeIn",
//         container: $("#thumbnail-container")
//     });
// });