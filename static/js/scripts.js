// static/js/scripts.js

function sendRequest(type, value) {
    const resultsOutput = document.getElementById('results-output');
    resultsOutput.textContent = 'Loading...';

    fetch('/lookup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ type: type, value: value })
    })
    .then(response => response.json())
    .then(data => {
        resultsOutput.textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        resultsOutput.textContent = 'Error: Could not retrieve data.';
        console.error('Error:', error);
    });
}

function lookupMyIPs() {
    sendRequest('my_ips', '');
}

function lookupSingleIp() {
    const ip = document.getElementById('singleIpInput').value;
    if (ip) {
        sendRequest('single_ip', ip);
    } else {
        alert("Please enter an IP address.");
    }
}

function lookupPhoneNumber() {
    const number = document.getElementById('phoneInput').value;
    if (number) {
        sendRequest('phone_number', number);
    } else {
        alert("Please enter a phone number.");
    }
}