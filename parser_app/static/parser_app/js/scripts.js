document.getElementById("parse-form").addEventListener("submit", function (e) {
    e.preventDefault(); // Остановить стандартное действие формы

    const form = e.target;
    const formData = new FormData(form);

    fetch(form.action, {
        method: "POST",
        headers: {
            "X-CSRFToken": form.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            const responseDiv = document.getElementById("response");
            if (data.success) {
                responseDiv.innerHTML = `<span style="color: green;">${data.message}</span>`;
            } else {
                responseDiv.innerHTML = `<span style="color: red;">${data.error}</span>`;
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            document.getElementById("response").innerHTML = `<span style="color: red;">Error occurred!</span>`;
        });
});
