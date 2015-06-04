function Inicializacao() {
  $('.errorlist').css('color','#990000');
  $('.errorlist').addClass('alert alert-danger');
  $('.ui-dialog-buttonset button').addClass('btn btn-outline btn-primary'); 
}



$(document).ajaxComplete(function() {
  Inicializacao();  
});

$(document).ready(function() {
  Inicializacao();  
});