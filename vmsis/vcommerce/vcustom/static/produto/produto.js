window.addEventListener('load', function(){
   $.get('/imagens/Lista', {})
   .done(function(data){
      vmsisLib.listImage('lista-produtos', '.panel-body', '#id_imgindex', data);       
   });
}, true);