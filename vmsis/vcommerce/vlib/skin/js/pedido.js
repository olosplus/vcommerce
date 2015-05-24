function ObrigaAdicional() {
  $("#div_ItemPedido a[title='Adicionar']").each(function(){
    $(this).click(function(){
      $("#ItemPedido tbody tr [name='idadicional']").click(function(){
        $("#div_ItAdicional a[title='Adicionar']")[0].onclick()
      });
             
    });
  });
  
}


$(document).ajaxComplete(function() {
  ObrigaAdicional();
});

$(document).ready(function() {
  ObrigaAdicional(); 
});