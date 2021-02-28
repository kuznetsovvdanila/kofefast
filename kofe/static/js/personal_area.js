$('.ord').click(function(){
    $('.orders').toggleClass('active');
    $('.cls').toggleClass('active');
})
$('.adr').click(function(){
    $('.addresses').toggleClass('active');
    $('.opn').toggleClass('active');
})
$('.addAnAddress').click(function(){
    $('.addressMenu').addClass('active');
})
$('.closeIt').click(function(){
    $('.addressMenu').removeClass('active');
})
//$('#prokryti').click(function(){
//    $('.addresses').toggleClass('active');
//    $('.opn').toggleClass('active');
//    const el = document.getElementById('prokryti');
//    el.scrollIntoView();
//})
