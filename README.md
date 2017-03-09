# OILS

[![Build Status](https://travis-ci.org/9gix/oils.svg?branch=master)](https://travis-ci.org/9gix/oils) 
[![Codecov]( https://codecov.io/github/9gix/oils/coverage.svg?branch=master)](https://codecov.io/github/9gix/oils?branch=master)


OILS Framework is an Integrated Library System (ILS) framework using a loosely coupled django apps.
In this repository, you will find a few django apps that are common among library system, 
such as cataloging, circulation and membership. 


## How to use OILS

A django knowledge is very useful before start using OILS. Because OILS is just a collections of django apps without any project.
You will have to create or use your existing django project, and include these apps into your project settings.

Alternatively, if you are starting a fresh new library project, you use our default template to start the django project.

    # Start a Fresh django Project
    django-admin.py startproject --template=https://github.com/9gix/oils/zipball/project-template -n Makefile,README.md <project-name>
    
    # Setup dependencies, db migration, assets
    make setup_dev
    
    # Runserver at port 8000
    make dev

## For contributors

### Requirements

- Python 3
- NodeJS

### Build and Run

1. Create a spinoff library

        django-admin.py startproject --template=https://github.com/9gix/oils/zipball/project-template -n Makefile,README.md <project-name>

    You can change the template path to your own copy of `project-template` if you are making changes to it and want to test it out.

2. Open `requirements/base.pip` in your spinoff library directory and change the path to the directory where your local copy of OILS is located.

3. Follow the README.md of the spinoff library.
