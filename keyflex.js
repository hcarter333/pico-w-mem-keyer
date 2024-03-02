var context = new AudioContext()
var o = null
var g = null
var keycmd = ""

document.addEventListener('DOMContentLoaded', function(){
  $(".js_play_sound").on("mousedown", function(e){
    e.preventDefault()
    var $target = $(e.target)
    eval($target.data("source"))
  })

  $(".js_play_sound").on("mouseup", function(e){
    e.preventDefault()
    o.stop()
    keyup()
  })

  $(".js_stop_sound").on("click", function(e){
    e.preventDefault()
    //o.stop()
    //keyup()
  })
}, false)

function example1(){
  context.resume()
  o = context.createOscillator()
  o.type = "sine"
  o.connect(context.destination)
  o.start()
  keydown()
}

function keydown(){
  keycmd = "http://192.168.4.1/light/on?msg=D"
  keysend()
}

function keyup(){
  keycmd = "http://192.168.4.1/light/on?msg=U"
  keysend()
}

function keysend(){
  if (typeof XMLHttpRequest != "undefined") {
    req = new XMLHttpRequest()
  } else if (window.ActiveXObject) {
    req = new ActiveXObject("Microsoft.XMLHTTP")
  }
  req.open("GET", keycmd, true)
  //req.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
        
  req.onreadystatechange = sk_cb
  req.send(null);

}

function sk_cb(){
    return
}
