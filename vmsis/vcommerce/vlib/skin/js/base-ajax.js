$(document).ready(function(){
  $("#UnidadeSelecionada").change(function(){
    var unidade = $(this).val()
    $.ajax({
        url: 'mudarunidade/',
        type: 'get',
        data: {"unidade" : unidade},
        success: function (data) {
          if (data == 'error')
            alert('Ocorreu um erro.');
        },
        failure: function (data) {
          alert('Ocorreu um erro.');
        }
    })         	
  });

  var unidade_selecionada = $("#UnidadeEscolhida").val();
  if(unidade_selecionada != undefined)
    $("#UnidadeSelecionada").val(unidade_selecionada);

});