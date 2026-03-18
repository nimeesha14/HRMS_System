document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        const alerts = document.querySelectorAll(".alert");
        alerts.forEach(alert => {
            alert.classList.remove("show");
            setTimeout(() => alert.remove(), 300);
        });
    }, 1000);
});