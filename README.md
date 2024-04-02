# E-Learning Platform API 
The E-Learning Platform API provides a comprehensive solution for building an online learning platform where users can register, access courses, interact with educational content, track their progress, and receive certificates. This API allows developers to create, manage, and customize various features of the e-learning platform to suit their specific requirements.

## Installation

- Docker installed on your machine ([Install Docker](https://docs.docker.com/get-docker/))

- Python virtual env
1. Open a terminal and create with:
    ```bash
    pyenv virtaulenv 3.11.4 env-name 
    ```
2. Install dependencies from requirements.txt
    ```bash
    cd uki-sotre-app
    pyenv activate env-name
    pip install -r requirements.txt
    pip install --upgrade pip
    ```
    Replace `env-name` with your desired virtual env name.

## Environment Variables

Add and set .env with vars to use database:

#### Set Database credentials
- `DB_PORT`: Port of postgresql database (5432).
- `DB_HOST`: Host of database.
- `DB_USER`: User of database.
- `DB_PASSWORD`: Password of database.
- `DB_NAME`: Name of database.


#### Set for postgresql database docker image
- `POSTGRES_DB="{DB_NAME}"`
- `POSTGRES_USER="{DB_USER}"`
- `POSTGRES_PASSWORD="{DB_PASSWORD}"`

#### Set postgresql database uri
- `DATABASE_URL="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"`

#### Set postgresql database uri
- `IMAGE_NAME=your-img-name`

## Building the Docker containers

Follow the next steps to build the python and db containers:

1. Open a terminal.
2. Navigate to the directory of the project.
3. Run the following command:

    ```bash
    docker compose build --no-cache
    docker compose up -d 
    ```

    You can remove flag `-d` to show in terminal logs while container is running.

Now you can run the application on your localhost: http://localhost:80

## Contributions
As were said, the project is in current development,therefore it is possible if you investigate on it, probably get any  kind of error or improvements areas. If that's the case, feel yourself free to contribute with your comments, features, issues or pull request. I'll take a look. Thanks!
