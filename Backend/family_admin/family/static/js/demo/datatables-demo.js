// Call the dataTables jQuery plugin

$(document).ready(function() {
  $('#dataTable').DataTable( {
      "language": {
          "lengthMenu": "Mostrar _MENU_ entradas",
          "zeroRecords": "No se ha encontrado nada - :c",
          "info": "Mostrar página _PAGE_ de _PAGES_",
          "infoEmpty": "No encontrado",
          "infoFiltered": "(filtrado de _MAX_ en total)",
          "search": "Buscar:",
          "paginate": {
              "previous":   "Anterior",
              "next":       "Siguiente",
          },

      }
  } );
} );

 $(document).ready(function() {
     // messages timeout for 10 sec 
     setTimeout(function() {
         $('.message').fadeOut('slow');
     }, 3000); // <-- time in milliseconds, 1000 =  1 sec

//     // delete message
     $('.del-msg').live('click',function(){
         $('.del-msg').parent().attr('style', 'display:none;');
     })
 });

//anadir dinamicamente inputs de videos
function addImages(){
    var count_image = 1;
    $('#addimg').click(function(){
        var div_image = $('#image');
        if(count_image<4){
            var add = '<label class="col-md-3 col-form-label" for="imagen1"><strong> Seleccione la imagen </strong></label>';
            add+='<div class="col-md-4">';
            add+='<input id="image-input" type="file" name="images[]" accept="image/*" required="">';
            add+='</div>';
            add+='<div class="col-md-5 text-right"></div>';
            div_image.append(add);
            count_image++;
        }
    });
}

//anadir dinamicamente inputs de imagenes
function addVideo(){
    var count_video = 1;
    $('#addvideo').click(function(){
        var div_video    = $('#video');
        if(count_video<4){
            var add = '<label class="col-md-3 col-form-label" for="imagen1"><strong> Seleccione video </strong></label>';
            add+='<div class="col-md-4">';
            add+='<input id="video-input" type="file" name="videos[]" accept="image/*" required="">';
            add+='</div>';
            add+='<div class="col-md-5 text-right"></div>';
            div_video.append(add);
            count_video++;
        }
    });
}

function setCsrf(){
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val()
        }
    });
}

//funcion para cargar imagenes
function postImages(){
    $('#postimages').click(function(e){
        e.preventDefault();
        //Crear arreglo con imagenes
        var form_data = new FormData();
        $("input[name*='images']").each(function(){
            var file = $(this)[0].files[0];
            form_data.append(file.name,file)
        });
        /*for (var pair of form_data.entries()) {
            console.log(pair[0]+ ', ' + pair[1]); 
        }*/
        setCsrf();
        //Enviar ajax con arreglo de imagenes
        $.ajax({
            type : 'POST',
            url : 'http://127.0.0.1:8000/recibir_imagenes',
            data :  form_data,
            processData: false,
            contentType: false, 
         
            success : function(json) {
                console.log(json)
            },
         
            error : function(jqXHR, status, error) {
                console.log(jqXHR,status,error)
            },
        });
        return false;
    });
}

//funcion para cargar videos
function postVideos(){
    $('#postvideos').click(function(e){
        e.preventDefault();
        
    });
}

$( document ).ready(function() {
    //Llamada funciones
    addImages();
    addVideo();
    postVideos();
    postImages();
});