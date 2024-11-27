// Function to validate login credentials
function validateLogin() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === 'surya' && password === 'surya') {
        // Hide the login form and show admin panel
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('admin-panel').style.display = 'block';
        return false; // Prevent form submission
    } else {
        alert('Invalid login or password. Try again.');
        return false; // Prevent form submission
    }
}

// Function to handle "Send Alert"
function sendAlert() {
    alert('Alert has been sent successfully!');
}

// Function to handle "View Box Numbers"
function viewBoxNumbers() {
    alert('Displaying box numbers...');
}
