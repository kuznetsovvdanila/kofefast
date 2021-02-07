$('.registrationButton').click(function(){
    $('.registration').addClass('active');
    $('.authorization').removeClass('active');
    $('.information').removeClass('active');
    $('.registrationButton').removeClass('active');
})
$('.defaultUserPhoto').click(function(){
    $('.registration').removeClass('active');
    $('.authorization').addClass('active');
    $('.information').removeClass('active');
    $('.registrationButton').addClass('active');
})
$('#id_username').attr('placeholder','Логин');
$('#id_first_name').attr('placeholder','Имя');
$('#id_last_name').attr('placeholder','Фамилия');
$('#id_password1').attr('placeholder','Пароль');
$('#id_password2').attr('placeholder','Подтверждение пароля');
