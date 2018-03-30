# hello-books-api
![Screenshot](https://travis-ci.org/meshack-mbuvi/hello-books-api.svg?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/700f93f2d9b3c5435d39/maintainability)](https://codeclimate.com/github/meshack-mbuvi/hello-books-api/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/meshack-mbuvi/hello-books-api/badge.svg?branch=master)](https://coveralls.io/github/meshack-mbuvi/hello-books-api?branch=master)

This is an API part of hello-books - a simple Flask application that helps manage a basic library system and its processes like stocking,tracking and renting books.
    
The following end-points have been implement so far :

    - POST /api/v1/books                -> Add a new book
    - PUT /api/v1/books/<bookId>        ->edit book info
    - DELETE /api/v1/books/<bookId>     -> delete a book
    - GET /api/v1/books                 -> retrieve all books
    - GET /api/v1/books/<bookId>        -> get a particular book
    - POST /api/v1/users/books/<bookId> -> user borrows a book
    - POST /api/v1/auth/register        -> register new user
    - POST /api/auth/reset              -> reset password
    
# Installation and use:
To work with this project on :
    - In your terminal,clone this repository on any directory of your choice
    
        $ git clone https://github.com/meshack-mbuvi/hello-books-api.git

   
   - If you do not have [virtual environment](https://virtualenv.pypa.io/en/stable/installation/), install one in your system.
   - cd to hello-books-api and execute the following commands:
        
        - $ virtualenv venv 
        - $ source venv/bin/activate
        - $ pip install -r requirements.txt
   - To make sure all tests are passing, execute
        - $ python tests.py
   - Then run the :
        - $ python run.py
        
   - Install and open [Postman](https://www.getpostman.com/) to experiment with the given endpoints.
       

# Contribution
 If you want to contribute to this project:
   - Fork it!
   - Create your feature branch: git checkout -b my-new-feature
   - Commit your changes: git commit -am 'Add some feature'
   - Push to the branch: git push origin my-new-feature
   - Submit a pull request :D
