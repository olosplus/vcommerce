 function InicInventario() {
  $("button.btn-primary").html('Confirmar');
  $("button.btn-danger").html('Cancela');

  $("a.fa-trash-o").attr('onclick', '');
  $("a.fa-file-o").attr('onclick', '');
  $("#id_dtinventario").attr('disabled', '');
  
  $("[name='qtdeprod_old']").attr('disabled','');
  $("[name='lote_id']").attr('disabled','');
  $("[name='almoxarifado_id']").attr('disabled','');
  $("[name='produto_id']").attr('disabled','');
  $("[name='empresa_id']").attr('disabled','');

  var alm = $("#id_almoxarifado");
  alm.addClass("invisible");
  alm.css({'display':'none'});
  alm.parent().append("<input type='text' class='form-control' disabled value='" + alm.find("[selected='selected']")[0].text + "'>");
};

$(document).ajaxComplete(function() {
  InicInventario();  
});

$(document).ready(function() {
  InicInventario();  
});
