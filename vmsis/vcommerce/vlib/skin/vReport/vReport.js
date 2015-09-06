/*

PageType - Estilo da página
  A4 - 
PageHeader - Div com tamanho de 100%

*/

vReport = function(pageType, container, data, sel_document){	
    
    if(pageType == "A4 portrait"){	
	  var pageHeight = 1122.519685039;//1207; 
	  var pageWidth = 793.700787402;//826.67; 
	}else if(pageType == "A4 landscape"){
	  var pageHeight = 826.67;//1207; 
	  var pageWidth = 1207;//826.67;
	};
	
	if (sel_document != undefined && sel_document != null && sel_document != ""){
	  var doc = sel_document;
	}else{
	  var doc = document;
    };    
	
	var pages = 1;
    
    /*utilidade - Serve para selecionar os elementos. Não utilizei jquery pois ainda não chegamos na matéria*/ 
	var getE = function(select){
		var e = undefined;
		var sel_type = select.substring(0,1);
		var sel = select.substring(1, select.length + 1);
		if (sel_type == "#"){
			return doc.getElementById(sel);			
		}else if(sel_type == "."){
			return doc.getElementsByClassName(sel);
		}else if(sel_type == "@"){
			return doc.getElementsByName(sel);			
		}else{
			return doc.getElementsByTagName(select);
		};
	};
    /*utilidade - serve para concatenar strings de forma mais elegante*/ 
	var format = function(str, list){
		var i = 0;		
		var text = str;
		for(i = 0; i <= list.length - 1; i++){
		   text = text.replace("%s", list[i]);		   
		};
		return text;
	};

	/*seleciona o elemento que deverá conter o relatório*/    
	var allBody = getE(container);        
	if (allBody.length != undefined)
		allBody = allBody[0]

    allBody.className += "body vReport";
//    allBody.innerHTML += "<div id='tools'></div>"
	allBody.innerHTML += "<div id='relContainer'></div>";
    
	var body = getE('#relContainer');
	
	var getPage = function(){
		return pages - 1;
	}
    
	addPage = (function(){		
		body.innerHTML += format("<div class='page' id='page%s' style='width:%spx;height:%spx;margin:3px auto 3px'></div>", 
		  [pages, pageWidth, pageHeight]);
		pages += 1;
	});
	
	var getPageEle = function(){
		return doc.getElementById("page" + getPage());
	}
	
    var addPageHeader = (function(style){		
		doc.getElementById("page" + getPage()).innerHTML += 
		  format("<div class='pageHeader' id = 'pageHeader_%s' style='%s'> </div>", [getPage(), style] );
	});
	
	var addComponent = function(parent, component){
		var page = getPageEle();
		var parE = undefined;
		if (parent != "pages" + getPage())
		   parE = doc.getElementById(parent);
	    else
			parE = page;
		parE.innerHTML += component;
	};
	
	var addLabel = function(parent, name, text, style){		
        addComponent(parent, format("<label class='label' id='%s_%s' style='%s'>%s</label>", [name, getPage(), style, text]));
	};

	var addP = function(parent, name, text, style){		
        addComponent(parent, format("<p class='paragraph' id='%s_%s' style='%s'>%s</label>", [name, getPage(), style, text]));
	};

	var addDiv = function(parent, name, text, style){		
        addComponent(parent, format("<div class='div' id='%s_%s' style='%s'>%s</div>", [name, getPage(), style, text]));
	};
	
	var addMasterBand = function(style){
	    var mBands = getE(".masterBand");
		var mBandsCount = 1;
		if(mBands != undefined){
			mBandsCount = mBands.length + 1;
		}
     	doc.getElementById("page" + getPage()).innerHTML += 
		  format("<div class='masterBand' id = 'masterBand_%s_%s' style='%s'> </div>", [getPage(), mBandsCount, style] );		
	};
		
	var checkPageSize = function(pageHeader, bandCount){
		var pg = getPageEle();
          		
	    var lastChild = pg.lastChild;
		
		var lastChildTop = lastChild.offsetTop;
		var lastChildHeight = lastChild.offsetHeight;
		
		if ( (lastChildTop + lastChildHeight) >= (pageHeight * getPage() ) ){
			pg.removeChild(lastChild);
			addPage();
			configPageHeader(pageHeader);			
			pg = getPageEle();
			lastChild.id = format("masterBand_%s_%s", [getPage(), bandCount]);
			pg.appendChild(lastChild);
		};
	};
	
	var configPageHeader = function(pageHeaderData){		
		var components = pageHeaderData.components;
        var style = pageHeaderData.style;        		
		addPageHeader(style);
      	if(components != undefined){
			var i = 0;
			for(i = 0; i <= components.length - 1; i++){
				if(components[i].type == "label"){
					addLabel("pageHeader_" + getPage(), components[i].name, components[i].text, components[i].style);					
				}else if(components[i].type == "p"){
					addP("pageHeader_" + getPage(), components[i].name, components[i].text, components[i].style);					
				}else if(components[i].type == "div"){
					addDiv("pageHeader_" + getPage(), components[i].name, components[i].text, components[i].style);					
				};	
			};
		};
	};

	var applyStyle = function(){
		getE("head")[0].innerHTML +=
		"<meta charset='UTF-8'>"+
		"<style type='text/css'> "+
        " .body.vReport{ "+
        "   background-color:#E6E6E6; "+
        "  } "+
        ".page{ "+
        " background-color:white; "+
        "} "+

        ".pageHeader, .masterBand, .pageFooter{ "+
        " display : inline; "+
	    " float: left; "+
	    " width: 100%;	"+
        " }  "+
        ".progress-bar { "+
        "	float: left; "+
        "	width: 0; "+
        "	height: 100%; "+
        "	font-size: 12px; "+
        "	line-height: 20px; "+
        "	color: #fff; "+
        "	text-align: center; "+
        "	background-color: #337ab7; "+
        "	-webkit-box-shadow: inset 0 -1px 0 rgba(0,0,0,.15); "+
        "	box-shadow: inset 0 -1px 0 rgba(0,0,0,.15); "+
        "	-webkit-transition: width .6s ease; "+
        "	-o-transition: width .6s ease; "+
        "	transition: width .6s ease; "+
        "} "+
		"#relContainer{ float:left; display:inline; width:100%;} "+
		"#tools{ "+
	    "  float:left; "+
		"  width:100%; "+
		"  display:inline;"+
		"  background-color : #F0F5F5;"+
		"  height: 50px;"+
        "  margin-bottom : 3px; "+		
		" } "+
        "</style>";
	};
	    
	
	this.view = function(){		                  
		vmsisLib.waitting.start();
        var pageHeader = data.pageHeader;
		var masterBand = data.masterBand;
        var row = [];    
        applyStyle();

		if(masterBand.bandData != undefined){		    		    			
			addPage();
		    configPageHeader(pageHeader);
			var i = 0;
			var a = 0;
			var b = 0;			
			var component = undefined;
			for(i = 0; i <= masterBand.bandData.length - 1; i++){
				addMasterBand(masterBand.style);
				row = masterBand.bandData[i];
				
				for(a = 0; a <= masterBand.components.length - 1; a++){
					component = masterBand.components[a];
					if(component.type == "dataLabel"){
						for(b = 0; b <= row.length - 1; b++){
							if (row[b].name == component.dbLink){
								addLabel(format("masterBand_%s_%s", [getPage(), i + 1] ) , component.name, row[b].value, component.style);
								checkPageSize(pageHeader, i + 1);								
							};
						};
					}else if(component.type == "dataP"){
						for(b = 0; b <= row.length - 1; b++){
							if (row[b].name == component.dbLink){
								addP(format("masterBand_%s_%s", [getPage(), i + 1] ) , component.name, row[b].value, component.style);
								checkPageSize(pageHeader, i + 1);								
							};					  
						};	
					}else if(component.type == "dataDiv"){
						for(b = 0; b <= row.length - 1; b++){
							if (row[b].name == component.dbLink){
								addDiv(format("masterBand_%s_%s", [getPage(), i + 1] ) , component.name, row[b].value, component.style);
								checkPageSize(pageHeader, i + 1);
							};
                        };							
					}else if(component.type == "p"){
						addP(format("masterBand_%s_%s", [getPage(), i + 1] ) , component.name, component.text, component.style)
					};
				};
			};
		};		       
		vmsisLib.waitting.stop();
	}
};
