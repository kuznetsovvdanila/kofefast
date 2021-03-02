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
    $('.info').addClass('hidden');
})
$('.closeIt').click(function(){
    $('.addressMenu').removeClass('active');
    $('.info').removeClass('hidden');
})
//$('#prokryti').click(function(){
//    $('.addresses').toggleClass('active');
//    $('.opn').toggleClass('active');
//    const el = document.getElementById('prokryti');
//    el.scrollIntoView();
//})
