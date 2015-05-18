function Inicializacao() {
//  $('form').addClass("form-inline")
  $('form input[type="text"]').addClass('form-control');
  $('form input[type="number"]').addClass('form-control');  
  $('form input[type="date"]').addClass('form-control');  
  $('form input[type="datetime"]').addClass('form-control');  
  $('form input[type="decimal"]').addClass('form-control');  
  $('form input[type="email"]').addClass('form-control');  
  $('form input[type="time"]').addClass('form-control');  
  $('form input[type="url"]').addClass('form-control'); 
  $('form input[type="password"]').addClass('form-control');
  $('form select').addClass('form-control');
  $('form textarea').addClass('form-control');
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