<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Networking - README</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
        }
        
  h1, h2, h3 {
            color: #333;
        }
        
  code {
            font-family: Consolas, monospace;
            background-color: #f0f0f0;
            padding: 2px 6px;
            border-radius: 4px;
        }
        
  pre {
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
        
  .container {
            max-width: 800px;
            margin: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Social Networking</h1>

  <h2>Description</h2>
        <p>The project is a Django-based web application containerized with Docker, facilitating user registration, authentication, friend requests, and management through RESTful APIs. It employs JWT for secure authentication and includes rate limiting for API endpoints.</p>

  <h2>Table of Contents</h2>
        <ol>
            <li><a href="#installation">Installation</a></li>
            <li><a href="#requirements">Requirements</a></li>
            <li><a href="#database-setup">Database Setup</a></li>
            <li><a href="#usage">Usage</a></li>
            <li><a href="#endpoints">Endpoints</a></li>
            <li><a href="#environment-variables">Environment Variables</a></li>
            <li><a href="#additional-notes">Additional Notes</a></li>
        </ol>

  <h2 id="installation">Installation</h2>
        <p>To run this project locally, Docker and Docker Compose need to be installed on your machine.</p>

  <h3>Steps:</h3>
        <ol>
            <li><strong>Clone the repository:</strong></li>
            <pre><code>git clone &lt;repository-url&gt;
cd &lt;project-folder&gt;</code></pre>

  <li><strong>Set up environment variables:</strong></li>
            <p>Create a <code>.env</code> file in the root directory and add the following variables (example provided):</p>
            <pre><code># Example .env file
HASH_KEY=your_secret_hash_key_here

# Database configuration for PostgreSQL
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=db
DB_PORT=5432</code></pre>
            <p>Replace placeholders with your actual secret keys and PostgreSQL database details.</p>

  <li><strong>Build and run Docker containers:</strong></li>
            <pre><code>docker-compose up --build</code></pre>
            <p>This command will build the Docker images and start the containers.</p>

  <li><strong>Apply database migrations:</strong></li>
            <pre><code>docker-compose exec web python manage.py migrate</code></pre>

  <li><strong>Create a superuser (optional):</strong></li>
            <p>If you need access to Django admin:</p>
            <pre><code>docker-compose exec web python manage.py createsuperuser</code></pre>
            <p>Follow the prompts to create a superuser account.</p>
        </ol>

  <h2 id="requirements">Requirements</h2>
        <p>Below is the list of Python packages required for this project. To install all dependencies, run the following command:</p>
    <pre><code>pip install -r requirements.txt</code></pre>
        <pre><code>
asgiref==3.8.1
Django==5.0.6
django-ratelimit==4.1.0
djangorestframework==3.15.1
psycopg2-binary==2.9.9
PyJWT==2.8.0
python-dotenv==1.0.1
sqlparse==0.5.0
tzdata==2024.1
        </code></pre>

  <h2 id="database-setup">Database Setup</h2>
        <p>This project uses PostgreSQL as the database backend. Make sure you have PostgreSQL installed locally or accessible via a remote server.</p>
        <p>Set up your PostgreSQL database credentials in the <code>.env</code> file under <strong>Database configuration</strong>.</p>
        <p>Example:</p>
        <pre><code># Database configuration for PostgreSQL
DB_NAME=mydatabase
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=db
DB_PORT=5432</code></pre>
        <p>Ensure the <code>DB_HOST</code> matches the service name defined in your <code>docker-compose.yml</code> file for the database service.</p>

<h2 id="usage">Usage</h2>
<p>Once you have set up the project following the installation steps, you can interact with the application using the provided API endpoints. Here’s a brief overview of how to use the key features:</p>

<h3>User Registration and Login:</h3>
<ol>
    <li><strong>Register a new user:</strong> Send a POST request to `/userregister` with the following JSON payload:
        <pre><code>{
    "name" : "your_name"    
    "email": "example@example.com",
    "password": "your_password"
}</code></pre>
    </li>
    <li><strong>Login:</strong> Send a POST request to `/login` with the following JSON payload:
        <pre><code>{
    "email": "example@example.com",
    "password": "your_password"
}</code></pre>
        <p>Upon successful login, you will receive a JWT token in the response.</p>
    </li>
</ol>

<h3>Friend Requests:</h3>
<ul>
    <li><strong>Send a friend request:</strong> Send a POST request to `/send_friend_request/<int:to_user_id_sent>` where `<int:to_user_id_sent>` is the ID of the user you want to send a friend request to.</li>
    <li><strong>Accept or Reject a friend request:</strong> Use the endpoints `/accept_friend_request/<int:request_id>` and `/reject_friend_request/<int:request_id>` to manage pending friend requests.</li>
    <li><strong>View pending friend requests:</strong> Send a GET request to `/pending_request` to retrieve a list of pending friend requests.</li>
    <li><strong>View friends:</strong> Send a GET request to `/friends` to retrieve a list of accepted friends.</li>
</ul>

<h3>User Search:</h3>
<p>To search for users by email or name, send a GET request to `/search/<str:keyword>`, where `<str:keyword>` is the search keyword.</p>
<p>For example, `/search/example` will search for users whose names or emails contain "example".</p>

  <h2 id="endpoints">Endpoints</h2>
        <ul>
            <li><strong>POST `/login`:</strong> User login endpoint.</li>
            <li><strong>POST `/userregister`:</strong> User registration endpoint.</li>
            <li><strong>GET `/search/&lt;str:keyword&gt;`:</strong> Search users endpoint.</li>
            <li><strong>POST `/send_friend_request/&lt;int:to_user_id_sent&gt;`:</strong> Send friend request endpoint.</li>
            <li><strong>PUT `/accept_friend_request/&lt;int:request_id&gt;`:</strong> Accept friend request endpoint.</li>
            <li><strong>PUT `/reject_friend_request/&lt;int:request_id&gt;`:</strong> Reject friend request endpoint.</li>
            <li><strong>GET `/pending_request`:</strong> List pending friend requests endpoint.</li>
            <li><strong>GET `/friends`:</strong> List friends endpoint.</li>
        </ul>

  <h2 id="environment-variables">Environment Variables</h2>
        <ul>
            <li><strong>HASH_KEY:</strong> Secret key for hashing.</li>
            <li><strong>Database Configuration:</strong> Configure your PostgreSQL database settings in the <code>.env</code> file as shown above.</li>
        </ul>
        <p>Ensure these environment variables are set correctly in your <code>.env</code> file.</p>

<h2 id="additional-notes">Additional Notes</h2>
<p>This Django project is designed to facilitate user registration, authentication, friend requests, and management of friends. Below are some key features and considerations:</p>

<h3>Key Features:</h3>
<ul>
    <li><strong>User Registration and Authentication:</strong> Users can register with their email and password. Authentication is handled using JWT (JSON Web Tokens) for secure API authentication.</li>
    <li><strong>Friend Requests:</strong> Users can send and receive friend requests. Friend requests have statuses (pending, accepted, rejected) and can be managed accordingly.</li>
    <li><strong>Search Functionality:</strong> Users can search for other users by email or name.</li>
    <li><strong>Friend List:</strong> Users can view their list of accepted friends.</li>
</ul>

<h3>Technologies Used:</h3>
<ul>
    <li><strong>Django:</strong> Backend framework for building web applications in Python.</li>
    <li><strong>Django REST Framework (DRF):</strong> Powerful and flexible toolkit for building Web APIs in Django.</li>
    <li><strong>JWT (JSON Web Tokens):</strong> Used for API authentication.</li>
    <li><strong>PostgreSQL:</strong> Relational database used to store application data.</li>
    <li><strong>Docker:</strong> Containerization platform used for development and deployment.</li>
</ul>

<h3>Usage Notes:</h3>
<ul>
    <li>Ensure Docker and Docker Compose are installed on your machine before starting.</li>
    <li>Modify the <code>.env</code> file with your actual secret keys and PostgreSQL database credentials before running the application.</li>
    <li>Use the provided API endpoints to interact with the application (e.g., user registration, login, friend requests). You can use tools like <a href="https://www.postman.com/">Postman</a> to test the endpoints.</li>
    <li>Refer to the <code>requirements.txt</code> file for Python package dependencies.</li>
</ul>
    </div>
</body>
</html>
