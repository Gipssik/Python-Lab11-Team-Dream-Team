function onlyPlayOneIn(container) {
    container.addEventListener("play", function (event) {
        audio_elements = [...container.getElementsByTagName("audio")]
        for (i = 0; i < audio_elements.length; i++) {
            audio_element = audio_elements[i];
            if (audio_element !== event.target) {
                audio_element.pause();
                audio_element.currentTime = 0;
            }
        }
        event.target.addEventListener('ended', function () {
            let index = audio_elements.indexOf(event.target);
            console.log(index);
            if (index === -1) {
                console.log("none of music");
                return;
            }
            else if (index === audio_elements.length - 1) {
                audio_elements[0].play();
                return;
            }
            else {
                audio_elements[index + 1].play();
            }
        });
    }, true);
}
const music = document.querySelectorAll("audio");
music.forEach(elem => elem.addEventListener('ended', playNextSong));
document.addEventListener("DOMContentLoaded", function () {
    onlyPlayOneIn(document.body);
});
