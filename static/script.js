
function searchDriver() {

    // Show loading spinner
    document.getElementById("loadingSpinner").style.display = "block";

    var driverId = (document.getElementById("driverId").value);
    console.log("Driver ID:", driverId);

    // Use AJAX to send a request to the server
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        console.log("ReadyState:", this.readyState, "Status:", this.status);
        if (this.readyState == 4) {
            // Hide loading spinner regardless of success or failure
            document.getElementById("loadingSpinner").style.display = "none";

            if (this.status == 200) {
                console.log("Response:", this.responseText);
                var resultTable = document.getElementById("resultTable");
                resultTable.innerHTML = this.responseText;
            } else {
                console.error("Error:", this.statusText);
            }
        }
    };

    xhr.open("GET", "/search?driverId=" + driverId, true);
    xhr.send();
}


function insertData() {
    var driverId = document.getElementById("insertDriverId").value;
    var reason = document.getElementById("insertFeature").value;
    var city = document.getElementById("insertCity").value;
    var serviceType = document.getElementById("insertServiceType").value;

    // Check if essential fields are not empty
    if (!driverId || !reason || !city || !serviceType) {
        alert("Please fill in all required fields.");
        return;
    }
    
    // Use AJAX to send a request to the server
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log("Response:", this.responseText);
            // Optionally, you can update the UI or provide user feedback here
        }
    };

    xhr.open("POST", "/insert_data", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    // Send data as JSON in the request body
    xhr.send(JSON.stringify({
        driverId: driverId,
        reason: reason,
        city: city,
        serviceType: serviceType
    }));
}


