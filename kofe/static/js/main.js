var current_time = new Date;
var hours = current_time.getHours();
var minutes = current_time.getMinutes() + 25;
var sHours = '';
var sMinutes = '';
if (minutes > 59) {
    minutes = minutes - 60;
    hours = hours + 1;
}
if (hours < 10) {
    sHours = '0' + String(hours);
}
else {
    sHours = String(hours);
}
if (minutes < 10) {
    sMinutes = '0' + String(minutes);
}
else {
    sMinutes = String(minutes);
}
if (document.getElementById('timeInput')) {
    document.getElementById('timeInput').value = sHours + '.' + sMinutes;
}
//document.getElementById('timeInput').oninput = function () {
//    if (Number(this.value[0] + this.value[1] + this.value[3] + this.value[4]) > 2359) {
//        document.getElementById('takeAnOrder').disabled = true;
//    }
//    else {
//        document.getElementById('takeAnOrder').disabled = false;
//    }
//}
if ($('#to_time').hasClass('ch')) {
    if (Number(document.getElementById('timeInput').value[0] + document.getElementById('timeInput').value[1] + document.getElementById('timeInput').value[3] + document.getElementById('timeInput').value[4]) > 2359) {
        console.log('yeet');
    }
}
$('.choose_your_address').click(function(){
    $('.choose_your_address_menu').removeClass('hidden');
    $('.choose_your_address_menu_background').addClass('active');
})
$('.password_change_return').click(function(){
    $('.passwordAuth').attr("required");
    $('.password_change_return').addClass('hidden');
    $('.password_change').removeClass('hidden');
    $('.submitAuth').removeClass('active');
    $('.passwordAuth').removeClass('active');
    $('.authorization').removeClass('move');
    document.getElementsByClassName('submitAuth')[0].value = 'Войти';
    document.getElementsByClassName('emailAuth')[0].placeholder = 'Почта';
    document.getElementsByClassName('type_changer')[0].value = 'authen';
    document.getElementsByClassName('submitAuth')[1].value = 'Войти';
    document.getElementsByClassName('emailAuth')[1].placeholder = 'Почта';
    document.getElementsByClassName('type_changer')[1].value = 'authen';
    $('input').addClass('placeholderWhite');
})
$('.password_change').click(function(){
    $('.passwordAuth').removeAttr("required");
    $('.password_change_return').removeClass('hidden');
    $('.password_change').addClass('hidden');
    $('.submitAuth').addClass('active');
    $('.passwordAuth').addClass('active');
    $('.authorization').addClass('move');
    document.getElementsByClassName('submitAuth')[0].value = 'Отправить письмо';
    document.getElementsByClassName('emailAuth')[0].placeholder = 'Почта';
    document.getElementsByClassName('type_changer')[0].value = 'password_change';
    document.getElementsByClassName('submitAuth')[1].value = 'Отправить письмо';
    document.getElementsByClassName('emailAuth')[1].placeholder = 'Почта';
    document.getElementsByClassName('type_changer')[1].value = 'password_change';
    $('input').addClass('placeholderWhite');
})
$('.addToBasket').click(function(){
    var elements = document.getElementsByClassName('user_y');
    for (var i = 0; i < elements.length; i++) {
        elements[i] = 0;
        elements[i].value = parseInt(window.pageYOffset);
    }
})
$('#to_time').click(function() {
    $('#to_time').addClass('ch');
    $('#fast').removeClass('ch');
})
$('#fast').click(function() {
    $('#to_time').removeClass('ch');
    $('#fast').addClass('ch');
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
    $('input').addClass('placeholderWhite');
    $('.registration').addClass('active');
    $('.authorization').removeClass('active');
    $('.information').removeClass('active');
    $('.registrationButton').removeClass('active');
    $('.description').addClass('active');
    document.getElementsByClassName('emailAuth')[0].placeholder = 'Почта';
})
$('.registrationButtonMobile').click(function(){
    $('input').addClass('placeholderWhite');
    $('.registrationMobile').addClass('active');
    $('.authorizationMobile').removeClass('active');
    $('.informationMobile').removeClass('active');
    $('.descriptionMobile').addClass('active');
    document.getElementsByClassName('emailAuth')[0].placeholder = 'Почта';
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
    $('input').addClass('placeholderWhite');
    document.getElementsByClassName('emailAuth')[0].placeholder = 'Почта';
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
    $('.choose_your_address_menu_background').addClass('active');
    $('.choose_your_address_menu_background').removeClass('not_active');
    $('.choose_your_address_menu').removeClass('hidden');
})
$('.choose_your_address_menu_background').click(function(){
    $('.choose_your_address_menu_background').removeClass('active');
    $('.choose_your_address_menu_background').addClass('not_active');
    $('.choose_your_address_menu').addClass('hidden');
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
