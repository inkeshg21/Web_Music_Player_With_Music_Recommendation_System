// function audioPlay() {
//     /*var player = document.getElementById("player2");*/
//   var player = document.getElementById("player");
//   //alert(player);
//     player.play();
//     initProgressBar();
//     isPlaying = true;
// }

var player = document.getElementById("player")
var btn = document.getElementById("play-btn")
var playState = true
if (playState) {
    player.play()
    playState = !playState
    btn.innerHTML = "<i class='fa-solid fa-pause text-dark'></i>"
}
function audioPlay() {
    if (playState) {
        player.play()
        console.log(player.play())
        playState = !playState
    } else {
        player.pause()
        playState = !playState
    }
    if (playState) {
        btn.innerHTML = "<i class='fa-solid fa-play text-dark'></i>"
    } else {
        btn.innerHTML = "<i class='fa-solid fa-pause text-dark'></i>"
    }
}
