import azure.functions as func
from services.resume_rag.api.functions import resume_rag_functions
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Initialize Azure Functions
app = func.FunctionApp()

# Register blueprints
app.register_blueprint(resume_rag_functions.bp)