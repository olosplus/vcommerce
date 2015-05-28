 function InicInventario() {
  $("#btn-salvar-listar").css('display', 'none');
  $("#btn-salvar-inserir").css('display', 'none');
  $("#btn-salvar-editar").html('Confirmar');
  $("#btn-cancelar").html('Cancela');
    
  $("a.fa-trash-o").attr('onclick', '');
  $("a.fa-file-o").attr('onclick', '');
  $("a.glyphicon-floppy-remove").attr('onclick', '');  
}

$(document).ajaxComplete(function() {
  InicInventario();
});

$(document).ready(function() {
  InicInventario();
});