function startVoice() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.lang = "en-IN";
    recognition.start();

    recognition.onresult = function(event) {
        let command = event.results[0][0].transcript;
        document.getElementById("spoken").innerText = command;

        fetch("/process", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({command: command})
        })
        .then(res => res.json())
        .then(data => alert(data.message));
    };

    recognition.onerror = function(event) {
        alert("Voice error: " + event.error);
    };
}
