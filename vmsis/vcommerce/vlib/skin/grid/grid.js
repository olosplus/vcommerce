
function activeLine(line, columns){
  var tr = $(line);
  var parent = tr.parent().parent(".table-editable");
  if (parent.length > 0){
    var ok = (!tr.hasClass("rowactive"));
    if (ok == false){
      return false;
    }
    if(tr.attr("operation") == 'inserted'){
      $("table[parent = '"+parent.attr('id')+"']").each(function(){
        $(this).find("tbody tr").addClass("notvis");
        $(this).find("tr[data-parent-indexrdow='" + tr.attr("data-indexrow") +"']").removeClass("notvis");
      });      
    }else{
      
      if ((($("table[parent = '"+parent.attr('id')+"']").find("tr[operation='inserted']").length > 0 || 
            $("table[parent = '"+parent.attr('id')+"']").find("tr[operation='updated']").length > 0)) &&
          (ok == true) ){
        ok = false;
        var msg = 'Existem dados não salvos. Deseja prosseguir e perder os dados não salvos? '+
          'Caso não queira perder os dados não salvos, cancele e salve-os.';
        ok = confirm(msg);
        if (ok == false){
          return false;
        };
      };
      if (ok == true){
        $("table[parent = '"+parent.attr('id')+"']").each(function(){
          GetGridEditable($(this).attr('module'), $(this).attr('id'), "", columns, parent.attr("id"),
            parent.attr('module'), tr.find("td [name='id']").val());
        });      
      };
    };    
    $("#" + parent.attr("id") + "  .rowactive").removeClass("rowactive");    
    tr.addClass("rowactive");
    SetChangesLine($('#' + parent.attr('parent')).find(".rowactive .gridtag").first());
  };
}

function SetChangesLine(element) {
  parent = $(element).parent().parent();
  if (parent.attr('operation') != 'inserted') {
    parent.attr('operation', 'updated');
  };
};

function RemoveSelectedRows(idGrid) {
  grid = $('#' + idGrid);
  //grid.find('tr[sel="true"]').remove()
  grid.find('tr[sel="true"]').each(function(){
    $("[parent='" + grid.attr("id") + "']").find("tbody tr").remove();
    $(this).remove();
  });
};

function ClearOperations(idGrid){
  grid = $('#' + idGrid);
  grid.find('tr[sel="true"]').attr('sel', 'false');
  grid.find('tr[operation="inserted"]').attr('operation', '');
  grid.find('tr[operation="updated"]').attr('operation', '');
}

function selectLine(element) {
  parent = $(element).parent().parent().parent();

  if (element.checked === true) {
    parent.attr('sel', 'true');
  } else {
    parent.attr('sel', 'false');
  };
  return true;
}

