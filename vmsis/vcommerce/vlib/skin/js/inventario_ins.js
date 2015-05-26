 function InicInventario() {
  $("button.btn-primary").html('Confirmar');
  $("button.btn-success").addClass('invisible');
  $("button.btn-primary").css({'display':'inline', 'float':'left', 'margin-right':'2px'});
  $("button.btn-danger").css({'display':'inline', 'float':'left'});
  
  $("button.btn-primary").attr('onclick', 'window.location.reload()');
  $("button.btn-primary").click(function(){
  	$("#Inventario").submit();
  })
  
  $("a.fa-trash-o").attr('onclick', '');
  $("a.fa-file-o").attr('onclick', '');
  $("a.glyphicon-floppy-remove").attr('onclick', '');

  $("button.btn-danger").html('Cancela');
}

$(document).ajaxComplete(function() {
  InicInventario();
});

$(document).ready(function() {
  InicInventario();
});