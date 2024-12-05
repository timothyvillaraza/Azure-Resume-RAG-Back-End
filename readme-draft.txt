Deploying Cloud Infrastructure
    Navigate to <root>/deploy/terraform
    Create secrets.tfvars
        ``
        postgres_admin_username = "pgadmin"             # OPTIONAL: The default of "pgadmin" is configured in variables.tf
        postgres_admin_password = "StrongPassword123!"  # PASSWORD
        ```
    terraform init
    terraform apply -var-file="secrets.tfvars"

    Database Setup
    Setting up Vector Extension - Enables the use of vector types
    Connect to the postgres database made by terraform
    CREATE EXTENSION IF NOT EXISTS vector;

Local Development (w/ Deployed Database)
    .env setup
        Create a .env file with the following environment variables

        Sample:
        ```
        OPENAI_KEY = <key>

        PG_VECTOR_DRIVER = 'postgresql+psycopg'
        PG_VECTOR_USER = <user>
        PG_VECTOR_PASSWORD = <password>
        PG_VECTOR_HOST = <host>
        PG_VECTOR_PORT = <port>
        PG_VECTOR_DATABASE_NAME = <db name>
        ```
    Running Locally
        func start in the root folder (folder containing function_app.py)