$(document).ajaxComplete(function() {
  $('input').addClass('form-control');
  $('select').addClass('form-control');
  $('textarea').addClass('form-control');
  $('.errorlist').css('color','#990000');
  $('.errorlist').addClass('alert alert-danger');

  $('.gridtag').removeClass('form-control');
  

});

$(document).ready(function() {
  $('input').addClass('form-control');
  $('select').addClass('form-control');
  $('textarea').addClass('form-control');
  $('.errorlist').css('color','#990000');
  $('.errorlist').addClass('alert alert-danger');  
  $('.gridtag').removeClass('form-control');
});