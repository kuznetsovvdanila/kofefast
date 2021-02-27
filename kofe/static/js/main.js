$('.registrationButton').click(function(){
    $('.registration').addClass('active');
    $('.authorization').removeClass('active');
    $('.information').removeClass('active');
    $('.registrationButton').removeClass('active');
    $('.description').addClass('active');
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
$('.eat').click(function(){
    $('.coffee').removeClass('active');
    $('.breakfast').addClass('active');
})
$('.drink').click(function(){
    $('.coffee').addClass('active');
    $('.breakfast').removeClass('active');
})
$('#id_username').attr('placeholder','Логин');
$('#id_first_name').attr('placeholder','Имя');
$('#id_last_name').attr('placeholder','Фамилия');
$('#id_password1').attr('placeholder','Пароль');
$('#id_password2').attr('placeholder','Подтверждение пароля');


 $('.provider').click(function(){
        var drink_id = $(this).attr('id').substring();
        console.log("#item"+drink_id);
        $(".item").removeClass('active');
        $("#item"+String(drink_id)).addClass('active');


})

let map;

function initMap() {
map = new google.maps.Map(document.getElementById("map"), {
  center: { lat: 55.7601296, lng: 37.6025209 },
  zoom: 12,
});
}