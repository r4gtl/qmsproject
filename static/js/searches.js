function searchFunctionGeneral(url, modalTitle, searchInputLabel, callerButtonId, event) {
  console.log("searchFunctionGeneral")
  
  console.log("callerButtonId iniziale: " + callerButtonId)
  $('#searchResults').data('callerButtonId', callerButtonId);
  $(document).ready(function() {
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
      $('#searchInput').val('');  // Pulisce il campo di ricerca
      $('#searchResults').empty(); // Pulisce i risultati della ricerca
    });

    // Pulisci i campi quando il modal viene aperto
    $('#searchModal').on('shown.bs.modal', function() {
      $('#searchInput').val('');  // Pulisce il campo di ricerca
      $('#searchResults').empty(); // Pulisce i risultati della ricerca
      $('#searchInput').focus();

      // Imposta il titolo del modal e l'etichetta del campo di ricerca
      $('#searchModalLabel').text(modalTitle);
      $('#searchInputLabel').text(searchInputLabel);
    });
    
    
  });


 
  
}

$('#searchResults').on('click', 'tr', function() {
  var callerButtonId = $('#searchResults').data('callerButtonId');
  console.log("callerButtonID: " + callerButtonId)
  // Esegui azioni aggiuntive in base all'ID del pulsante chiamante
  if (callerButtonId === 'openSearchArticleButton') {
    console.log("Cliccato")
    // Azioni specifiche per il pulsante chiamante openSearchArticleButton
  } else {
    // Azioni di default
  }
  
});

