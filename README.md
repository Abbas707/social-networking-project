# Social Networking API

This is a Django-based API for a social networking application, which includes functionalities like user login/signup, searching users, sending/accepting/rejecting friend requests, and more. The project is set up with Docker for easy deployment and environment management.

## Features

- **User Management:** User registration and authentication.
- **Friend Requests:** Send, accept, reject friend requests.
- **User Search:** Search users by email or name with pagination.
- **Friend List:** View accepted friends and pending requests.
- **Database:** MySQL used for persistent storage.

## Requirements

- Docker
- Docker Compose
- Python 3.x (if running locally without Docker)

## Getting Started

### Clone the Repository

```bash
$ git clone https://github.com/Abbas707/social-networking-project.git
$ cd social-networking-project
```

## Local Development :grinning:
### *If you prefer to run the project locally without Docker*:

### 1. **Create the virtualenv and install the requirements**:
The local **virtual env** must then be created. You could wonder **"is a virtual environment is necessary? "** because we're using Docker. The answer is **YES** since there may be times when you wish to test your project locally without using Docker, and **venv** will accelerate our procedure at those times. As a result, let's create the **.venv**.
- make sure our working directory would be the **social-netowrking-project** and branch would be the **main**
  - `$ python -m venv social-network-env`
- Activate the **.venv**
  - `source ./social-network-env/bin/activate`
- Navigate to the project directory and install the requirements
  - `(.social-network-env) my_system/social-networking-project (main) $ pip install -r requirements.txt`

### 2. Set Up the Database:
Make sure you have a postgres server running locally and create a database for the project. Update the .env file with your local database credentials.

### 3. Run Migrations:
- `$ python manage.py migrate`

### 4. Create .env based on environment:
We have to create the **.env** at our project level as all the credentials and configuration will defined into **.env** file. With help of [environ](https://pypi.org/project/environs/) package python will load it and use it. this **.env** is use in docker as well. Following table contains all the configuration with optional flag, default value, docker required variables, project required variables.

| Variable Name     | Optional | Default Value | Docker                                 | Project                                       |
|-------------------|----------|---------------|----------------------------------------|-----------------------------------------------|
| POSTGRES_DB       | NO       |               | [Yes] in postgres container required   | [Yes] for connecting to database              |
| HOST              | NO       | postgres_db   | [Yes] in docker db service itself host | [Yes] for connectiong to db service           |
| POSTGRES_USER     | NO       | postgres      | [Yes] postgres image need required     | [Yes] for connecting to database              |
| POSTGRES_PASSWORD | NO       | postgres      | [Yes] postgres image need required     | [Yes] for connecting to database              |
| PORT              | NO       | 5432          | [Yes] postgres image need required     | [Yes] for connecting to database              |

### 5. Run the Server:
- `$ python manage.py runserver`


## Docker Setup :smiley:

### 1. **Install the docker and docker-compose according to your OS**

### 2. **Run the project in docker container**:
Now we are going to build the docker image and running the docker-compose service into detached mode it will may take time if predefined image not found like postgres, python etc.
- following command will create the container from services that are defined in **docker-compose.yaml** file.
  - `$ docker-compose up --build -d`
  - **up**  will create and run the container
  - **--build** will build the docker **image** if found within the services which are listed in **docker-compose.yaml** file.
  - **-d** run docker container in detached mode(in background)
- Check is container are runnning in background and hit the [localhost](http://localhost/)
  - `$ docker ps`
