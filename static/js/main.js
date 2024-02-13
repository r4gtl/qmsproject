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


// DRAG & DROP RIGHE TABELLE //
/*
Funzione per rendere le righe della tabella trascinabili
Inserire la chiamata 
document.addEventListener('DOMContentLoaded', function() {

const table = document.getElementById('myTable');
makeTableRowsDraggable(table);
});
 
inserire per ogni riga della tabella il tag
<tr data-pk="{{ dettaglio.pk }}">
dove {{ dettaglio.pk }} indica la pk di quella riga.
Per chiamare poi la funzione che aggiorna il backend:

definire come costante l'url che punta alla funzione che gestisce
la chiamata ajax del backend
const searchURL = "{% url 'ricette:update_row_numbers' %}";


definire come deve essere il link da assegnare ad ogni riga per modificare il dettaglio
const linkTemplate = "/ricette/modifica_dettaglio_ricetta_rifinizione/{pk}/";

chiamare la funzione con le variabili
updateRowNumbers(table, searchURL, linkTemplate);

*/



function makeTableRowsDraggable(table) {
  const rows = table.querySelectorAll('tbody tr');

  rows.forEach(row => {
    row.draggable = true;
    row.classList.add('draggable');

    // Aggiungi event listener per il trascinamento
    row.addEventListener('dragstart', () => {
      row.classList.add('dragging');
    });

    row.addEventListener('dragend', () => {
      row.classList.remove('dragging');
      updateRowNumbers(table);
    });
  });

  // Aggiungi event listener per il trascinamento
  table.addEventListener('dragover', (event) => {
    event.preventDefault();
    const afterElement = getDragAfterElement(table, event.clientY);
    const draggingElement = table.querySelector('.dragging');
    if (afterElement == null) {
      table.querySelector('tbody').appendChild(draggingElement);
    } else {
      table.querySelector('tbody').insertBefore(draggingElement, afterElement);
    }
  });
}

// Funzione per trovare l'elemento dopo cui deve essere inserito il trascinamento
function getDragAfterElement(table, y) {
  const draggableElements = [...table.querySelectorAll('.draggable:not(.dragging)')];
  return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect();
    const offset = y - box.top - box.height / 2;
    if (offset < 0 && offset > closest.offset) {
      return { offset: offset, element: child };
    } else {
      return closest;
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element;
}


  function updateRowNumbers(table) {
    const rows = table.querySelectorAll('tbody tr');
    const newNumbers = [];
  
    rows.forEach((row, index) => {
      const rowNumberCell = row.querySelector('td:first-child');
      rowNumberCell.textContent = index + 1;
      newNumbers.push({ pk: row.dataset.pk, numero_riga: index + 1 });
    });
    
  
    // Esegui una chiamata AJAX per inviare i nuovi numeri di riga al backend
    fetch(searchURL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',        
        'X-CSRFToken': getCookie('csrftoken') // Assicurati di includere il CSRF token
      },
      
      body: JSON.stringify({ data: newNumbers.map((item, index) => ({ pk: item.pk, numero_riga: index + 1 })) })
  
    })  
    .then(response => {
          if (!response.ok) {
              throw new Error('Errore durante l\'aggiornamento dei numeri di riga');
          }
          return response.json();
      })
      .then(data => {
          console.log('Nuovi numeri di riga inviati con successo al backend:', data);
          updateLinksWithNewData(table, newNumbers, linkTemplate); // Chiamata alla funzione per aggiornare i link
      })
      .catch(error => {
          console.error('Errore:', error);
      });
  }
  
  //13/02/2024 - ELIMINABILE
  /*function updateLinksWithNewData(table, newNumbers) {
      const rows = table.querySelectorAll('tbody tr');
      rows.forEach((row, index) => {
          const rowNumberCell = row.querySelector('td:first-child');
          const pk = newNumbers[index].pk;
          const numero_riga = newNumbers[index].numero_riga;
          const url = `/ricette/modifica_dettaglio_ricetta_rifinizione/{ricettarifinizione.pk}/${pk}/`;
          rowNumberCell.innerHTML = `<a href="${url}" id="numero_riga_${pk}">${numero_riga}</a>`;
      });
  }*/
  
  function updateLinksWithNewData(table, newNumbers, linkTemplate) {
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach((row, index) => {
      const rowNumberCell = row.querySelector('td:first-child');
      const pk = newNumbers[index].pk;
      const numero_riga = newNumbers[index].numero_riga;
      const url = linkTemplate.replace('{pk}', pk);
      rowNumberCell.innerHTML = `<a href="${url}" id="numero_riga_${pk}">${numero_riga}</a>`;
    });
  }
  
  
  // Funzione per ottenere il valore del CSRF token
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
  
    