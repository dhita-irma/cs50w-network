# Network - Social Network
Twitter-like social network built with Django 3.1.1 and JavaScript.


## Table of Contents
- [Project Summary](#project-summary)
- [Technologies](#technologies)
- [Features](#features)
- [Setup](#setup)


## Project Summary
This project is created for [Project 4 of CS50W](https://cs50.harvard.edu/web/2020/projects/4/network/). Network is a Twitter-like social network for following users, making and liking posts.

What's included in CS50W distribution code: initial django app set up, views and urls route for login, logout, and register. 


## Technologies 
#### Python Django 3.1.1
- Create endpoints: render homepage, following page, profile page
- Create APIs: create post, post detials, edit posts, like/unlike posts
- Create models: User, Post, UserFollowing, Like

#### JavaScript
- Fetch posts with API to create, display, and edit 
- Implement dynamic Follow/Unfollow, Like/Unlike, and Edit button 
- Create, hide, and display elements 

## Features 
- Create new post
- Edit post  
- Following feed
- Profile page
- Follow / Unfollow users
- Like / Unlike posts



## Setup 
- Clone or download this repository in the folder and open it in your editor of choice.
- Create and activate [virtual environment](https://docs.python.org/3.9/library/venv.html) by running following command in the terminal of the base directory of this project:

    ```
    python -m venv <virtual environment name>
    C:\> <venv address>\Scripts\activate
    ```

- Then install the project dependencies with
    ```
    pip install -r requirements.txt
    ```
- Now you can run the project with this command
    ```
    python manage.py runserver

    ```

