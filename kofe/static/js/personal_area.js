var hdn = '';
var hdnChng = '';
var menuItemOpen = false;
var menuAddressCafeOpen = false;

$('.ownerInterface').click(function(){
    if ($('.ownerInterface').hasClass('active')) {
        $('.addressMenuProvider').removeClass('active');
        $('.itemEditForm').removeClass('active');
        $('.info').removeClass('hidden');
        $('.infoOwner').addClass('hidden');
        $('.edit').removeClass('active');
    }
    else {
        console.log('ae');
        $('.edit').removeClass('active');
        $('.addressMenu').removeClass('active');
        $('.infoOwner').removeClass('hidden');
        $('.info').addClass('hidden');
    }
    $('.opn').addClass('active');
    $('.addresses').removeClass('active');
    $('.cls').addClass('active');
    $('.orders').removeClass('active');
    $('.ownerInterface').toggleClass('active');
})
$('.itemEdit').click(function(){
    if ($('.orders').hasClass('active')) {
        menuItemOpen = true;
        $('.orders').removeClass('active');
        $('.cls').addClass('active');
    }
    if ($('.addresses').hasClass('active')) {
        menuAddressCafeOpen = true;
        $('.addresses').removeClass('active');
        $('.opn').addClass('active');
    }
    var t_element = this.classList;
    var el = document.getElementsByClassName('itemEditForm');
    for (var i = 0; i < el.length; i++) {
        if (el[i].id == t_element[1]) {
            $(el[i]).addClass('active');
        }
    }
    $('.infoOwner').addClass('hidden');
})
$('.addAnItem').click(function(){
    var el = document.getElementsByClassName('itemEditForm');
    for (var i = 0; i < el.length; i++) {
        if (el[i].id == '0') {
            $(el[i]).addClass('active');
        }
    }
    $('.infoOwner').addClass('hidden');
})
$('.addCafeAddress').click(function(){
    $('.addressMenuProvider').addClass('active');
    $('.infoOwner').addClass('hidden');
    $('.itemEditForm').removeClass('active');
    $('.edit').removeClass('active');
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
    if ($('.info').hasClass('hidden')) {
        hdn = 'infoOwner';
    }
    else {
        hdn = 'info';
    }
    console.log('открыть', hdn);
    $('.edit').removeClass('active');
    $('.addressMenu').addClass('active');
    $('.info').addClass('hidden');
    $('.infoOwner').addClass('hidden');

})
$('.addAnAddressProvider').click(function(){
    if ($('.orders').hasClass('active')) {
        menuItemOpen = true;
        $('.orders').removeClass('active');
        $('.cls').addClass('active');
    }
    if ($('.addresses').hasClass('active')) {
        menuAddressCafeOpen = true;
        $('.addresses').removeClass('active');
        $('.opn').addClass('active');
    }
    $('.addressMenuProvider').addClass('active');
    $('.infoOwner').addClass('hidden');
})
$('.addAnAddress').click(function(){
    if ($('.info').hasClass('hidden')) {
        hdn = 'infoOwner';
    }
    else if ($('.infoOwner').hasClass('hidden')) {
        hdn = 'info';
    }
    else {
        hdn = 'info';
    }
    $('.edit').removeClass('active');
    $('.addressMenu').addClass('active');
    $('.info').addClass('hidden');
    $('.infoOwner').addClass('hidden');

    $('.addressMenu').addClass('active');
    $('.info').removeClass('move');
    $('.infoOwner').removeClass('move');
    $('.person').removeClass('hidden');
    $('.personInfo').removeClass('hidden');
})
$('.closeIt').click(function(){
    if (menuItemOpen) {
        $('.orders').addClass('active');
        $('.cls').removeClass('active');
        $('.itemEditForm').removeClass('active');
        menuItemOpen = false;
        $('.infoOwner').removeClass('move');
        $('.infoOwner').removeClass('hidden');
    }
    if (menuAddressCafeOpen) {
        $('.addresses').addClass('active');
        $('.opn').removeClass('active');
        $('.itemEditForm').removeClass('active');
        menuAddressCafeOpen = false;
        $('.infoOwner').removeClass('move');
        $('.infoOwner').removeClass('hidden');
    }
    if ($('.addressMenuProvider').hasClass('active')) {
        $('.addressMenuProvider').removeClass('active');
        $('.infoOwner').removeClass('move');
        $('.infoOwner').removeClass('hidden');
    }
    if ($('.itemEditForm').hasClass('active')) {
        $('.infoOwner').removeClass('move');
        $('.infoOwner').removeClass('hidden');
        $('.itemEditForm').removeClass('active');
    }
    if ($('.edit').hasClass('active')) {
        $('.info').removeClass('move');
        $('.infoOwner').removeClass('move');
        if (hdnChng == 'info') {
            $('.info').removeClass('hidden');
        }
        if (hdnChng == 'infoOwner') {
            $('.infoOwner').removeClass('hidden');
        }
        $('.edit').removeClass('active');
    }
    if ($('.addressMenu').hasClass('active')) {
        if (hdn == 'info') {
            $('.info').removeClass('hidden');
        }
        if (hdn == 'infoOwner') {
            $('.infoOwner').removeClass('hidden');
        }
        $('.addressMenu').removeClass('active');
    }
    $('.person').removeClass('hidden');
    $('.personInfo').removeClass('hidden');
})
$('.photo').click(function(){
    if ($('.info').hasClass('hidden')) {
        hdnChng = 'infoOwner';
    }
    else {
        hdnChng = 'info';
    }
    $('.addressMenu').removeClass('active');
    $('.edit').addClass('active');
    $('.info').addClass('hidden');
    $('.infoOwner').addClass('hidden');
})
$('.chng').click(function(){
    $('.info').addClass('move');
    $('.infoOwner').addClass('move');
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
