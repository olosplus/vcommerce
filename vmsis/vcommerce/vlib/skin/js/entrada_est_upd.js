function InicEntrada() {
  $(".fieldWrapper a.inline").attr('onclick', '');

  $("[name='produto_id']").attr('disabled','');
  $("[name='empresa_id']").attr('disabled','');

  $(".fieldWrapper a.inline").remove("a.inline");

  var forn = $("#id_fornecedor");
  forn.css('display', 'none')
  forn.parent().append("<input type='text' class='form-control' disabled value='" + 
    forn.find("[selected='selected']")[0].text + "'>");

  var dtentr = $("#id_dtentrada");
  dtentr.css('display', 'none');
  dtentr.parent().append("<input class='form-control form-control-customizado inline' type='date' "+
    "value='"+ dtentr.val() +"' disabled >");
};

$(document).ajaxComplete(function() {
  InicEntrada();  
});

$(document).ready(function() {
  InicEntrada();
});

