
// Funzione per la ricerca generica:
// Indicare le variabili nella chiamata dall'evento click del pulsante
// Esempio d'uso:
// il pulsante deve essere così
/*
<button type="button" 
      class="btn btn-info mt-3" 
      id="openSearchArticleButton"
      data-bs-toggle="modal" 
      data-bs-target="#searchModal"
      data-url="{% url 'core:search_articolo' %}" 
      data-modal-title="Cerca Articolo" 
      data-search-input-label="Cerca Articoli"
      ><i class="bi bi-search"></i></button>
  </div>
*/    
// La gestione dell'evento click del pulsante deve essere così
/*
$(document).ready(function() {
  $('#openSearchArticleButton').click(function(event) {
    var callerButtonId = $(this).attr('id');
    var url = $(this).data('url');
    var modalTitle = $(this).data('modal-title');
    var searchInputLabel = $(this).data('search-input-label');
    searchFunctionGeneral(url, modalTitle, searchInputLabel, callerButtonId, event);
  });
});
*/
// Questo chiamerà e gestirà il modal baseModalGenericSearch.html che va ovviamente incluso nel template
// {% include "core/modals/baseModalGenericSearch.html" %}


function searchFunctionGeneral(url, modalTitle, searchInputLabel, callerButtonId, event) {
  
  var callerButton = $('#' + callerButtonId);
  var setFocusValue = callerButton.data('setfocus');

  $('#searchResults').data('callerButtonId', callerButtonId);
  $('#searchResults').data('setFocusValue', setFocusValue); // Assegno il valore di setfocus in modo da impostare il focus su un controllo dopo la scelta
  

    $("#searchInput").on("input", function() {
      
      var searchTerm = $(this).val().trim();
      if (searchTerm.length >= 1) {
        $.ajax({
          url: url,
          method: "GET",
          data: { search: searchTerm },
          dataType: 'json',
          success: function(data) {
            var resultsContainer = $("#searchResults");
            resultsContainer.empty(); // Pulisce eventuali risultati precedenti

            // Aggiunge i nuovi risultati al DOM
            if (data && data.html) {
              resultsContainer.html(data.html);
              console.log("data: " + data.html)
            } else {
              resultsContainer.append("<p>Nessun risultato trovato.</p>");
            }
          },
          error: function(xhr, errmsg, err) {
            console.log(errmsg);
            // Gestisci eventuali errori qui
          }
        });
      } else {
        $("#searchResults").empty(); // Pulisce i risultati se la stringa di ricerca è troppo corta
      }
    });

    $('#searchModal').on('hide.bs.modal', function() {
      console.log("Modal chiuso")
      $('#searchInput').val('');  // Pulisce il campo di ricerca
      $('#searchResults').empty(); // Pulisce i risultati della ricerca
      $('#searchModal').removeData();
    });

    // Pulisci i campi quando il modal viene aperto
    $('#searchModal').on('shown.bs.modal', function() {
      $('#searchInput').val('');  // Pulisce il campo di ricerca
      $('#searchResults').empty(); // Pulisce i risultati della ricerca
      $('#searchInput').focus();

      $.ajaxSetup({ cache: false }); // Pulisce la cache

      // Imposta il titolo del modal e l'etichetta del campo di ricerca
      $('#searchModalLabel').text(modalTitle);
      $('#searchInputLabel').text(searchInputLabel);
    });
    
    
 


 
  
}

