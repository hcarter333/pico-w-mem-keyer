var context = new AudioContext()
var o = null
var g = null

document.addEventListener('DOMContentLoaded', function(){
  $(".js_play_sound").on("click", function(e){
    e.preventDefault()
    var $target = $(e.target)
    eval($target.data("source"))
  })

  $(".js_stop_sound").on("click", function(e){
    e.preventDefault()
    o.stop()
  })
}, false)

function example1(){
  o = context.createOscillator()
  o.type = "sine"
  o.connect(context.destination)
  o.start()
}