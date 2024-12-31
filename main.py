from flask import Flask, render_template_string, request, redirect, url_for, flash, session
import os
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For flash messages and session handling
USER_DATA_FILE = 'users.txt'

# Function to load users from the file
def load_users():
    users = {}
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    parts = line.strip().split(',')
                    if len(parts) == 4:  # Now expecting 4 parts (username, password, user_number, ip_address)
                        username, password, user_number, ip_address = parts
                        users[username] = (password, user_number, ip_address)
                    else:
                        print(f"Invalid user line: {line.strip()}")  # Debugging line
    return users

# Function to save a new user to the file
def save_user(username, password, user_number, ip_address):
    with open(USER_DATA_FILE, 'a') as file:
        file.write(f"{username},{password},{user_number},{ip_address}\n")

# Function to generate a unique 10-digit number
def generate_unique_number():
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        # Check if the username already exists
        if username in users:
            flash('Username already exists. Please log in.')
            return redirect(url_for('login'))

        # Generate a unique 10-digit number for the new user
        user_number = generate_unique_number()

        # Capture the user's IP address
        user_ip = request.remote_addr

        # Save the new user with their number and IP address
        save_user(username, password, user_number, user_ip)
        flash('Account successfully created. Please log in.')
        return redirect(url_for('login'))

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Register</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #f3c623, #6a0dad);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    overflow: hidden;
                    color: #fff;
                }
                .container {
                    background: rgba(255, 255, 255, 0.15);
                    border-radius: 20px;
                    padding: 40px;
                    width: 100%;
                    max-width: 400px;
                    text-align: center;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
                }
                h2 {
                    margin-bottom: 20px;
                    color: #f3c623;
                    font-size: 2rem;
                    font-weight: 700;
                }
                input[type="text"], input[type="password"] {
                    width: 100%;
                    padding: 12px;
                    margin: 10px 0;
                    border: 2px solid #6a0dad;
                    border-radius: 8px;
                    outline: none;
                    font-size: 1rem;
                    background-color: #fff;
                    color: #333;
                }
                button {
                    width: 100%;
                    padding: 14px;
                    background-color: #6a0dad;
                    color: #fff;
                    border: none;
                    border-radius: 8px;
                    font-size: 1.1rem;
                    cursor: pointer;
                }
                .footer {
                    margin-top: 20px;
                    color: #f3c623;
                    font-size: 0.9rem;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Create Your Account</h2>
                <form method="post">
                    <input type="text" name="username" placeholder="Enter your name" required><br>
                    <input type="password" name="password" placeholder="Enter your password" required><br>
                    <button type="submit">Create Account</button>
                </form>
                <div class="footer">
                    <p>Already have an account? <a href="/login" style="color: #fff;">Login here</a></p>
                </div>
            </div>
        </body>
        </html>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        # Check if the user exists and the password matches
        if username in users and users[username][0] == password:
            session['username'] = username  # Store the username in the session
            session['user_number'] = users[username][1]  # Also store the user's number
            flash('Login successful!')
            return redirect(url_for('loading'))  # Redirect to loading page
        else:
            flash('Invalid username or password. Please try again.')
            return redirect(url_for('login'))

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Login</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #f3c623, #6a0dad);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    overflow: hidden;
                    color: #fff;
                }
                .container {
                    background: rgba(255, 255, 255, 0.15);
                    border-radius: 20px;
                    padding: 40px;
                    width: 100%;
                    max-width: 400px;
                    text-align: center;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
                }
                h2 {
                    margin-bottom: 20px;
                    color: #f3c623;
                    font-size: 2rem;
                    font-weight: 700;
                }
                input[type="text"], input[type="password"] {
                    width: 100%;
                    padding: 12px;
                    margin: 10px 0;
                    border: 2px solid #6a0dad;
                    border-radius: 8px;
                    outline: none;
                    font-size: 1rem;
                    background-color: #fff;
                    color: #333;
                }
                button {
                    width: 100%;
                    padding: 14px;
                    background-color: #6a0dad;
                    color: #fff;
                    border: none;
                    border-radius: 8px;
                    font-size: 1.1rem;
                    cursor: pointer;
                }
                .footer {
                    margin-top: 20px;
                    color: #f3c623;
                    font-size: 0.9rem;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Login</h2>
                <form method="post">
                    <input type="text" name="username" placeholder="Enter your name" required><br>
                    <input type="password" name="password" placeholder="Enter your password" required><br>
                    <button type="submit">Login</button>
                </form>
                <div class="footer">
                    <p>Don't have an account? <a href="/" style="color: #fff;">Register here</a></p>
                </div>
            </div>
        </body>
        </html>
    ''')

@app.route('/loading')
def loading():
    return render_template_string(''' 
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Loading</title>
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background: linear-gradient(135deg, #f3c623, #6a0dad);
                    color: #fff;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }
                .loader {
                    border: 8px solid rgba(255, 255, 255, 0.2);
                    border-radius: 50%;
                    border-top: 8px solid #f3c623;
                    width: 60px;
                    height: 60px;
                    animation: spin 1s linear infinite;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                .message {
                    margin-top: 20px;
                }
            </style>
            <script>
                setTimeout(function() {
                    window.location.href = '/dashboard';  // Redirect to the dashboard after a delay
                }, 2000); // Adjust this delay as needed
            </script>
        </head>
        <body>
            <div>
                <div class="loader"></div>
                <div class="message">Logging in...</div>
            </div>
        </body>
        </html>
    ''')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        user_number = session['user_number']
        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Dashboard</title>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"> <!-- FontAwesome CDN -->
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: linear-gradient(135deg, #f3c623, #6a0dad);
                        color: #fff;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        position: relative; /* Added for positioning of the button */
                    }
                    .panel {
                        background: rgba(255, 255, 255, 0.1);
                        border-radius: 20px;
                        padding: 40px;
                        text-align: center;
                        backdrop-filter: blur(10px);
                        border: 1px solid rgba(255, 255, 255, 0.2);
                        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
                        display: flex;
                        flex-direction: column;  
                        justify-content: space-between;  
                        height: 300px;  /* Increased height for better layout */
                        display: none; /* Initially hide the panel */
                    }
                    h2 {
                        margin-bottom: 20px;
                    }
                    .copy-section {
                        display: flex;
                        align-items: center;
                        justify-content: center; 
                        margin-top: 10px; 
                    }
                    #user-number {
                        margin-right: 10px; 
                        font-size: 1.2rem; 
                    }
                    .copy-icon {
                        cursor: pointer;
                        font-size: 1.5rem; 
                        color: #6a0dad; 
                    }
                    input[type="text"] {
                        width: 100%;
                        padding: 12px;
                        margin: 10px 0;
                        border: 2px solid #6a0dad;
                        border-radius: 8px;
                        outline: none;
                        font-size: 1rem;
                        background-color: #fff;
                        color: #333;
                    }
                    button {
                        padding: 10px;
                        background-color: #6a0dad;
                        color: #fff;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                    }
                </style>
                <script>
                    function copyToClipboard() {
                        var numberText = document.getElementById("user-number").innerText;
                        navigator.clipboard.writeText(numberText).then(function() {
                            alert("Number copied to clipboard: " + numberText);
                        }, function(err) {
                            console.error("Could not copy text: ", err);
                        });
                    }

                    function togglePanel() {
                        var panel = document.getElementById("panel");
                        if (panel.style.display === "none" || panel.style.display === "") {
                            panel.style.display = "flex"; // Show panel
                        } else {
                            panel.style.display = "none"; // Hide panel
                        }
                    }

                    function createNumber() {
                        var newNumber = document.getElementById("new-number").value;
                        alert("Number created: " + newNumber);
                        document.getElementById("new-number").value = ""; // Clear input after submission
                    }
                </script>
            </head>
            <body>
                <button onclick="togglePanel()" style="position: absolute; top: 20px; right: 20px; background: #6a0dad; color: white; border: none; border-radius: 5px; padding: 10px;">New</button>
                <div class="panel" id="panel">
                    <h2>Welcome, {{ session['username'] }}!</h2>
                    <div class="copy-section">
                        <p>Your number: <span id="user-number">{{ user_number }}</span></p>
                        <i class="fas fa-copy copy-icon" onclick="copyToClipboard()" title="Copy to clipboard"></i>
                    </div>
                    <div>
                        <input type="text" id="new-number" placeholder="Put the number here" required>
                        <button onclick="createNumber()">Create number</button>
                    </div>
                </div>
            </body>
            </html>
        ''', user_number=user_number)
    else:
        flash("You need to log in first!")
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
