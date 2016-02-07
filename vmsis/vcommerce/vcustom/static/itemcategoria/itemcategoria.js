window.addEventListener('load', function(){
   $('.grid-custom-title .glyphicon.glyphicon-print').each(function(){
       $(this).attr('onclick', '');
       $(this).attr('href', '/itemcategoria/relagrupamento');
       $(this).attr('target', '_blank');
   })
});