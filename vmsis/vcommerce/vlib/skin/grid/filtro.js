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
  var modulo = module;
  var modelo = model;
  var colunas = columns;
  $.ajax({
    url: '/filtro',
    type: 'get',    
    data: {"module" : modulo, "model" : modelo},
    success: function (data) {
      $('#dialog').html(data);      
      
      $('#dialog').dialog({
        dialogClass : "no-close",        
        maxHeight: 500,
        buttons : [
          {
            text : "Filtrar",
            click : function(){
              
              form = $(this).children("form");              
              form_serialized = form.serializeArray();
              
              $("#filter_cache").remove();
              $("body").append("<input type='hidden' id='filter_cache'  "+
                " value= '" + JSON.stringify(form_serialized) + "' >");

              var palavras_inteiras = $("#palavras_inteiras").val();

              GetGridData(modulo, modelo, form_serialized, colunas, palavras_inteiras, 1, 'id');
              $(this).dialog("close");
            }
          },
          {
            text : "Cancelar",
            click : function(){
              $(this).dialog("close");
            }
          }
        ]
      });
    },
    failure: function (data) {
      alert('Got an error dude');
    }
  });  
};