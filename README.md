# Project 03 - Microservice Implementation and Load Balancing

### Author
Justin Blanco 887073658

### Class/Section
449-02

## Project 3 Summary
This project implements two RESTful back-end services and prepares them for production deployment. Utilizes Python, sqlite_utils, requests library, and Hug Libraries. Deployed using foreman, gunicorn, and HAProxy.

## Starting Application
Verify that the current working directory is api/ `cd api/`

Run the following commands to initialize the database and start the API

`./bin/init.sh`

`foreman start`

Open a new command line Terminal in the api directory and Start HAProxy Load Balancer
  
`sudo haproxy -f ./etc/haproxy.cfg -D -p ./var/run/haproxy.pid -sf $(cat ./var/run/haproxy.pid)`

# Documentation

## API Documentation
### Content Negotiation
Both APIs will respond to the following 'Accept:' values
* application/json

### User API Operations - users_api.py
GET   /users/ - get list of all users<br>
POST  /users/ - Add a new user<br>
GET   /users/{id} - Find user by id<br>
PUT   /users/{id} - Update user by id<br>
GET   /users/search?username=,email=,bio=password= - Search for user base off parameters<br>
GET   /followers/ - get a list of a followers<br>
POST  /followers/ - add a new follower<br>
GET   /followers/{id} - Find follower by resource id<br>
GET   /followers/search?follower_id=,following_id= - search for follower ids base off parameters<br>
GET   /following/ - retrieves all usernames of people following each other<br>
GET   /following/{username} - retrieves a list of usernames a user is following<br>

### Timelines API Operations - posts_api.py
GET   /timelines/home?username= - home timeline of a user consisting of recent posts by all users that this user follows (5 per friend)<br>

GET   /timelines/posts/{username} - posts a user has made
GET   /timelines/public - all posts from all users

POST  /timelines/posts/ - add a new post by a user




