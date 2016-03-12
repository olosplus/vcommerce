function removeClassPalavrasInteiras(){
  $('#palavras_inteiras').removeClass();
};

function palavrasInteirasValue(){
  $('#palavras_inteiras').click(function(){
    if($(this).val() === "S")
      $(this).val("N")
    else
      $(this).val("S")
  });
};

$(document).ajaxComplete(function() {
  removeClassPalavrasInteiras();
  palavrasInteirasValue();
});

$(document).ready(function() {
  removeClassPalavrasInteiras();
  palavrasInteirasValue();
});

function Filter (module, model, columns) {
  vmsisLib.waitting.start();
  var modulo = module;
  var modelo = model;
  var colunas = columns;
  $.ajax({
    url: '/filtro',
    type: 'get',    
    data: {"module" : modulo, "model" : modelo},
    success: function (data) {            
      try{

         var parser = new DOMParser()
         var doc_received = parser.parseFromString(data, "text/html");
         var frm_received = doc_received.querySelector('#conteudo-filtro');
         
         
         try{
             $('#filtro .popup-body .content-filter').empty();
             document.querySelector('#filtro .popup-body .content-filter').appendChild(frm_received);
         }catch(e){
             console.log(e);
         };

         vmsisLib.popup.openPopup('#filtro');
      }catch(e){
         vmsisLib.aviso(e);
         vmsisLib.waitting.stop();
      }
      vmsisLib.waitting.stop();
      
      $("#btn-filtrar").click(function(){
            vmsisLib.waitting.start();
            form = $("#conteudo-filtro").children("form");              
            form_serialized = form.serializeArray();
              
            $("#filter_cache").remove();
            $("body").append("<input type='hidden' id='filter_cache'  "+
               " value= '" + JSON.stringify(form_serialized) + "' >");

            var palavras_inteiras = $("#palavras_inteiras").val();
              
            GetGridData(modulo, modelo, form_serialized, colunas, palavras_inteiras, 1, 'id');
            vmsisLib.waitting.stop();
            vmsisLib.popup.closePopup('filtro');
      });
      
    },
    failure: function (data) {
      alert('Got an error dude');
    }
  });  
};