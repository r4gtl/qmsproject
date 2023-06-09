setTimeout(function() {
    $('#message').fadeOut('slow');
}, 3000);

function getRandomColor() { //generates random colours and puts them in string
    console.log("Arrivato");
    var colors = [];
    for (var i = 0; i < 3; i++) {
      var letters = '0123456789ABCDEF'.split('');
      var color = '#';
      for (var x = 0; x < 6; x++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      colors.push(color);
    }
    return colors;
  }



