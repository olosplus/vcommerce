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
            var ele = $("#"+ idContainer +" li .vmsis-text-box-item-active");            
            $("#"+ idContainer +" li").removeClass("vmsis-text-box-item-active");
            $(this).addClass("vmsis-text-box-item-active");                    
            if (typeof executeOnClick == 'function') {
                clickReturn = executeOnClick.call(this);
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


vmsisLib.contextMenu = function(fnExecuteOnItenClick, idContext){
    if (idContext) {
       var context_id = '#' + idContext
    }else{
       var context_id = "";
    }
    
    
    $(context_id + ".contextmenu").each(function(){
        var element = $(this);
        element.css("display","none");
        
        var parent = $(element.attr("data-container"));
        if (parent.length == 0 && element.attr("data-container").substr(0, 1) != '#' ) {
            parent = $("#" + element.attr("data-container"));
        }
        parent.attr('context-data-container', element.attr("data-container"))
        parent.on('contextmenu', function(e){
            var all_context = $(".contextmenu");
            all_context.offset({left:0, top:0});
            all_context.css("display", "none"); 
            
            var ele = $(this);
            
            var context = $("[data-container='" + $(this).attr("context-data-container") + "']");
            context.offset({left:e.clientX, top:e.clientY});
            context.css("display", "block");
            
            if (fnExecuteOnItenClick && typeof fnExecuteOnItenClick === 'function') {
                subEle = context.find('div');
                
                subEle.each(function(){
                   $(this).unbind('click');
                   $(this).click(function(e){
                      fnExecuteOnItenClick.call(ele[0],  this);                      
                   });
                });
            }
            
            e.preventDefault();
                                                
        });
        $(document).on('click', function(e){
            if(e.button == 0){
                var context = $(".contextmenu");
                context.offset({left:0, top:0});
                context.css("display", "none");                                 
            }
        });
    });
    
    
};


/*popus e dialogos*/
vmsisLib.popup = {}
vmsisLib.popup.open = false;


vmsisLib.popup.openPopup = function(select){
   var ele = document.querySelector(select);
    
    if(!ele){
    	ele = document.querySelector("#" + select);
    };
    
    if(ele){
    	ele.setAttribute('style', 'display:table');
    }
       vmsisLib.popup.open = true;
   
}

vmsisLib.popup.closePopup = function(id_filter, fnToExecuteAfter){
   

    var ele = document.querySelector("#" + id_filter);
	
	if(ele){
		ele.setAttribute('style', 'display:none');
	}
    
    vmsisLib.popup.open = false;
    
    if (fnToExecuteAfter) {
        fnToExecuteAfter.call();
    }
    
}

vmsisLib.popup.removePopup = function(id_filter, fnToExecuteAfter){
   $("#" + id_filter).remove();
    if (fnToExecuteAfter) {
        fnToExecuteAfter.call();
    }   
}



vmsisLib.aviso = function(message, fnToExecuteAfter){
    var html =
          '  <div class="popup-body popup-dlg small-radius">	'+
 	      '    <h2 class="yellow title">Aviso ! </h2> '+
          '    <p > <center>' + message + ' </center></p>'+          
 	  	  '    <center><a href="javascript:void(0)" id="vmsisMsgBtn" class="btn btn-warning ">OK</a></center> '+       
 	      '  </div> ';
 
    var popupE = document.createElement('div');
    popupE.setAttribute('class', 'popup small-radius');
    popupE.setAttribute('id', 'vmsisMsg');
    popupE.innerHTML += html
    
    try{        
        document.querySelector('body').appendChild(popupE); 
    }catch(e){
        console.log(e);
    };
    document.getElementById("vmsisMsgBtn").executeAfter = fnToExecuteAfter;
    document.getElementById("vmsisMsgBtn").addEventListener('click', function(){
       vmsisLib.popup.removePopup("vmsisMsg", this.executeAfter);
    });

    vmsisLib.popup.openPopup('vmsisMsg');    
}

vmsisLib.confirma = function(message, executeIfTrue, executeIfFalse){
    var html =
          '  <div class="popup-body popup-dlg small-radius">	'+
 	      '    <h2 class="yellow title">Confirmação ! </h2> '+
          '    <p><center> ' + message + ' </center> </p>'+          
 	  	  '   <div class="content-center"> <button type="button" id="vmsisMsgBtnYes" class="button button-green small-radius">Sim</button> '+
          '    <button type="button" id="vmsisMsgBtnNo" class="button button-red small-radius">Não</button> </div>'+                  
 	      '  </div> ';
 
    var popupE = document.createElement('div');
    popupE.setAttribute('class', 'popup small-radius');
    popupE.setAttribute('id', 'vmsisMsg');
    popupE.innerHTML += html
    
    try{
        document.querySelector('body').appendChild(popupE);
    }catch(e){
        console.log(e);
    };

    document.getElementById("vmsisMsgBtnYes").executeAfter = executeIfTrue;
    document.getElementById("vmsisMsgBtnNo").executeAfter = executeIfFalse;
    document.getElementById("vmsisMsgBtnYes").addEventListener('click', function(){      
       vmsisLib.popup.removePopup("vmsisMsg", this.executeAfter);
    });
    document.getElementById("vmsisMsgBtnNo").addEventListener('click', function(){       
       vmsisLib.popup.removePopup("vmsisMsg", this.executeAfter);
    });

    vmsisLib.popup.openPopup('vmsisMsg');
        
}


/*treeview*/

vmsisLib.treeView = function(idTreeView, fnExecuteOnItenClick){
    
	$('#' + idTreeView + '.tree-view ul li').each(function(){
		var ele = $(this).children('ul');
		if(ele.length > 0){			
		   $(this).addClass('has-child');
    	}else{
		   $(this).addClass('has-no-child');
		};
               

	    $(this).click(function(e){
		    $(this).parents('.tree-view').find('.selected').removeClass('selected');	
            $(this).addClass('selected');
            
            var ele = $(this).children('ul');
			if(ele.length > 0){
			    if($(this).hasClass('opened')){
			    	$(this).removeClass('opened');
			    }else{
			        $(this).addClass('opened');
			    };
			};
			      
	 	    if (ele.hasClass('node-active')){
		   	    ele.removeClass('node-active');
		    }else{
		   	    ele.addClass('node-active');
	        }
            
            if (fnExecuteOnItenClick) {
               if(typeof fnExecuteOnItenClick == 'function'){
                  fnExecuteOnItenClick.call(this);
               }
            }
		    e.stopPropagation();			    	
	    });
		
	});	
}

vmsisLib.listImage = function(id, container, bindTo, data_stringfy){
    imagens = JSON.parse(data_stringfy);
    sel = $(bindTo).val();
    
    $(container).append(vmsisLib.format('<div id="%s" class="sel-imglist cur-pointer" > </div>', [id + 'sel-imglist']));
         
    
    $(container).append(vmsisLib.format('<div class="popup" id="%s">  '+
                                        '  <div class="popup-body"> '+
                                        '    <a class="page-close" href="javascript:void(0)" title="Fechar" >X</a>'+
                                        '    <div class="imglist"></div> '+
                                        '  </div> '+
                                        '</div>',
                                        [id, id]))
    $('#' + id + ' > .popup-body > .page-close' ).click(function(){
       vmsisLib.popup.closePopup(id);    
    });
    for (img in imagens) {
      
      $("#" + id + ' .imglist').append(vmsisLib.format('<div class="flo-left bck-hover-blue cur-pointer imglist-item" data-value="%s"> <img src="%s"></img></div>',
          [img,imagens[img]]))
    }
   
    $('#' + id +  ' .imglist-item').click(function(){
       $('#' + id + ' .imglist-item').removeClass('selected');
       $(this).addClass('selected');
       $('#' + id + 'sel-imglist').html($(this).html());
       vmsisLib.popup.closePopup(id);
       $(bindTo).val($(this).attr('data-value'));
    });
   
    if (sel) {
       $('#' + id +  'sel-imglist').html( $(vmsisLib.format('[data-value="%s"]', [sel])).html());
    }else{
       $('#' + id +  'sel-imglist').html('<span class="red">Selecione uma imagem...</span>');  
    }
   
    $('#' + id +  'sel-imglist').click(function(){
       vmsisLib.popup.openPopup(id);
    })

}