function JoinToJson(key, value) {
  var val_alt = value;
  val_alt = val_alt.replace(/'/g, " ");
  val_alt = val_alt.replace(/"/g, " ");
  val_alt = val_alt.replace("\\", "\\\\");
  return '"' + key.replace(" ", "") + '":"' + val_alt + '",';
};


function GetGridChange(idGrid, operation) {
  var line_separator = "<<LINE_SEPARATOR>>";
  if (operation === 'sel') {
    var list_tr = $('#' + idGrid + ' tr[sel="' + true + '"]');
  } else {
    var list_tr = $('#' + idGrid + ' tr[operation="' + operation + '"]');
  };
  var str_json = '';
  var str_row = '';
  for (tr in list_tr) {
    
    if (list_tr.hasOwnProperty(tr)) {
      if (isNaN(tr)) 
        continue
      
      tds = list_tr[tr].children;
      if (list_tr[tr].childElementCount > 0) {
        str_row = '{' + JoinToJson("data-indexrow", list_tr[tr].getAttribute('data-indexrow'));
        str_row +=  JoinToJson("data-parent-indexrow", list_tr[tr].getAttribute('data-parent-indexrow'));
      };
      for (td in tds) {
        if (tds.hasOwnProperty(td)) {
          if (tds[td].childElementCount > 0) {
            element = tds[td].children[0];
            if (element.nodeName === "INPUT" || element.nodeName === "TEXTAREA") {
              str_row += JoinToJson(element.name, element.value);
            };
            if (element.nodeName === "SELECT") {
              if (element.selectedIndex > -1) 
                str_row += JoinToJson(element.name, element.options[element.selectedIndex].value);
            };
          };
        };
      };
    };
    if (list_tr[tr].childElementCount > 0) {
      str_row = str_row.substr(0, str_row.length - 1);
      str_row += '}' + line_separator + " ";
      if (str_row != '}' + line_separator + " ") {
        str_json += str_row;
      };
    };
  };
  str_json = str_json.substr(0, str_json.length - 1);

  return str_json;
};

function getAttrGrid(idGrid, attr) {
  var grid = $("#" + idGrid);
  return grid.attr(attr)
}

function ParseGridToJson(idGrid) {
  return {
    rows_inserted: GetGridChange(idGrid, "inserted"),
    rows_updated: GetGridChange(idGrid, "updated"),
    model: getAttrGrid(idGrid, 'mod'),
    module: getAttrGrid(idGrid, 'module'),
    link_to_form: getAttrGrid(idGrid, 'link_to_form'),
    parent : getAttrGrid(idGrid, 'parent'),
    grid_id: idGrid
  };
}

function ParseGridToJsonDelete(idGrid) {
  return {
    rows_deleted: GetGridChange(idGrid, "sel"),
    model: getAttrGrid(idGrid, 'mod'),
    module: getAttrGrid(idGrid, 'module')
  };
}

function InsertEmptyRow(columns, idGrid, link_to_form) {
  var html_input = "<input type='{{TYPE}}' value='{{VALOR}}' {{DISABLE}} {{STEP}} " + "class = 'gridtag' name = {{NAME}} onchange='SetChangesLine(this)'></input>";
  var type_input = "";
  var data_row = 1;
  var last_tr = $("#" + idGrid + " > tbody > tr").last();
  var parent_data_index = null;
  
  var parent_grid = $("#" + $("#" + idGrid).attr("parent")).last();
  
  if(parent_grid != undefined && parent_grid != null) {
    parent_data_index = parent_grid.find(".rowactive").last().attr("data-indexrow");
  };
  
  if(parent_data_index == undefined || parent_data_index == null) {
    parent_data_index = "";
  };

  if(last_tr != undefined){
    var last_index = last_tr.attr('data-indexrow');
    if(last_index != "" && last_index != undefined)
      data_row = parseInt(last_index) + 1;
  };

  html = "<tr operation='inserted' sel='true' data-indexrow='"+data_row+"' onclick='activeLine(this, "+
    JSON.stringify(columns) +")' "+
         " data-parent-indexrow = "+parent_data_index+">";
  html += "<td> <center><input type='checkbox' checked onchange='selectLine(this)'></input> </td></center>";
  for (column in columns) {
    if (columns.hasOwnProperty(column)) {
      if (columns[column].type === 'link') {
        continue;
      };
      if ((columns[column].name === "id") || (columns[column].name === link_to_form)) {
        html += "<td class='notvis'>";
      } else {
        html += "<td>";
      };
      //for inputs
      if ((columns[column].type != 'select') && (columns[column].type != 'link') 
         /*&& (columns[column].type != 'textarea')*/) {
        html += html_input.replace('{{TYPE}}', columns[column].type);
        html = html.replace('{{VALOR}}', "");
        html = html.replace('{{DISABLE}}', '');
        html = html.replace('{{NAME}}', columns[column].name);
        if (columns[column].type === 'decimal') {
          html = html.replace("{{STEP}}", "step='any'");
        } else {
          html = html.replace("{{STEP}}", "");
        };
      };
/*      if (columns[column].type === 'textarea') {
        html += "<textarea class = 'gridtag' name='" + columns[column].name + "' onchange='SetChangesLine(this)'>" + "</textarea>";
      };*/
      if (columns[column].type == 'select') {
        if (columns[column].options != 'undefined') {
          var options = columns[column].options;
          var values = columns[column].values;
          var selected = "selected";
          var model = columns[column].model;
          var module = columns[column].module;
          var url = columns[column].url;
          var name = columns[column].name;

          var popupScript = "";
          if(url){
            popupScript += "ondblclick='insert(\""+ model +"\", \""+ module +"\", \""+ url +"\",\""+name +"\")'"
          }

          html += "<select class = 'gridtag' name='" + columns[column].name + "' onclick='SetChangesLine(this)' "+
          popupScript + " >";
          for (option in options) {
            if (options.hasOwnProperty(option)) {
              html += "<option value='" + values[option] + "'";
              
              if (selected != "")
                html += selected;
               
              html += ">";
              html += options[option] + "</option>";
            };
            selected = "";
          };
          html += "</select>";
        };
      };
    };
    html += "</td>";
  };
  html += "</tr>";
  body = $("#" + idGrid + "> tbody");
  $("#" + idGrid + "> tbody").append(html);
};

function InsertLineWithValue(row, columns, readonly, link_to_form, index_row, idGrid) {
  var html_input = "<input type='{{TYPE}}' value='{{VALOR}}' {{STEP}} class = 'gridtag' name = " + "{{NAME}}  onchange='SetChangesLine(this)'>" + "</input>";
  var type_input = "";
  var class_links = "";
  var events = "";
  var index = 0;
  var options = undefined;
  var values = undefined;
  var parent_data_index = null;
  
  var parent_grid = $("#" + $("#" + idGrid).attr("parent")).last();
  
  if(parent_grid != undefined && parent_grid != null) {
    parent_data_index = parent_grid.find(".rowactive").last().attr("data-indexrow");
  };
  
  if(parent_data_index == undefined || parent_data_index == null) {
    parent_data_index = "";
  };

  html = "<tr data-indexrow='" + index_row + "' onclick='activeLine(this, "+ JSON.stringify(columns) +")' "+
    "data-parent-indexrow= "+ parent_data_index+">";
  if (readonly === "False") {
    html += "<td> <center><input type='checkbox' onchange='selectLine(this)'> " + "</input> </td></center>";
  };
  for (column in columns) {
    if (columns.hasOwnProperty(column)) {
      if ((columns[column].type === 'link') && (readonly === "False")) {
        continue;
      };
      if ((columns[column].name === "id") || (columns[column].name === link_to_form)) {
        html += "<td class = 'notvis'>";
      } else {
        html += "<td>"
      }
      //for inputs
      if ((columns[column].type != 'select') && (columns[column].type != 'link') && 
          /*(columns[column].type != 'textarea')*/  (columns[column].type != "") && 
          (columns[column].type != "select-readonly") ) {
        html += html_input.replace('{{TYPE}}', columns[column].type);
        html = html.replace('{{VALOR}}', row.v[index]);
        html = html.replace('{{NAME}}', columns[column].name);
        if (columns[column].type === 'decimal') {
          html = html.replace("{{STEP}}", "step='any'");
        } else {
          html = html.replace("{{STEP}}", "");
        };
      };
/*      if (columns[column].type === 'textarea') {
        html += "<textarea class = 'gridtag' name='" + columns[column].name + "' onchange='SetChangesLine(this)'>" + row.v[index] + "</textarea>"
      };*/
      if ((columns[column].type === 'link') && (readonly === "True")) {
        if (columns[column].name === "update") {
          class_links = "fa fa-pencil";
        } else {
          if (columns[column].name = "delete") {
            class_links = "fa fa-trash-o";
            events = 'return confirm("Deseja realmente deletar este registro ?")';
          };
        };
        html += "<center><a  href = '" + row.v[index] + "' class='" + class_links + "' title= '" + columns[column].label + "' onclick='" + events + "'>" + "</a></center>";
      };
      
      if(columns[column].type == 'select-readonly'){
        if (columns[column].options != 'undefined') {
          options = columns[column].options;
          values = columns[column].values;

          for (option in options) {
            if (options.hasOwnProperty(option)) {        
              if (row.v[index] === values[option]) {
                html += options[option];
              };
            };
          };
        }  
      };

      if (columns[column].type == 'select') {
        if (columns[column].options != 'undefined') {
          options = columns[column].options;
          values = columns[column].values;
          var model = columns[column].model;
          var module = columns[column].module;
          var url = columns[column].url;
          var name = columns[column].name;

          var popupScript = "";
          if(url){
            popupScript += "ondblclick='insert(\""+ model +"\", \""+ module +"\", \""+ url +"\",\""+name +"\")'"
          }
          
          html += "<select  class='gridtag' name='" + columns[column].name + "' " + 
            " onclick='SetChangesLine(this)' onkeydown='SetChangesLine(this)' "+ popupScript +">";
          for (option in options) {
            if (options.hasOwnProperty(option)) {
              html += "<option value='" + values[option] + "'";
              if (row.v[index] === values[option]) {
                html += "selected>";
              } else {
                html += ">";
              };
              html += options[option] + "</option>";
            };
          };
          html += "</select>";
        };
      };
      if (columns[column].type === "") {
        html += row.v[index];
      };
    };
    html += "</td>";
    index += 1;
  };

  html += "</tr>";
  return html
};

function ShowError(input_error){
  $('.errorgrid').attr('title', '');
  $('.errorgrid').removeClass('errorgrid');
  var value = input_error.value;
  var grid_id = input_error.name;
  var row = input_error.getAttribute("data-indexrow");
  
  if(row == -1){
    alert(value);
  };

  var list = value.split(",");
  var ele_sel = undefined;
  var ele = undefined;
  var ele_sel_name = "";
  var i = 0;  
  
  for(i = 0; i <= list.length - 1; i++ ){
    ele_sel_name = list[i].split(":")[0]
    ele_sel_name = ele_sel_name.replace('[', '').replace(']', '');
    ele_sel = $("#" + grid_id + " tr[data-indexrow='" + row + "']");
    ele = ele_sel.find('[name= '+ ele_sel_name + ']');
    if (ele[0] == undefined)
      ele = ele_sel.find('[name= '+ ele_sel_name + '_id]');
    ele.addClass("errorgrid");
    ele.attr('title', list[i].split(":")[1].replace('[', '').replace(']', ''))
  };
}

function Grid(DivGridId, Data) {

  var columns = Data.columns;
  var rows = Data.rows;
  var bar = Data.bar;
  var module = Data.grid_key;
  var grid_id = Data.grid_mod;
  var model = Data.grid_mod;
  var use_crud = Data.use_crud;
  var readonly = Data.read_only;
  var url_insert = Data.url_insert;
  var url_update = Data.url_update;
  var url_delete = Data.url_delete;
  var parent = Data.parent;
  var link_to_form = Data.link_to_form;
  var pages = parseInt(Data.number_of_pages);
  var selected_page = parseInt(Data.selected_page);
  var title = Data.title;

  if (readonly === "True"){
    var table_class = 'tablegrid table table-condensed table-hover table-striped table-readonly'
  }else{
    var table_class = 'tablegrid table table-bordered table-hover table-striped table-editable'
  }; 

  var html = "";
  
  if (readonly === "True") {
    html += "<div class='grid panel-default panel-customizado'>";
    html += "<div class='panel-heading grid-custom-title'>";
    for (item_bar in bar) {
      if (bar.hasOwnProperty(item_bar)) {
        if ((bar[item_bar].type === 'link') && (readonly === "True")) {
          html += "<a class = 'fa fa-file-o' href = '" + bar[item_bar].value + "' title='" + 
            bar[item_bar].label + "'>" + "</a> <div class='separador'>|</div> ";
        };
      };
    };

    html += "<a class = 'glyphicon glyphicon-search' href='javascript:void(0)' "+
      "onclick='Filter(\"" + module + "\", \"" + model + "\", " + JSON.stringify(columns)  +
      "  )' title='Filtrar' ></a>";
    html += "<div class='separador'>|</div> <a class='glyphicon glyphicon-print' href='javascript:void(0)' "+
      "title='Relatório'  onclick='Print(\"" + module + "\", \"" +
              model + "\", " + JSON.stringify(columns)  +
            ", \"id\", \""+ title +" \")'> </a>";
    html += "<div class='separador'></div>  <div class='separador'></div>";
    
    html +=  "<strong style='font-size:20px'>" + title + "</strong>";
    html += "</div>"
  }
  else{
    html += "<div class='grid panel panel-default panel-customizado' >";
    html += "<div class='panel-heading'>" + title + "</div>";
  };
  html += "<div class='panel-body'>"
  html += "<table id='" + grid_id + "' parent='" + 
    parent + "'" + "link_to_form='" + link_to_form + "'" +
    " class='"+ table_class + "' module='" +
     module + "' " + "mod='" + model + "'><thead class = 'header'> <tr>";

  if(readonly === "False") {
    html += "<th><center>*</center></th>";  
  };

  for (column in columns) {
    if (columns.hasOwnProperty(column)) {
      if ((columns[column].type === 'link') && (readonly === "False")) {
        continue;
      };

      if ((columns[column].name === "id") || (columns[column].name === link_to_form)) {
        html += "<th class='notvis'>" + columns[column].label + " </th>";
      } else {
        if (columns[column].type != "link" && readonly === "True"){
          html += "<th>" + columns[column].label + 
            " <a class='glyphicon glyphicon-triangle-bottom' onclick='get_grid_orderly(\"" + module + "\", \"" +
              model + "\", " + JSON.stringify(columns)  +
            ", \"" + columns[column].name + "\")' href='javascript:void(0)'></a></th>";
        }else{
          html += "<th>" + columns[column].label + "</th>";
        };  
      };
    };
  };

  html += "</tr></thead>";
  html += "<tbody>"
  var index_row = 0;
  for (row in rows) {
    if (rows.hasOwnProperty(row)) {
      index_row += 1;
      html += InsertLineWithValue(rows[row], columns, readonly, link_to_form, index_row, grid_id)
    };
  };

  html += "</tbody>";
  html += "</table>";
  html += "</div>"; 
  html += "<div class='panel-footer'>";  
  if (readonly === "False") {
    
    html += "  <a href='javascript:void(0)' class='fa fa-file-o' title='Adicionar'" + 
      "onclick='InsertEmptyRow(" + JSON.stringify(columns) + ",\"" + grid_id + "\", \"" + link_to_form + "\" )'>" +
       "</a> | ";

    html += "  <a href='javascript:void(0)' id='linkcancel' class='glyphicon glyphicon-floppy-remove' " +
      "onclick='RemoveSelectedRows(\"" + grid_id + "\" )' title='Cancelar'>" + "</a> | ";

    html += "  <a href='javascript:void(0)' onclick='doDeleteGrid(\"" + grid_id + "\")' class = 'fa fa-trash-o' " + 
      "title='Deletar selecionados'></a>  ";

/*    html += "  <a href='javascript:void(0)' onclick='doPostGrid(\"" + grid_id + "\")' class='glyphicon glyphicon-floppy-disk' " + 
      " title='Salvar'></a>"; */
  
  }else{
    html += "<div class='navigation' >";
    html += "<div class='navigation-centralize'>"
    html += "<div class='inline' id='div_prior'>"
    html += "<ul class='pagination'> <li>"
    html += "<a href='javascript:void(0)' aria-label='Previous' onclick='ControlPagination(" + pages + "," + 
      JSON.stringify(columns) + "," + 
      selected_page.toString() + ",\"" + module + "\",\"" + model + "\"," + " \"prior\")'> "+         
      "<span aria-hidden='true'>&laquo;</span></a> </li></ul></div>";    
    html += "<nav>";
    html += "<ul class='pagination'>";
    html += "</ul>"
    html += "</nav>"; 
    html += "<div class='inline' id='div_next'>"
    html += "<ul class='pagination'> <li>"
    html += "<a href='javascript:void(0)' aria-label='Next' onclick='ControlPagination(" + pages + "," + 
      JSON.stringify(columns) + "," + 
      selected_page.toString() + ",\"" + module + "\",\"" + model + "\"," + " \"next\")'> "+         
      "<span aria-hidden='true'>&raquo;</span></a> </li></ul></div>";    
    html += "</div>";
    html += "</div>"    
  };
  
  html += "</div>";
  html += "</div>"
  $("#" + DivGridId).html(html);
  ControlPagination(pages, columns, selected_page, module, model, "");

};

function doPostGrid(idGrid) {
  var parent = $('#' + idGrid).attr('parent');
  var sequence = "";
  var send_to = $('#ownurl').val();
  var redirect_to = $('#listurl').val();

  if ((parent != "") && (parent != undefined)) {
    sequence = $('#' + parent).attr('sequence');
    var link_to_form = $('#' + idGrid).attr('link_to_form');
    if ((sequence != "") && (sequence != undefined)) {
      $("#" + idGrid + " input[name= '" + link_to_form + "'").each(function () {
        $(this).attr("value", sequence);
      });
    } else {
      sequence = "";
    };
  };
  if (parent != "") {
    if(sequence === "" || sequence === undefined) {   
      doPostForm(send_to, parent, redirect_to, false, "");
    }else{
      doPostForm(send_to, parent, "", false, "");
    }

  } else {
    var jsgrid = ParseGridToJson(idGrid);
    $.ajax({
      url: '/savegrid',
      type: 'get',
      //this is the default though, you don't actually need to always mention it
      data: jsgrid,
      success: function (data) {
        var parser = new DOMParser()
        var doc_received = parser.parseFromString(data, "text/html");
        var erros = doc_received.getElementById('grid_erros');
        if (erros != null) {
           ShowError(erros);
        } else {
          ClearOperations(idGrid);
          
          alert('Dados salvos com sucesso!');
        }
      },
      failure: function (data) {
        alert('Got an error dude');
      }
    });
  };
};

function doDeleteGrid(idGrid) {
  var parent = $('#' + idGrid).attr('parent');
  if (parent === "") {
    jsgrid = ParseGridToJsonDelete(idGrid);
    $.ajax({
      url: '/deletegrid',
      type: 'get',
      //this is the default though, you don't actually need to always mention it
      data: jsgrid,
      success: function (data) {
        alert(data);
        RemoveSelectedRows(idGrid);
      },
      failure: function (data) {
        alert('Got an error dude');
      }
    });
  } else {
    var send_to = $('#ownurl').val();
    var redirect_to = $('#listurl').val();
    doPostForm(send_to, parent, "", true, idGrid);
    RemoveSelectedRows(idGrid);
  };
}

// using jQuery

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getJsonChildGrids(id){
    var script = "";
    $('table[parent="' + id + '"]').each(function () {
      script += JSON.stringify(ParseGridToJson($(this).attr('id'))) + "[[<<ROW_SEPARATOR>>]]";
      script += getJsonChildGrids($(this).attr('id'));
    });
    return script;
}

function doPostForm(send_to, form_id, url_redirect, is_delete, id_grid_delete, close_window) {
  vmsisLib.waitting.start();
  close_window = close_window || false;
  var form = $('#' + form_id);
  if(form.attr('tagName') != 'form'){
    form = $('form').first();
  };
  var url = send_to;
  var csrftoken = getCookie('csrftoken');
  var jsgrid = "";
  if (is_delete === false) {
    //$('table[parent="' + form_id + '"]').each(function () {
    //  jsgrid += JSON.stringify(ParseGridToJson($(this).attr('id'))) + "[[<<ROW_SEPARATOR>>]]";
    //});
    jsgrid += getJsonChildGrids(form_id);
  } else {
    jsgrid += JSON.stringify(ParseGridToJsonDelete(id_grid_delete)) + "[[<<ROW_SEPARATOR>>]]";
  };

  form.append("<input type='hidden' name='child_models' value='" + jsgrid + "'></input>");

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  $.ajax({
    url: url,
    type: 'post',
    data: form.serialize(),
    success: function (data) {
      vmsisLib.waitting.stop();
      var parser = new DOMParser()
      var doc_received = parser.parseFromString(data, "text/html");
      var frm_received = doc_received.getElementById(form_id);
      if (frm_received === null) {
        var erros = doc_received.getElementById("grid_erros");
        if (erros != null) {
          ShowError(erros)
        } else {
          if (url_redirect != "") {
            window.location.href = url_redirect;
          } else {            
            $('table[parent="' + form_id + '"]').each(function () {
              ClearOperations($(this).attr('id'));
            })
            alert('Dados atualizados com sucesso!');
          };
        };
      } else {
        var frm = document.getElementById(form_id);
        if (frm_received.innerHTML === "") {
          if (url_redirect != "") {
            window.location.href = url_redirect;
          } else {
            ClearOperations(idGrid);
            alert('Dados atualizados com sucesso!');
          }
        } else {
          var ownurl = doc_received.getElementById('ownurl');
          var errorList = doc_received.getElementsByClassName('errorlist');
          if(ownurl != undefined && ownurl != null && errorList.length ==0){
            if(url_redirect != undefined && url_redirect != ""){
              window.location.href = url_redirect;
            }else{
              window.location.href = ownurl.value;   
            }
          }else{
            frm.innerHTML = frm_received.innerHTML;
            return false;
          };
        }
      }      
      if(close_window){
        window.close();              
      }
      
    },
    error: function (data) {
      vmsisLib.waitting.stop()
      alert(data.responseText);
    }
  });
  return false;
};

function get_grid_orderly (module, model, columns, column) {
  $("#grid_order_by").remove();
  $('body').append('<input type="hidden" id="grid_order_by" value = "'+  column +'">');
  get_grid_page(module, model, columns, 1);
}

function get_grid_page (module, model, columns, page) {
  var filter = $("#filter_cache").val();
  var palavras_inteiras = $("#palavras_inteiras").val();
  
  ordenacao = $("#grid_order_by").val();

  if(filter === undefined){
    filter = "";
  }else{
    filter = JSON.parse(filter)
  };

  if(palavras_inteiras === undefined){
    palavras_inteiras = "";
  };

  GetGridData(module, model, filter, columns, palavras_inteiras, page, ordenacao);
  
}

function GetGridData (module, model, filter, columns, partial_search, page, order_by) {
  var modulo = module;
  var modelo = model;
  var colunas = columns;    
  var filtro = "";
  var ordernar = order_by;

  if (filter != ""){
    filtro = JSON.stringify(filter);    
  };

  var pagina = page;
  
  $.ajax({
    url: '/getgrid',
    type: 'get',
    data: {"module" : modulo, "model" : modelo, "columns" : JSON.stringify(colunas), "form_serialized" : filtro,
      "partial_search" : partial_search, "page" : pagina, "order_by" : ordernar},
    success: function (data) {
      dados = JSON.parse(data);
      Grid("div_" + modelo, dados)
    },
    failure: function (data) {
      alert('Got an error dude');
    }
  });       
}

function GetGridEditable(module, model, filter, columns, parent, parent_module, parent_id) {
  var modulo = module;
  var modelo = model;
  var colunas = columns;    
  var filtro = "";

  if (filter != ""){
    filtro = JSON.stringify(filter);    
  };
  
  $.ajax({
    url: '/getgrideditable',
    type: 'get',
    data: {"module" : modulo, "model" : modelo, "columns" : JSON.stringify(colunas), "form_serialized" : filtro,
      "partial_search" : "", "page" : "", "order_by" : "", "parent_model" : parent, "parent_module": parent_module,
      "parent_id": parent_id },
    success: function (data) {
      dados = JSON.parse(data);
      Grid("div_" + modelo, dados)
    },
    failure: function (data) {
      alert('Got an error dude');
    }
  });       
}


function ControlPagination(total_pages, columns, selected_page, module, model, command){  
  var section_paginate = $("#section_paginate").val();
  
  var pages_in_section = 12;
  var next_section = 0;
  var initial_page = 0;
  var end_page = 0;

  if(command === "" && section_paginate != undefined){
    next_section = section_paginate;
  };
 
  if( (command === "prior" && section_paginate === "1") || 
      (command === "next" && parseInt(section_paginate) >= (total_pages/pages_in_section)  )){
    return;
  };

  if (section_paginate === undefined) {
    if(command === "next"){
      next_section = 2;
    }else if(command === "prior" || command === ""){
      next_section = 1;
    };
  }else{
    if(command === "next"){
      next_section = parseInt(section_paginate) + 1;
    }else if(command === "prior"){
      next_section = parseInt(section_paginate) - 1;
    };
  };
  
  initial_page = ( (next_section - 1) * pages_in_section);
  end_page = initial_page + pages_in_section;

  if (initial_page > total_pages)
    initial_page = 0;

  if (end_page > total_pages)
    end_page = total_pages;

  var class_selected_page = "";
  var html = "";

  for(var i = initial_page + 1; i <= end_page; i++){
    if (selected_page === i){
      class_selected_page = "active disabled selected-page";
    }else{
      class_selected_page = "no-selected-page";
    };

    html += "<li class='"+ class_selected_page +"' ><a href='javascript:void(0)' onclick='get_grid_page(\"" + 
      module + "\", \"" + model + "\", " +
      JSON.stringify(columns)  + "," + i.toString() + ")' >" +
      i.toString() +"</a></li>";
  };

  if (section_paginate === undefined) {
     $("body").append("<input id='section_paginate' type='hidden' value='"+ next_section + "'>");
  }else{
    $("#section_paginate").val(next_section);
  };

  $("nav > .pagination").html(html);
  PaginagionCentralize();
}

function PaginagionCentralize(){
  main_width = $(".navigation").width();
  child_width = 0

  $(".pagination").each(function(){
    child_width += $(this).width()
  });
    
  width_wrap = (main_width - child_width) / 2;
  $("#navigation-wrapper").remove();
  $(".navigation").prepend("<div id='navigation-wrapper' class='inline'></div>");
  $("#navigation-wrapper").width(width_wrap);
  $("#navigation-wrapper").height(35);
}

function Print(module, model, columns, column, title){
  var filter = $("#filter_cache").val();
  var palavras_inteiras = $("#palavras_inteiras").val();
  var filtro = ""; 
  ordenacao = $("#grid_order_by").val();

  if(filter === undefined){
    filter = "";
  }else{
    filter = JSON.parse(filter)
  };
 
  if (filter != ""){
    filtro = JSON.stringify(filter);    
  };

  if(palavras_inteiras === undefined){
    palavras_inteiras = "";
  };

    $.ajax({
      url: '/printgrid',
      type: 'get',
      //this is the default though, you don't actually need to always mention it
      data: {"module" : module, "model" : model, "columns" : JSON.stringify(columns), "form_serialized" : filtro,
      "partial_search" : palavras_inteiras, "page" : -1, "order_by" : ordenacao, "title" : title},

      success: function (data) {
        var response = eval(data);

 //       var parser = new DOMParser()
//        var doc_received = parser.parseFromString("", "text/html");
        var winRel = window.open("", title, "_blank");
        var report = new vReport("A4 portrait", "body", response, winRel.document );       
        report.view();
        

                
//        var fileCode = doc_received.getElementsByTagName("html")[0].innerHTML;
//        fileCode = "<html> " + fileCode + "</html>";
//        var fileBlob = new Blob([fileCode], {type: 'text/html'});
//        var url = URL.createObjectURL(fileBlob);
//        var myWindow = window.open(url);

      },
      failure: function (data) {
        alert('Got an error dude');
      }
    });

}