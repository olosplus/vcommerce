$(document).ready(function(){
	$("#id_identificador").change(function(){
		var value = $(this).val();
		var campo_insc = $("#id_nrinscjurd");
		campo_insc.val("");
		if(value === 'J'){
		   campo_insc.mask("00.000.000/0000-00");
		}else if(value === 'F'){
		   campo_insc.mask("000.000.000-00");
		}else{
			campo_insc.mask("0000000000000000");
		}
	});

	$("input[name='cdcep']").mask('00000-000');
	$("input[name='nrtelefone']").mask('(00)0000-0000');
	$("input[name='nrcelular']").mask('(00)0000-0000');

	$("a[title='Adicionar']").click(function(){
		$("input[name='cdcep']").mask('00000-000');
		$("input[name='nrtelefone']").mask('(00)0000-0000');
        $("input[name='nrcelular']").mask('(00)0000-0000');		
	})
})