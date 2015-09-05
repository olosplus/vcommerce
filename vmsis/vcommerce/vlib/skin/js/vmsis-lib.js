//cria a funcionalidade icontains no JQUERY
jQuery.expr[":"].icontains = jQuery.expr.createPseudo(function(arg) {
    return function( elem ) {
        return jQuery(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
    };
});

//CRIA A BIBLIOTECA vmsisLib
vmsisLib = {};

/*listBox
  -cria uma lista com um filtro
  -listBox.new : criar um novo listBox na página
    -parametros
      -jsonList : um json com os dados no formato {"valor1" : "texto exibido", "valor2" : "texto exibido"}
      -idContainer : o id do elemento que irá conter o listBox(deve estár vazio)
      -label : uma descrição a ser exibida para o listBox
      -executeOnClick : método que será executado sempre que um item for clicado. O método que
        for passado neste parâmetro sempre deve conter um parâmetro que receberá o próprio elemento
        clicado(this)
  -listBox.getVal : Busca o valor(data-value) selecionado de um listBox
    -parametros
      -idContainer : id do container a qual o listBox pertence
*/
vmsisLib.listBox = {}
vmsisLib.listBox.new = function(jsonList, idContainer, label, executeOnClick){
   
    var html = "<div class='vmsis-list-box'>";
    if (label) {
        html += "<p class='vmsis-list-box-label'>" + label + "</p>";
    }
    html += "<input type='text' placeholder='Procurar...' class='form-control' >";
        
    html += "<ul>";
    for(item in jsonList){
        html += "<li data-value='" + item + "'>" + jsonList[item] + "</li>"
    };
    html += "</ul>";
    html += "</div>";
    $("#"+ idContainer).html(html);
    $("#"+ idContainer +" input").keyup(function(){
        var val = $(this).val();
        if (val != "") {
            $("#"+ idContainer +" .vmsis-list-box li").css('display', 'none');
            $("#"+ idContainer +" .vmsis-list-box li:icontains('"+ val +"')").css('display', 'block');
        }else{
            $("#"+ idContainer +" li").css('display', 'block');
        };
    });
    
    $("#"+ idContainer +" .vmsis-list-box li").each(function(){
        
        $(this).click(function(){
            ele = $("#"+ idContainer +" li .vmsis-text-box-item-active");            
            $("#"+ idContainer +" li").removeClass("vmsis-text-box-item-active");
            $(this).addClass("vmsis-text-box-item-active");                    
            if (typeof executeOnClick == 'function') {
                clickReturn = executeOnClick(this);
                if (clickReturn === false) {
                    $("#"+ idContainer +" li").removeClass("vmsis-text-box-item-active");
                    ele.addClass("vmsis-text-box-item-active");
                    return;
                }                
            };
        });
    });
}

vmsisLib.listBox.getVal = function(idContainer){
    return $("#" + idContainer + " .vmsis-text-box-item-active").first().attr('data-value');
}

vmsisLib.listBox.setFocus = function(idContainer){
    $("#" + idContainer + " input").first().focus();
}



/*
 Format é uma função para evitar concatenação de strings. Passe o parâmetro %s onde se quer
 colocar um valor concatenado e eles serão substituidos pela lista informada.
 Parametros:
  - str : String onde quer se inserir o valor
  - list : Lista de strings que deverão substituir os parâmetros %s(na ordem)

*/

vmsisLib.format = function(str, list){
		var i = 0;		
		var text = str;
		for(i = 0; i <= list.length - 1; i++){
		   text = text.replace("%s", list[i]);		   
		};
		return text;
	};
vmsisLib.waitting = {};
vmsisLib.waitting.intervalVar;
vmsisLib.waitting.start = function(){
    vmsisLib.waitting.intervalVar = setInterval(function(){
        if($(".modal-waitting").length == 0){
            $("body").append("<div class='modal-waitting'></div>");
            
            $(".modal-waitting").css({"background-color":"white", "bottom": 0, "left": 0, "position": "fixed",
              "right": 0, "top": 0, "height" : "100%", "width":"100%", "opacity" : 0.5,
              "border-radius" : "0px", "box-shadow": "0px 0px 0px gray"});
            
            
            $(".modal-waitting").append($( '<div class="waitting-vmsis 1 active"> </div>'));
            $(".modal-waitting").append($( '<div class="waitting-vmsis 2"> </div>'));
            $(".modal-waitting").append($( '<div class="waitting-vmsis 3"> </div>'));
            $(".modal-waitting").append($( '<div class="waitting-vmsis 4"> </div>'));
            $(".modal-waitting").append($( '<div class="waitting-vmsis 5"> </div>'));
            $(".modal-waitting").append($( '<div class="waitting-vmsis 6"> </div>'));
            $(".modal-waitting").append($( '<div class="waitting-vmsis 7"> </div>'));
            
            
        }
        if($(".waitting-vmsis.1").hasClass("active")){
            $(".waitting-vmsis.1").removeClass("active");
            $(".waitting-vmsis.2").addClass("active");
        }else if($(".waitting-vmsis.2").hasClass("active")){
            $(".waitting-vmsis.2").removeClass("active");
            $(".waitting-vmsis.3").addClass("active");          
        }else if($(".waitting-vmsis.3").hasClass("active")){
            $(".waitting-vmsis.3").removeClass("active");
            $(".waitting-vmsis.4").addClass("active");          
        }else if($(".waitting-vmsis.4").hasClass("active")){
            $(".waitting-vmsis.4").removeClass("active");
            $(".waitting-vmsis.5").addClass("active");          
        }else if($(".waitting-vmsis.5").hasClass("active")){
            $(".waitting-vmsis.5").removeClass("active");
            $(".waitting-vmsis.6").addClass("active");          
        }else if($(".waitting-vmsis.6").hasClass("active")){
            $(".waitting-vmsis.6").removeClass("active");
            $(".waitting-vmsis.7").addClass("active");          
        }else if($(".waitting-vmsis.7").hasClass("active")){
            $(".waitting-vmsis.7").removeClass("active");
            $(".waitting-vmsis.1").addClass("active");          
        };
        
        $(".waitting-vmsis").css({"border-radius" : "10px", "width" : "10px", "height" : "10px", "background-color" : "#337ab7",
            "float" : "left", "position" : "relative", "left" : "45%", "top" : "45%", "margin" : "2px", "z-index" : 1001})
        
        $(".waitting-vmsis.active").css({"background-color": "white", "border" : "1px solid #337ab7"});
                
    }, 350);
    return vmsisLib.waitting.intervalVar;
}

vmsisLib.waitting.stop = function(waittingVar){
   clearVar = waittingVar || vmsisLib.waitting.intervalVar;
   clearInterval(vmsisLib.waitting.intervalVar); 
   $(".modal-waitting").remove();
}