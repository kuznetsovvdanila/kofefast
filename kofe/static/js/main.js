$('.arrowMobile').click(function(){
    $('.arrow').toggleClass('active');
    $('.arrowMobile').toggleClass('active');
    $('.addressMenuMainPage').toggleClass('active');
})
$('.mainAuth').click(function(){
    $('.arrow').removeClass('active');
    $('.addressMenuMainPage').removeClass('active');
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

//$('.eat').click(function(){
//    $('.coffee').removeClass('active');
//    $('.breakfast').addClass('active');
//})
//$('.drink').click(function(){
//    $('.coffee').addClass('active');
//    $('.breakfast').removeClass('active');
//})

$('#id_username').attr('placeholder','Логин');
$('#id_first_name').attr('placeholder','Имя');
$('#id_last_name').attr('placeholder','Фамилия');
$('#id_password1').attr('placeholder','Пароль');
$('#id_password2').attr('placeholder','Подтверждение пароля');

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

let map;

function initMap() {
map = new google.maps.Map(document.getElementById("map"), {
  center: { lat: 55.7601296, lng: 37.6025209 },
  zoom: 12,
});
}