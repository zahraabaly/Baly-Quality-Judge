
function searchDriver() {
    var driverId = (document.getElementById("driverId").value);
    console.log("Driver ID:", driverId);

    // Use AJAX to send a request to the server
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        console.log("ReadyState:", this.readyState, "Status:", this.status);
        if (this.readyState == 4 && this.status == 200) {
            console.log("Response:", this.responseText);
            var resultTable = document.getElementById("resultTable");
            resultTable.innerHTML = this.responseText;
        }
    };

    xhr.open("GET", "/search?driverId=" + driverId, true);
    xhr.send();
}
