Deploying Cloud Infrastructure
    Login to azure account
        `az login`

    Deploy
        Navigate to <root>/deploy/terraform
        Create secrets.tfvars
        Sample:
        ``
        # secrets.tfvars
        azure_subscription_id   = <Subscription ID>
        postgres_admin_username = <Username>  # OPTIONAL: The default of "pgadmin" is configured in variables.tf
        postgres_admin_password = <Password>
        ```
        terraform init
        terraform apply -var-file="secrets.tfvars"
    
    Confirm
        On the azure portal, check the resource groups

Local Development (w/ Deployed Database)
    Install Dependencies from Requirmenets files
        Navigate to root
        `pip install -r requirements.txt`

    Configure Azure local.settings.json
        Create a local.settings.json in the root folder, get the connection string of the storage account from <storage account> -> Security + networking -> Access Keys
        Sample:
        ```
        {
        "IsEncrypted": false,
        "Values": {
            "AzureWebJobsStorage": <storage account connection string>,
            "FUNCTIONS_WORKER_RUNTIME": "python",
            "AzureWebJobsFeatureFlags": "EnableWorkerIndexing"
        },
        "Host": {
            "LocalHttpPort": 5004,
            "CORS": "*"
        }
        }
        ```

    Database IP White Listing
        Allows you to connect to the azure hosted postgres database from you local computer
        On the azure portal, navigate to the database -> Settings -> Networking and allow your IP

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