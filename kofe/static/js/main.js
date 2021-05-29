$('.addToBasket').click(function(){
    var elements = document.getElementsByClassName('user_y');
    for (var i = 0; i < elements.length; i++) {
        elements[i] = 0;
        elements[i].value = parseInt(window.pageYOffset);
    }
})
$('.arrowMobile').click(function(){
    $('.arrow').toggleClass('active');
    $('.arrowMobile').toggleClass('active');
    $('.addressMenuMainPage').toggleClass('active');
})
$('.arrowMobileNotMobile').click(function(){
    $('.arrowNotMobile').toggleClass('active');
    $('.arrowMobileNotMobile').toggleClass('active');
    $('.addressMenuMainPageNotMobile').toggleClass('active');
})
$('.mainAuth').click(function(){
    $('.arrow').removeClass('active');
    $('.arrowNotMobile').removeClass('active');
    $('.addressMenuMainPage').removeClass('active');
    $('.addressMenuMainPageNotMobile').removeClass('active');
})
$('.registrationButton').click(function(){
    $('.registration').addClass('active');
    $('.authorization').removeClass('active');
    $('.information').removeClass('active');
    $('.registrationButton').removeClass('active');
    $('.description').addClass('active');
})
$('.registrationButtonMobile').click(function(){
    $('.registrationMobile').addClass('active');
    $('.authorizationMobile').removeClass('active');
    $('.informationMobile').removeClass('active');
    $('.descriptionMobile').addClass('active');
})
$('.openAuth').click(function(){
    $('.registration').removeClass('active');
    $('.authorization').addClass('active');
    $('.information').removeClass('active');
    $('.registrationButton').addClass('active');
    $('.description').removeClass('active');
})
$('.openAuthMobile').click(function(){
    $('.registrationMobile').removeClass('active');
    $('.authorizationMobile').addClass('active');
    $('.informationMobile').removeClass('active');
    $('.descriptionMobile').removeClass('active');
})
$('.defaultUserPhoto').click(function(){
    $('.registration').removeClass('active');
    $('.authorization').addClass('active');
    $('.information').removeClass('active');
    $('.registrationButton').addClass('active');
    $('.description').removeClass('active');
})
$('.closeIt').click(function(){
    $('.registration').removeClass('active');
    $('.authorization').removeClass('active');
    $('.information').addClass('active');
    $('.registrationButton').addClass('active');
    $('.description').removeClass('active');
})
$('.closeIt').click(function(){
    $('.registrationMobile').removeClass('active');
    $('.authorizationMobile').removeClass('active');
    $('.informationMobile').addClass('active');
    $('.descriptionMobile').removeClass('active');
})
$('.mapPointImage').click(function(){
    $('.mapForProvider').addClass('active');
})
$('.mapForProvider:not(iframe)').click(function(){
    $('.mapForProvider').removeClass('active');
})

$(".sendIt select").change(function() {
    $(this).closest('form').submit();
});

//$('#id_username').attr('placeholder','Логин');
//$('#id_first_name').attr('placeholder','Имя');
//$('#id_last_name').attr('placeholder','Фамилия');
//$('#id_password1').attr('placeholder','Пароль');
//$('#id_password2').attr('placeholder','Подтверждение пароля');

$('.del').click(function(){
    $(".item").addClass('show');
    $(".item").removeClass('active');
    $(".provider").removeClass('active');
    $(".del").addClass('active');
})
$('.provider:not(.del)').click(function(){
    $(".del").removeClass('active');
    $(this).toggleClass("active");
    var drink_id = $(this).attr('id').substring();
    $(".item").removeClass('show');
    var element = document.getElementsByClassName('item');
    counter = 0;
    counterHas = 0;
    for(var i = 0; i < element.length; i++) {
        if(element[i].id == String(drink_id)) {
            $(element[i]).toggleClass('active');
        }
        if(!element[i].classList.contains('active')) {
            counter++;
        }
        if(element[i].classList.contains('active')) {
            counterHas++;
        }
    }
    if(counter == element.length) {
        $(".item").toggleClass('show');
        $(".del").addClass('active');
    }
    if(counterHas == element.length) {
        $(".item").addClass('show');
        $(".item").removeClass('active');
        $(".provider").removeClass('active');
        $(".del").addClass('active');
    }
})


//местоположение пользователя
window.onload = function() {
  var startPos;
  var geoOptions = {
    enableHighAccuracy: true
  }

  var geoSuccess = function(position) {
    startPos = position;
    document.getElementById('startLat').innerHTML = startPos.coords.latitude;
    document.getElementById('startLon').innerHTML = startPos.coords.longitude;
  };
  var geoError = function(error) {
    console.log('Error occurred. Error code: ' + error.code);
    // error.code can be:
    //   0: unknown error
    //   1: permission denied
    //   2: position unavailable (error response from location provider)
    //   3: timed out
  };

  navigator.geolocation.getCurrentPosition(geoSuccess, geoError, geoOptions);
};

//инициализация карт
ymaps.ready(init);
function init(){
    var myMap = new ymaps.Map("map", {
    center: [55.753596, 37.621696],
    zoom: 7
    });
}
