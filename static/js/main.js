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
  console.log('Setting focus on: ' + fieldId);
  $(document).ready(function() {
      $("#" + fieldId).focus();
  });
};


// Chiudere un modal e settare il focus su un campo
// DELLO STESSO TEMPLATE
// vedi l'uso di esempio nel template sostanza_sds.html della app chem_man
function closeModalAndSetFocus(modalId, elementId) {
  $(modalId).modal('hide');

  $(modalId).on('hidden.bs.modal', function () {
    console.log('Modal closed');
    setTimeout(function() {
      $('#' + elementId).focus();
    }, 100);
    
  });
}




// Per gestire il pulsante Annulla
function goBack() {
  window.history.back();
};

// Prova in sostituzione della funzione precedente
function cancelAndRedirectTo(url) {
  window.location.href = url;
}

// Inizializzare le tabelle di DataTable con le labels in Italiano
// Si usa con initializeDataTable('id_tabella');
function initializeDataTable(tableId) {
  $(document).ready(function() {
      $(`#${tableId}`).DataTable({
          "pageLength": 50,
          "language": {
              "sProcessing": "Elaborazione in corso...",
              "sLengthMenu": "Mostra _MENU_ voci",
              "sZeroRecords": "Nessun risultato trovato",
              "sEmptyTable": "Nessun dato disponibile",
              "sInfo": "Voci da _START_ a _END_ di _TOTAL_ voci",
              "sInfoEmpty": "Voci da 0 a 0 di 0 voci",
              "sInfoFiltered": "(filtrato da _MAX_ voci totali)",
              "sInfoPostFix": "",
              "sSearch": "Cerca:",
              
              "sUrl": "",
              "oPaginate": {
                  "sFirst": "Prima",
                  "sPrevious": "Precedente",
                  "sNext": "Successiva",
                  "sLast": "Ultima"
              }
          }
      });
  });
}




// Le prossime funzioni servono per switchare le righe di una tabella in alto o in basso
// Esempio di uso: due pulsanti, uno per spostare in su e uno in giù
// <button type="button" class="btn btn-sm btn-outline-primary ms-1" 
// data-bs-toggle="tooltip" data-bs-placement="top"
// data-bs-custom-class="custom-tooltip"
// data-bs-title="Sposta la riga in alto"
// id="btnUp"
// onclick="updateNumeroRigaServer('articoli','DettaglioProcedura', '{{ dettaglio.pk }}', 1, 'down', '{% url 'core:update_numero_riga_down' %}')"
// >
// <i class="bi bi-arrow-bar-up"></i>
// </button>
// <button type="button" class="btn btn-sm btn-outline-primary ms-1" 
// data-bs-toggle="tooltip" data-bs-placement="top"
// data-bs-custom-class="custom-tooltip"
// data-bs-title="Sposta la riga in basso"
// id="btnDown"
// onclick="updateNumeroRigaServer('articoli','DettaglioProcedura', '{{ dettaglio.pk }}', 1, 'up', '{% url 'core:update_numero_riga_up' %}')"
// >
// <i class="bi bi-arrow-bar-down"></i>
// </button>
// </td>
// Sull'evento onclick va richiamato il nome dell'app, il nome del modello, il pk della riga, lo step, l'azione e l'url
// Funzione per eseguire l'aggiornamento lato server
function updateNumeroRigaServer(appLabel, model, dettaglioId, nuovoNumeroRiga, action, url) {
  $.ajax({
      //url: action === 'up' ? '{% url "core:update_numero_riga_up" %}' : '{% url "core:update_numero_riga_down" %}',
      url: url,
      method: 'POST',
      data: {
          model: model,
          app_label: appLabel,
          dettaglio_id: dettaglioId,
          increment: action === 'up' ? 1 : -1,
          action: action,
          csrfmiddlewaretoken: '{{ csrf_token }}'
      },
      success: function (data) {
          if (data.success) {
              // Esegui la funzione di callback per l'aggiornamento lato client
              updateNumeroRigaCallback(dettaglioId, data.numero_riga);
          } else {
              alert(data.error);
          }
      },
      error: function (xhr, textStatus, errorThrown) {
          console.error('Errore durante la richiesta Ajax:', errorThrown);
      }
  });
}

function updateNumeroRigaCallback(dettaglioId, nuovoNumeroRiga) {
  var numeroRigaElement = document.getElementById('numero-riga-' + dettaglioId);
  if (numeroRigaElement) {
      updateTableWithNewNumberRiga(nuovoNumeroRiga);
      numeroRigaElement.textContent = nuovoNumeroRiga;
      location.reload();
      console.log("Nuovo numero riga: " + nuovoNumeroRiga)
      // Cerca la riga con il nuovo numero_riga e aggiorna la tabella
      //updateTableWithNewNumberRiga(nuovoNumeroRiga);
  } else {
      console.error('Elemento non trovato con ID:', 'numero-riga-' + dettaglioId);
  }
}

function updateTableWithNewNumberRiga(newNumeroRiga) {
  // Trova la tabella
  var tableBody = document.getElementById('table-body');

  // Cerca la riga con il numero_riga desiderato
  var rows = tableBody.getElementsByTagName('tr');
  for (var i = 0; i < rows.length; i++) {
      var currentRow = rows[i];
      var numeroRigaElement = currentRow.querySelector('.numero-riga');
      if (numeroRigaElement && parseInt(numeroRigaElement.textContent) === newNumeroRiga) {
          // Aggiorna solo questa riga
          // Puoi anche chiamare una funzione per aggiornare solo questa riga, se necessario
          var updatedRowElement = '<td class="numero-riga" id="numero-riga-' + currentRow.id.split('-')[2] + '"><a href="#">' + (newNumeroRiga - 1) + '</a></td>';
          updatedRowElement += '<td>' + currentRow.querySelector('td:nth-child(2)').textContent + '</td>';
          updatedRowElement += '<td class="text-center">' + currentRow.querySelector('td:nth-child(3)').innerHTML + '</td>';
          currentRow.innerHTML = updatedRowElement;
          break;  // Esci dal ciclo dopo l'aggiornamento
      }
  }
}

