 function InicParamGeral() {
  $("button.btn-primary").html('Confirmar');
  $("button.btn-danger").html('Desfazer');
  $("button.btn-danger").attr('onclick', 'window.location.reload()');
}

$(document).ajaxComplete(function() {
  InicParamGeral();  
});

$(document).ready(function() {
  InicParamGeral();  
});