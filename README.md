# Reqs

Tested on `python 3.10`.

# How to run?

```bash
pip install -r requirements.txt
```

```bash
docker run --name mysql-fastapi -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=fastapi_db -p 3306:3306 -d mysql:8.0
```

Inside root project:
```bash
PYTHONPATH=`pwd` uvicorn main:app --reload
```

To test:
```bash
PYTHONPATH=`pwd` pytest tests
```


# Task content

Task Description:

- Develop a web application following the MVC design pattern.(Meaning 3 different Levels for Routing, Business Logic, DB calls for each call Functionality)
- Interface with a MySQL database using SQLAlchemy for ORM.
- Implement field validation and dependency injection as needed.
- Use Python and FastAPI for building the application.

Submission Guidelines:

- Submit your code via GitHub by sharing the repository link to lucidtasksubmission@gmail.com.
- Time to submit the task - 2h
- Make the repo public

Application Requirements:


1. Endpoints:

All data entities should have defined a SQLAlchemy model and a Pydantic model with extensive type validation for both.(validating all their fields in schema and model field type)



  Signup Endpoint:
    Accepts email and password.
    Returns a token (JWT or randomly generated string).


  Login Endpoint:
    Accepts email and password.
    Returns a token upon successful login; error response if login fails.

  AddPost Endpoint:
    Accepts text and a token for authentication.
    Validates payload size (limit to 1 MB), saves the post in memory, returning postID.
    Returns an error for invalid or missing token.
    Dependency injection for token authentication.
  GetPosts Endpoint:
    Requires a token for authentication.
    Returns all user's posts.
    Implements response caching for up to 5 minutes for the same user.
    Returns an error for invalid or missing token.
    Dependency injection for token authentication.

  DeletePost Endpoint:
    Accepts postID and a token for authentication.
    Deletes the corresponding post from memory.
    Returns an error for invalid or missing token.
    Dependency injection for token authentication.


2. Additional Requirements:

Important: Make sure all functions and dependencies run efficiently, without extra database calls or unnecessary steps. Try to use the least number of database calls needed for the task. 
Utilize token-based authentication for the "AddPost" and "GetPosts" endpoints, obtainable from the "Login" endpoint.
  Implement request validation for the "AddPost" endpoint to ensure the payload does not exceed 1 MB.
  Use in-memory caching for "GetPosts" to cache data for up to 5 minutes.
Ensure the implementation of both SQLAlchemy and Pydantic models for each endpoint includes extensive type validation to guarantee the accuracy and integrity of data being processed.
Documentation and comments should be comprehensive, on each and every function there should be documentation explaining the purpose and functionality of the code.