$(document).ready(function(){
    
    var apps =  JSON.parse($("#list_apps").val());
    var usuarios = JSON.parse($("#list_users").val());
    
    var getPermissoesUsuario = function(item){
        var listbox = vmsisLib.listBox;
        var usuario_id = listbox.getVal('div-filtro-usuario');
        if (!usuario_id) {
            alert('Primeiro selecione o usuário.');
            listbox.setFocus('div-filtro-usuario');
            return false;
        }
        var modulo = listbox.getVal('div-escolha-app-usuario');
        
        var addCheckBox = function(name, checked, label){
             var html = "<div>";
             if (checked) {                        
                 html += vmsisLib.format("<input type='checkbox' checked name='%s'>", [name]);
             }else{
                 html += vmsisLib.format("<input type='checkbox' name='%s'>", [name]);
             }                    
             html += vmsisLib.format("<label for='%s'>%s</label>", [name, label]);
             html += "</div>";
             return html;
        }
        
        $.get('get_permissoes/',
            {'module': modulo, 'id_funcionario': usuario_id})
            .done(function(data){
                source = eval(data);
                html = "";
                
                for (app in source) {
                    html += vmsisLib.format("<div class='col-md-12 container-permissions' data-model='%s'>",
                                            [source[app].model]);                    
                        html += "<p>" + source[app].verbose_name + "</p>";                                        
                        html += addCheckBox('usuario_can_add', source[app].can_add, 'Permitir adicionar');
                        html += addCheckBox('usuario_can_change', source[app].can_change, 'Permitir modificar');
                        html += addCheckBox('usuario_can_delete', source[app].can_delete, 'Permitir excluir');
                    html += "</div>";        
                }
                $("#div-permissoes-usuario").html(html);
                if (source.length > 0) {
                    $("#btn-salvar-per-usuario").attr("disabled", false);
                    $("#alert-permissoes-usuario").css("display", "none");
                }else{
                    $("#btn-salvar-per-usuario").attr("disabled", true);
                    var alert = $("#alert-permissoes-usuario");
                    alert.css("display", "block");
                    alert.html("Nenhuma permissão pode ser fornecida.");
                }
            })
    }
    
    var setPermissoesUsuario = function(){
        
        var permissoes = [];
        if (!$("#btn-salvar-per-usuario").attr("disabled")) {
            $("#div-permissoes-usuario .container-permissions").each(function(){                                                            
                var can_add = $(this).find("input[name='usuario_can_add']").first().prop("checked");
                var can_change = $(this).find("input[name='usuario_can_change']").first().prop("checked");
                var can_delete = $(this).find("input[name='usuario_can_delete']").first().prop("checked");
                var model = $(this).attr("data-model");
                
                var listbox = vmsisLib.listBox;
                var usuario_id = listbox.getVal('div-filtro-usuario');
                
                if (!usuario_id) {
                    alert('Primeiro selecione o usuário.');
                    listbox.setFocus('div-filtro-usuario');
                    return false;
                }
                var modulo = listbox.getVal('div-escolha-app-usuario');

                if (!modulo) {
                    alert('Primeiro selecione o módulo.');
                    listbox.setFocus('div-escolha-app-usuario');
                    return false;
                }
                var modules = modulo.split('.');
                var app_label = modules[modules.length - 1];

                permissoes.push({"model" : model, "can_add" : can_add, "can_change" : can_change,
                                 "can_delete" : can_delete, "usuario" : usuario_id, "app_label" : app_label});
            });
        
            $.get("/set_permissoes", {"data" : JSON.stringify(permissoes)}).
            done(function(data){
                alert(data);    
            })
        }
    }
    
    var listBox = vmsisLib.listBox;
    listBox.new(usuarios, 'div-filtro-usuario', 'Usuários:', getPermissoesUsuario);
    listBox.new(apps, 'div-escolha-app-usuario', 'Telas:', getPermissoesUsuario);
    $("#btn-salvar-per-usuario").click(setPermissoesUsuario);
})
