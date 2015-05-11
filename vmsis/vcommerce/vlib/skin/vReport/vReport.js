/*

PageType - Estilo da página
  A4 - 
PageHeader - Div com tamanho de 100%

*/

vReport = function(pageType, container, data){	
    
    if(pageType == "A4"){	
	  var pageHeight = 1207; //default 3508 / 3 -- 1207
	  var pageWidth = 826.67; //default 2480 / 3 --826.67
	};
	
	var doc = document;
	var pages = 1;

    /*utilidade*/ 
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
    
	var format = function(str, list){
		var i = 0;		
		var text = str;
		for(i = 0; i <= list.length - 1; i++){
		   text = text.replace("%s", list[i]);		   
		};
		return text;
	};
	
	var body = getE(container)[0];    
    $('body').addClass('vReport');
    body.innerHTML = "";
	
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
		
		//lastChildTop = lastChildTop - ( (getPage() -1) * pageHeight)
		//lastChildTop + lastChildHeight > pageHeight
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
	
	this.view = function(){		
        var pageHeader = data.pageHeader;
		var masterBand = data.masterBand;
        var row = [];    
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
					};
				};
			};
		};		       
	}
};
