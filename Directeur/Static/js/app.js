$(document).ready(function () {
   taux();
});

function taux() {
    $('.taux').each(function(){
        $(this).text('0 %');
        $(this).css('color', 'red');
        const pourc = parseFloat($(this).attr('data-target'));
        if(pourc <= 10){
            $(this).text(pourc + ' %');
            $(this).css('color', 'green');
        }
        if(pourc > 10 && pourc <= 20){
            $(this).text(pourc + ' %');
            $(this).css('color', 'rgb(255, 123, 0)');
        }
        if(pourc > 20){
            $(this).text(pourc + ' %');
            $(this).css('color', 'red');
        }
    });
}
