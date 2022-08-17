document.querySelectorAll(".btn-dl").forEach(function(btn) {
    btn.addEventListener("click", function() {
        btn.innerText = "Downloading...";
    });
});