setTimeout(function() {
    $('#message').fadeOut('slow');
}, 3000);



// $(document).ready(function() {
//   $('.datepicker').datepicker({
//       format: 'dd-mm-yyyy',
//       autoclose: true,
//       todayHighlight: true
//   });
// });


function getRandomColor() { //generates random colours and puts them in string    
    var colors = [];
    for (var i = 0; i < 50; i++) {
      var letters = '0123456789ABCDEF'.split('');
      var color = '#';
      for (var x = 0; x < 6; x++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      colors.push(color);
    }
    return colors;
  };

//Funzione per ricaricare subito eventuali immagini senza dover ricaricare la pagina
function handleImagePreview(imageUploadId, previewImageId) {
  var imageUploadField = $('#' + imageUploadId);
  var previewImageElement = $('#' + previewImageId);  
  imageUploadField.change(function() {
    var input = this;
    var url = URL.createObjectURL(input.files[0]);
    previewImageElement.attr('src', url);
  });
};


