
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on( 'connect', function() {
  socket.emit( 'message', {
    data: 'User Connected'
  })
  var form = $( 'form' ).on( 'submit', function( e ) {
    e.preventDefault()
    let user_name = "{{ username }}"
    let user_input = $( 'input.message' ).val()
    let room_input = $( 'input.room' ).val()
    socket.emit( 'message', {
      user_name : user_name,
      message : user_input,
      room: room_input
    })
    $( 'input.message' ).val( '' ).focus()
  })
})
socket.on( 'response', function( msg ) {
  console.log( msg )
  if( typeof msg.user_name !== 'undefined' ) {
    $( 'h3' ).remove()
    $( 'div.message' )
        .append('<div><b style="color: #000">'+msg.user_name+': </b>'+msg.message+'</div>' )
  }
})