setTimeout(function() {
    $('#message').fadeOut('slow');
}, 3000);





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

//Funzione per ricaricare subito eventuali immagini senza dover ricaricare la pagina da un campo option
function handleImagePreviewOptionOld(selectId, previewImageId) {
  console.log("Funzione!")
  var selectField = $('#' + selectId);
  var previewImageElement = $('#' + previewImageId);

  selectField.change(function() {
    var selectedOption = $(this).find('option:selected');
    var imageUrl = selectedOption.data('symbol-image-url');
    console.log("Url: " + imageUrl)
    console.log("Funzione123!")
    if (imageUrl) {
      previewImageElement.attr('src', imageUrl);
    } else {
      // Se l'opzione selezionata non ha un'immagine associata, puoi impostare un'immagine di fallback o nascondere l'elemento dell'anteprima.
      // Ad esempio, puoi usare:
      // previewImageElement.attr('src', 'path/to/fallback-image.jpg');
      // o
      previewImageElement.hide();
    }
  });

  // Aggiungi il seguente codice per inizializzare l'anteprima all'avvio della pagina
  var selectedOption = selectField.find('option:selected');
  var imageUrl = selectedOption.data('symbol-image-url');

  if (imageUrl) {
    previewImageElement.attr('src', imageUrl);
  } else {
    // Se l'opzione selezionata inizialmente non ha un'immagine associata, puoi impostare un'immagine di fallback o nascondere l'elemento dell'anteprima.
    // Ad esempio, puoi usare:
    // previewImageElement.attr('src', 'path/to/fallback-image.jpg');
    // o
    previewImageElement.hide();
  }
};



// Questa funzione serve per passare l'url di un'immagine
// in modo che un eventuale campo immagine cambi istantaneamente al cambio della selezione di un campo option
// esempio d'uso:
// var symbolImageURL = "{% url 'chem_man:get_symbol_image_url' %}";
// $(document).ready(function() {
//	handleImagePreviewOption('id_fk_simbolo_ghs', 'preview-image', symbolImageURL);
// });

function handleImagePreviewOption_Old(selectId, previewImageId, symbolImageURL) {
  console.log("Funzione eccomi qui")
  var selectField = $('#' + selectId);
  var previewImageElement = $('#' + previewImageId);
  
  selectField.change(function() {
    console.log("Funzione eccomi qui")
    var selectedOptionValue = $(this).val();
    
    if (selectedOptionValue) {
      $.ajax({
        url: symbolImageURL,  // Inserisci l'URL dell'endpoint Django
        type: 'GET',
        data: { fk_simbolo_ghs_id: selectedOptionValue },
        success: function(response) {
          if (response.success && response.image_url) {
            previewImageElement.attr('src', response.image_url);
            previewImageElement.show();
          } else {
            previewImageElement.hide();
          }
        },
        error: function(xhr, textStatus, errorThrown) {
          console.log('Errore AJAX:', errorThrown);
        }
      });
    } else {
      previewImageElement.hide();
    }
  });
  
  // Inizializza l'anteprima all'avvio della pagina
  var initialOptionValue = selectField.val();
  if (initialOptionValue) {
    selectField.trigger('change');
  }
};


// Settare il focus su un campo predefinito
// definire l'ID del campo e richiamare la funzione 
// setFocusOnField('campo_predefinito');
function setFocusOnField(fieldId) {
  $(document).ready(function() {
      $("#" + fieldId).focus();
  });
};

function goBack() {
  window.history.back();
}