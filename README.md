# Microblog Backend

### Author
Justin Blanco

### Class/Section
449-02

## Project Summary
Adds asynchronous messaging to the projects 2&3. Uses the greenstalk library for accessing the beanstalk work queue.
Performance tested using hey and uses python's debugging server for SMTP.

## Starting Application
Verify that the current working directory is api/ `cd api/`

Start up your local instance of DynamoDb using while in the installed directory
`java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb`

Run the following commands to initialize the database and start the API

`./bin/init.sh`

`foreman start`

Open a new command line Terminal in the api directory and Start HAProxy Load Balancer
  
`sudo haproxy -f ./etc/haproxy.cfg -D -p ./var/run/haproxy.pid -sf $(cat ./var/run/haproxy.pid)`

# Documentation

# API Documentation
## Content Negotiation
Both APIs will respond to the following 'Accept:' values
* application/json

## User API Operations - users_api.py
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

## Timelines API Operations - posts_api.py
GET   /timelines/home?username= - home timeline of a user consisting of recent posts by all users that this user follows (5 per friend)<br>

GET   /timelines/posts/{username} - posts a user has made
GET   /timelines/public - all posts from all users

POST  /timelines/posts/ - add a new post by a user
POST  /timelines/posts/jobs - add a new post by a user using the message queue

## Likes API Operations - likes_api.py
GET   /likes/{post_id} - get the number of likes of a post
PUT   /likes/{post_id} - likes a post
GET   /likes/users/{user_id} - lists of users' likes
GET   /likes/popular - list of top 10 popular posts

## Polls API Operations - polls_api.py
GET   /polls/ - returns all polls of all users
GET   /polls/users/{user_id} - returns the polls of a user
GET   /polls/questions/{question} - returns the poll of a question
PUT   /polls/users/{user_id} - vote for a user poll
