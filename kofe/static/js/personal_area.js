$('.ownerInterface').click(function(){
    $('.ownerInterface').toggleClass('active');

    $('.info').toggleClass('hidden');
    $('.infoOwner').toggleClass('hidden');

    $('.addresses').removeClass('active');

    $('.orders').removeClass('active');
})
$('.ord').click(function(){
    $('.orders').toggleClass('active');
    $('.cls').toggleClass('active');
})
$('.adr').click(function(){
    $('.addresses').toggleClass('active');
    $('.opn').toggleClass('active');
})
$('.addressOpen').click(function(){
    $('.edit').removeClass('active');
    $('.addressMenu').addClass('active');
    $('.info').addClass('hidden');
})
$('.addAnAddress').click(function(){
    $('.edit').removeClass('active');
    $('.addressMenu').addClass('active');
    $('.info').addClass('hidden');
    $('.info').removeClass('move');
    $('.person').removeClass('hidden');
    $('.personInfo').removeClass('hidden');
})
$('.closeIt').click(function(){
    $('.addressMenu').removeClass('active');
    $('.edit').removeClass('active');
    $('.info').removeClass('hidden');
    $('.info').removeClass('move');
    $('.person').removeClass('hidden');
    $('.personInfo').removeClass('hidden');
})
$('.photo').click(function(){
    $('.addressMenu').removeClass('active');
    $('.edit').addClass('active');
    $('.info').addClass('hidden');
})
$('.chng').click(function(){
    $('.info').addClass('move');
    $('.person').addClass('hidden');
    $('.personInfo').addClass('hidden');
    $('.addressMenu').removeClass('active');
    $('.edit').addClass('active');
    $('.personInfo').addClass('hidden');
})

$('.input_file input[type=file]').change(function(){
    var t = $(this).val();
    if(t.indexOf('C:\\fakepath\\')+1)
        t = t.substr(12);
    var e = $(this).next().find('.fake_file_input');
    e.val(t);
});
$('.clear_input').click(function(){
    var a = $(this).parent();
    var e = a.find('.fake_file_input');
    var t = a.find('input[type=file]');
    t.replaceWith('<input type="file" name="" >');
    e.val('');
});

//$('#prokryti').click(function(){
//    $('.addresses').toggleClass('active');
//    $('.opn').toggleClass('active');
//    const el = document.getElementById('prokryti');
//    el.scrollIntoView();
//})
