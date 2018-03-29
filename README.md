# hello-books-api
![Screenshot](https://travis-ci.org/meshack-mbuvi/hello-books-api.svg?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/700f93f2d9b3c5435d39/maintainability)](https://codeclimate.com/github/meshack-mbuvi/hello-books-api/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/700f93f2d9b3c5435d39/test_coverage)](https://codeclimate.com/github/meshack-mbuvi/hello-books-api/test_coverage)

[![Coverage Status](https://coveralls.io/repos/github/meshack-mbuvi/hello-books-api/badge.svg?branch=master)](https://coveralls.io/github/meshack-mbuvi/hello-books-api?branch=master)


This is aa api part of hello-books; is a simple Flask application that helps manage a basic library system and its processes like stocking,tracking and renting books.

When fully finished, the application has the following endpoints:

    An admin section from where administrators can do things like add new admins, add new books, 
    remove and/or update book information.
    User section from where users can create their accounts, borrow and return borrowed books.
    
The following end-points have been implement so far :
    - POST /api/v1/books -> Add a new book
    - PUT /api/v1/books/<bookId> ->edit book info
    - DELETE /api/v1/books/<bookId>
    - GET /api/v1/books 
    - GET /api/v1/books/<bookId> 
    - POST /api/v1/users/books/<bookId> -> user borrows a book
    - POST /api/v1/auth/register -> register new user
    - POST /api/auth/reset-password 
    
#Installation and use:
To work with this project on :
    - Navigate to root directory of your server.
    - Clone this repository on that directory
    - Using SSH:
    
       git@github.com:meshack-mbuvi/hello-books-api.git
    
    - Using HTTP:
    
        https://github.com/meshack-mbuvi/hello-books-api.git
        
For best experience and functionality of all endpoints, use Postman since it supports all http verbs. You can also use your terminal to end data.


*Note* : The project is on development and some functionalities may not be fully working. This is only the front-end part of the whole application.

#Contribution
 If you want to contribute to this project:

   - Fork it!
   - Create your feature branch: git checkout -b my-new-feature
   - Commit your changes: git commit -am 'Add some feature'
   - Push to the branch: git push origin my-new-feature
   - Submit a pull request :D
