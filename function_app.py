import azure.functions as func
from services.resume_rag.api.functions import resume_rag_functions
from dotenv import load_dotenv

app = func.FunctionApp()

# Register blueprints
app.register_blueprint(resume_rag_functions.bp)