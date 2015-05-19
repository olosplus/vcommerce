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

function postForm(idForm, url, url_redirect){
  var form = $("#" + idForm);
  var csrftoken = getCookie('csrftoken');
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

      var parser = new DOMParser()
      var doc_received = parser.parseFromString(data, "text/html");
      var frm_received = doc_received.getElementById(idForm);
      var frm = document.getElementById(idForm);
      if (frm_received.innerHTML === "") {
        if (url_redirect != ""){
            window.location.href = url_redirect;
        }
      } else {
        frm.innerHTML = frm_received.innerHTML;       
      };
    },
    error: function (data) {
      alert(data.responseText);
    }
  });
  return false;    
}


$(document).ready(function(){
  $("#UnidadeSelecionada").change(function(){
    var unidade = $(this).val()
    $.ajax({
        url: 'mudarunidade/',
        type: 'get',
        data: {"unidade" : unidade},
        success: function (data) {
          if (data == 'error')
            alert('Ocorreu um erro.');
        },
        failure: function (data) {
          alert('Ocorreu um erro.');
        }
    })         	
  });

  var unidade_selecionada = $("#UnidadeEscolhida").val();
  if(unidade_selecionada != undefined)
    $("#UnidadeSelecionada").val(unidade_selecionada);

});