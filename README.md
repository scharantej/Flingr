## Flask Application Design for a Dating App

### HTML Files

**index.html**

- Landing page of the application.
- Contains forms for user registration, login, and a brief introduction to the app.

**profile.html**

- User's profile page.
- Displays user's information, preferences, and a list of potential matches.

**matches.html**

- Page showing a list of potential matches.
- Includes details about each match, such as profile picture, name, and compatibility score.

**chat.html**

- Chat interface for users to connect with their matches.
- Contains a conversation history and input field for sending messages.

### Routes

**@app.route('/register', methods=['GET', 'POST'])**

- Handles user registration.
- Accepts GET requests for displaying the registration form and POST requests for processing the submitted data.

**@app.route('/login', methods=['GET', 'POST'])**

- Handles user login.
- Accepts GET requests for displaying the login form and POST requests for authenticating the user.

**@app.route('/profile', methods=['GET'])**

- Displays the user's profile page.
- Accepts GET requests only.

**@app.route('/matches', methods=['GET'])**

- Displays a list of potential matches for the user.
- Accepts GET requests only.

**@app.route('/chat/<match_id>', methods=['GET', 'POST'])**

- Handles chat communication between the user and a specific match.
- Accepts GET requests for displaying the chat interface and POST requests for sending messages.