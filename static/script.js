console.log("JavaScript connected successfully!");

// Find the search input
const searchInput = document.getElementById("historySearch");

// Find all history table rows
const historyRows = document.querySelectorAll(
    ".history-table tbody tr"
);

// Listen for user input
searchInput.addEventListener("input", function () {

    // Get the text entered by the user
    const searchTerm = searchInput.value.toLowerCase().trim();

    // Check every history row
    historyRows.forEach(function (row) {

        const rowText = row.textContent.toLowerCase();

        // Show matching rows and hide non-matching rows
        if (rowText.includes(searchTerm)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }

    });

});
// ===== IP RESULT NOTIFICATIONS =====

const resultMessage = document.getElementById("resultMessage");

if (resultMessage) {

    const message = resultMessage.textContent;

    if (message.includes("valid IP address")) {
        resultMessage.classList.add("success-message");
    }
    else if (message.includes("Invalid IP format")) {
        resultMessage.classList.add("error-message");
    }

}