$('#searchResults').on('click', 'tr', function() {
  var callerButtonId = $('#searchResults').data('callerButtonId');
  var setFocusValue = $('#searchResults').data('setFocusValue');
  console.log("setFocusValue: " + setFocusValue)
  
  switch (callerButtonId) {
    // Valuta il caso in cui si stia cercando un articolo
    case 'openSearchArticleButton':
      var id_fk_articolo = $(this).find('.articolo-id').text();    
      $('#id_fk_articolo').val(id_fk_articolo);    
      $('#searchModal').modal('hide');
      break;
    
      // Valuta il caso in cui si stia cercando un colore
    case 'openSearchColorButton':
      var id_fk_colore = $(this).find('.colore-id').text();    
      $('#id_fk_colore').val(id_fk_colore);    
      $('#searchModal').modal('hide');
      break;
      
    case 'openSearchChemicalButton':
        var id_fk_prodotto_chimico = $(this).find('.prodotto-id').text();    
        $('#id_fk_prodotto_chimico').val(id_fk_prodotto_chimico);    
        $('#searchModal').modal('hide');
        

      break;

      // Valuta il caso in cui si stia cercando una revisione da accodare alla Ricetta di Rifinizione
    case 'openSearchRevisionButton':
      var conferma = confirm("Sei sicuro di voler accodare questa ricetta?");
  
      if (conferma) {
        // Ottiene l'id del prodotto chimico dalla riga cliccata
        var ricettaId = $(this).find('.ricetta-id').text();
        var ricettaAttiva = $('#openSearchRevisionButton').data('ricettaAttiva'); // Passa l'id della ricetta attiva alla quale accodare. Dato passato nel button
                
        // Chiude il modal
        $('#searchModal').modal('hide');
        // recupera il CSRF-Token dal form
        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
        
        // Invia una richiesta AJAX per aggiungere i record DettaglioRicettaRifinizione
        $.ajax({
            url: "/ricette/accoda_dettaglio_ricetta_rifinizione/",  
            method: "POST",
            data: {
                ricetta_id: ricettaId,
                ricettaAttiva: ricettaAttiva,
                csrfmiddlewaretoken: csrftoken
            },
            dataType: 'json',
            success: function(data) {
              if (data.redirect_url) {
                window.location.href = data.redirect_url;
              } else {
                  console.error('Errore durante il reindirizzamento:', data.error);
              }
              
            },
            error: function(xhr, errmsg, err) {
                console.log(errmsg);
                
            }
        });
      }
      break;
      
        // Valuta il caso in cui si stia cercando una revisione da accodare alla Ricetta di Rifinizione
    case 'openSearchColorRevisionButton':
      var conferma = confirm("Sei sicuro di voler accodare questa ricetta?");
  
      if (conferma) {
        // Ottiene l'id del prodotto chimico dalla riga cliccata
        var ricettaId = $(this).find('.ricetta-id').text();
        var ricettaAttiva = $('#openSearchColorRevisionButton').data('ricettaAttiva'); // Passa l'id della ricetta attiva alla quale accodare. Dato passato nel button
                
        // Chiude il modal
        $('#searchModal').modal('hide');
        // recupera il CSRF-Token dal form
        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
        
        // Invia una richiesta AJAX per aggiungere i record DettaglioRicettaRifinizione
        $.ajax({
            url: "/ricette/accoda_dettaglio_ricetta_colore_rifinizione/",  
            method: "POST",
            data: {
                ricetta_id: ricettaId,
                ricettaAttiva: ricettaAttiva,
                csrfmiddlewaretoken: csrftoken
            },
            dataType: 'json',
            success: function(data) {
              if (data.redirect_url) {
                window.location.href = data.redirect_url;
              } else {
                  console.error('Errore durante il reindirizzamento:', data.error);
              }
              
            },
            error: function(xhr, errmsg, err) {
                console.log(errmsg);
                
            }
        });
      }
      break;

      

    default:
      // Azioni di default
      break;
      
  }

  if (typeof setFocusValue !== 'undefined') {
    setFocus=$('#' + setFocusValue);
    setTimeout(function() {
      setFocus.focus(); // Imposta il focus sul campo indicato
  }, 500);
  }
  
  
  
});


// PULSANTI DI RICERCA STANDARD 

// Intercetto l'evento relativo al pulsante per cercare i prodotti chimici
$(document).ready(function() {
  $('#openSearchChemicalButton').click(function(event) {    
    var callerButtonId = $(this).attr('id');
    var url = $(this).data('url');
    var modalTitle = $(this).data('modal-title');
    var searchInputLabel = $(this).data('search-input-label');
    searchFunctionGeneral(url, modalTitle, searchInputLabel, callerButtonId, event);
  });
});



// Intercetto l'evento relativo al pulsante per cercare le revisioni ricette rifinizione
$(document).ready(function() {
  $('#openSearchRevisionButton').click(function(event) {    
    var callerButtonId = $(this).attr('id');
    var url = $(this).data('url');
    var modalTitle = $(this).data('modal-title');
    var searchInputLabel = $(this).data('search-input-label');
    searchFunctionGeneral(url, modalTitle, searchInputLabel, callerButtonId, event);
  });

});


// Intercetto l'evento relativo al pulsante per cercare le revisioni dei colori rifinizione
$(document).ready(function() {
  $('#openSearchColorRevisionButton').click(function(event) {    
    var callerButtonId = $(this).attr('id');
    var url = $(this).data('url');
    var modalTitle = $(this).data('modal-title');
    var searchInputLabel = $(this).data('search-input-label');
    searchFunctionGeneral(url, modalTitle, searchInputLabel, callerButtonId, event);
  });

});

// Intercetto l'evento relativo al pulsante per cercare gli articoli
$(document).ready(function() {
  $('#openSearchArticleButton').click(function(event) {    
    var callerButtonId = $(this).attr('id');
    var url = $(this).data('url');
    var modalTitle = $(this).data('modal-title');
    var searchInputLabel = $(this).data('search-input-label');
    searchFunctionGeneral(url, modalTitle, searchInputLabel, callerButtonId, event);
  });
});

// Intercetto l'evento relativo al pulsante per cercare i colori
$(document).ready(function() {
  $('#openSearchColorButton').click(function(event) {    
    var callerButtonId = $(this).attr('id');
    var url = $(this).data('url');
    var modalTitle = $(this).data('modal-title');
    var searchInputLabel = $(this).data('search-input-label');
    searchFunctionGeneral(url, modalTitle, searchInputLabel, callerButtonId, event);
  });
});




