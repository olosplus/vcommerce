$(document).ready(function(){
    
   // var apps =  JSON.parse($("#list_apps").val());
   var usuarios = JSON.parse($("#list_users").val());
    
    var getPermissoesUsuario = function(item){
        var listbox = vmsisLib.listBox;
        var usuario_id = listbox.getVal('div-filtro-usuario');
        if (!usuario_id) {
            vmsisLib.aviso('Primeiro selecione o usuário.');
            listbox.setFocus('div-filtro-usuario');
            return false;
        }
        var modulo = this.getAttribute('data-module');
        
        if (!modulo) {
            return
        }
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
                    if (source[app].can_add != undefined) {
                       html += addCheckBox('usuario_can_add', source[app].can_add, 'Permitir adicionar');
                    }
                    if (source[app].can_change != undefined) {
                       html += addCheckBox('usuario_can_change', source[app].can_change, 'Permitir modificar');
                    }
                    if (source[app].can_delete != undefined) {
                       html += addCheckBox('usuario_can_delete', source[app].can_delete, 'Permitir excluir');
                    }
                    if (source[app].can_show != undefined) {
                       html += addCheckBox('usuario_can_show', source[app].can_show, 'Permitir visualizar');
                    }
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
            }).fail(function(data){
                vmsisLib.aviso(data);
            })
    }
    
    var setPermissoesUsuario = function(container_selector, check_btn_save){
        
        var permissoes = [];
        if (!$("#btn-salvar-per-usuario").attr("disabled") || !check_btn_save) {            
            $(container_selector).each(function(){                                                            
                var can_add = $(this).find("input[name='usuario_can_add']").first().prop("checked");
                var can_change = $(this).find("input[name='usuario_can_change']").first().prop("checked");
                var can_delete = $(this).find("input[name='usuario_can_delete']").first().prop("checked");
                var can_show = $(this).find("input[name='usuario_can_show']").first().prop("checked");
                var model = $(this).attr("data-model");
                
                var listbox = vmsisLib.listBox;
                var usuario_id = listbox.getVal('div-filtro-usuario');
                
                if (!usuario_id) {
                    vmsisLib.aviso('Primeiro selecione o usuário.');
                    listbox.setFocus('div-filtro-usuario');
                    return false;
                }
                var modulo = $("#treeViewApps .selected").attr("data-module");

                if (!modulo) {
                    vmsisLib.aviso('Primeiro selecione o módulo.');
                    listbox.setFocus('div-escolha-app-usuario');
                    return false;
                }
                var modules = modulo.split('.');
                var app_label = modules[modules.length - 1];

                permissoes.push({"model" : model, "can_add" : can_add, "can_change" : can_change,
                                 "can_delete" : can_delete,"can_show" : can_show, "usuario" : usuario_id,
                                 "app_label" : app_label});
            });
        
            $.get("/set_permissoes", {"data" : JSON.stringify(permissoes)}).
            done(function(data){
                vmsisLib.aviso(data);    
            })
        }
    }
    
    var aplicarConfiguracoesSubMenu = function(){
        var aplicar = function(ele){
            $("#treeViewApps").find('.selected').removeClass('selected');
            $(ele).addClass('selected');
            setPermissoesUsuario('#aplicar_permissao_sub_menus .popup-body', false);
        };
        $('.aplicarSubmenus').each(function(){
           aplicar(this);
        })
        $('.aplicarSubmenus').find('li').each(function(){
            aplicar(this);
        });
        vmsisLib.aviso('As permissões foram aplicadas com sucesso!');
        vmsisLib.popup.closePopup('aplicar_permissao_sub_menus');
    }
    
    var listBox = vmsisLib.listBox;
    listBox.new(usuarios, 'div-filtro-usuario', '', getPermissoesUsuario);
    vmsisLib.treeView("treeViewApps", getPermissoesUsuario);    
    
    $("#btn-salvar-per-usuario").click(function(){
        setPermissoesUsuario("#div-permissoes-usuario .container-permissions", true)
    });
    
    vmsisLib.contextMenu(function(){
       //alert($(this).parent()[0].getAttribute('data-module'));
       $('#treeViewApps .aplicarSubmenus').removeClass('aplicarSubmenus');
       $(this).parent().addClass('aplicarSubmenus');
       vmsisLib.popup.openPopup('aplicar_permissao_sub_menus');       
    }, 'controle_acesso_sub');
    
    $('#btn-replicar-permissao').click(aplicarConfiguracoesSubMenu);
    
    
})
