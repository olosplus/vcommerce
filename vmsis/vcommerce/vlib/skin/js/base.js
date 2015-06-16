function Inicializacao() {
  $('.errorlist').css('color','#990000');
  $('.errorlist').addClass('alert alert-danger');
  $('.ui-dialog-buttonset button').addClass('btn btn-outline btn-primary'); 
}

function hidePage(page){
  page.css('display', 'none');
}

function showPage(page){
  hideAllPages();
  page.css('display', 'block');
  $(".page-active").removeClass("page-active");
  btn = $("#btn-show-" + page[0].id);
  btn.addClass("page-active");
  btn.parent().addClass("page-active");
}

function hideAllPages(){
  $(".vmsis_pages").each(function(){
    hidePage($(this));
  });
}


function resizeFrame(iframe){  
  if(iframe){
    var body = iframe.contentWindow.document.body;  
    
    var heightNavigation = $('#open-pages-navigation').height();
    var pageTopHeight = $('#main-top-navigator').height()
    var winHeight = $(window).height();
    
    $(iframe).css({"min-height" : (winHeight - heightNavigation - pageTopHeight) + "px",
      "max-height" : (winHeight - heightNavigation - pageTopHeight ) + "px"});

    resizeCrud(iframe.id)
  };
}

function createPage(id, url, title){

  $("#open-pages-navigation").append('<div class="div-page-navi "><a class="pages-nav" '+
    ' onclick="showPage($(\'#'+ id +'\'))" id="btn-show-'+ id +'" >'+ 
    title + '</a> <a href="javascript:void(0)" onclick="destroyFrame(\''+id+'\')" class="page-close">x</a> </div>');

  var htmlPage =  "<iframe class='vmsis_pages' src='" + url + 
   "' id= '"+ id +"' onload='resizeFrame(this)'  "+
   " frameborder='0'> </iframe>";
  $("#main-container").append(htmlPage);

  showPage($("#" + id));

}

function destroyFrame(idFrame){
  $("#" + idFrame).remove();
  $("#btn-show-" + idFrame).parent().remove();
}

function resizeCrud(idFrame){
  
  framedoc = $("#" + idFrame).contents();
  if(framedoc.find("#main-panel").length > 0){
    var headerTop = framedoc.find("#main-panel > .panel-heading").first().offset().top;
    var headerHeight = framedoc.find("#main-panel > .panel-heading").first().height();
  
    var footerTop = framedoc.find("#main-panel > .panel-footer").first().offset().top;
    var footerHeight = framedoc.find("#main-panel > .panel-footer").first().height();
  
    var winHeight = $("#" + idFrame).height();

    var middleHeight = winHeight - headerHeight - footerHeight - headerTop - 70;
    framedoc.find("#main-panel > .panel-body").css({"max-height": middleHeight + "px", "overflow" : "auto"})
  };

}

function openPage(app, url, title){
  if (url.toLowerCase() != 'javascript:void(0)') {
    
    hideAllPages();

    var app_id =  "iframe-" + app.replace(/\./g, "-");

    ele_app = $("#" + app_id);
    if(ele_app.length > 0){
      showPage(ele_app);
    }
    else{
      createPage(app_id, url, title);
    }
  }
}

function insert(model, module, url, name){

    var w = $(window).width();
    var h = $(window).height();
    var left = (screen.width/2)-(w/2);
    var top = (screen.height/2)-(h/2);
    /*
    var myWindow = window.open(url, 'inserir', 'toolbar=no, location=no, '+
   'directories=no, status=no, menubar=no, scrollbars=yes, resizable=yes, copyhistory=no, width='+w+', '+
   'height='+h+', top='+top+', left='+left);
   */
   var myWindow = window.open(url, '', 'location=no, scrollbars=yes, width='+w+', '+  'height='+h+', top='+top+', left='+left);

    myWindow.onload = function(){
       this.document.getElementById("btn-salvar-inserir").style.display = "none"
       this.document.getElementById("btn-cancelar").style.display = "none"
       this.document.getElementById("header-title-link").setAttribute("href", "javascript:void(0)");
    }

    myWindow.onbeforeunload = function(){
      getDataLookup(model, module, 'id_' + name);
      this.close();
    }
}

function getDataLookup(model, module, id_component){
  $.ajax({
    url: 'getdatalookup/',
    type: 'get',
    data: {'model':model, 'module':module},
    success: function (data) {
      var dataLk = eval(data);
      
      var lookup = $("#" + id_component);
      
      if(lookup.length <= 0){
        lookup = $("[name='" + id_component.replace("id_", "") + "']");
      };

      var lkValue;
      lookup.each(function(){
        th = $(this);
        lkValue = th.val();
        th.empty();

        var newOption = $('<option value="-1">----------</option>');
        th.append(newOption);

        for(var i = 0; i <= dataLk.length - 1; i++){
          newOption = $('<option value="'+ dataLk[i].value +'">'+ dataLk[i].object +'</option>');
          th.append(newOption);
          th.trigger("chosen:updated");         
        }
        th.val(lkValue);
      });

    },
    error: function (data) {
      alert(data.responseText);
      return false;
    }
  });

}

$(document).ajaxComplete(function() {
  Inicializacao();  
});

$(document).ready(function() {
  Inicializacao();  
});