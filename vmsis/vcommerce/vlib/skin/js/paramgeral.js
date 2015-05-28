 function InicParamGeral() {
  $("#btn-salvar-listar").css('display', 'none');
  $("#btn-salvar-inserir").css('display', 'none'); 
  $("#btn-salvar-editar").html('Confirmar');
  $("#btn-cancelar").html('Desfazer');
  $("#btn-cancelar").attr('onclick', 'window.location.reload()');
}

$(document).ajaxComplete(function() {
  InicParamGeral();  
});

$(document).ready(function() {
  InicParamGeral();  
});