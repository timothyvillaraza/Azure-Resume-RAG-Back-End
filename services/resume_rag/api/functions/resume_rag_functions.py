import azure.functions as func
import logging
from io import BytesIO

# Services
from services.resume_rag.api.services.resume_rag_service import ResumeRagService

# Requests/Response
from services.resume_rag.api.functions.models.get_resume_inference_request import GetResumeInferenceRequest
from services.resume_rag.api.functions.models.get_resume_inference_response import GetResumeInferenceResponse

# App Registration
bp = func.Blueprint()

# Service Registration
_resumeRagService = ResumeRagService()
    
@bp.function_name('GetResumeInference')
@bp.route(route="getresumeinference", methods=[func.HttpMethod.POST])
async def get_resume_inference(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Parse request body
        request = GetResumeInferenceRequest(**req.get_json())

        # Service Layer Call
        get_resume_inference_model = await _resumeRagService.get_resume_inference_async(request.query)
        
        # Map to response
        get_resume_inference_response = GetResumeInferenceResponse(
            llm_response = get_resume_inference_model.llm_response,
            context_sources = get_resume_inference_model.context_sources
        )
        
        # Return response
        return func.HttpResponse(get_resume_inference_response.model_dump_json(), status_code=200)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
    
        return func.HttpResponse(str(e), status_code=getattr(e, 'status_code', 400))

@bp.function_name(name="EmbedResumeOnUpload")
@bp.blob_trigger(arg_name="blob", path="bcresumerag/resume.pdf", connection="AzureWebJobsStorage")
async def embed_resume_on_upload(blob: func.InputStream) -> None:
    try:
        await _resumeRagService.delete_resume_embeddings()
        
        # Serialize incoming PDF
        pdf = BytesIO(blob.read())
        
        await _resumeRagService.save_resume_embeddings_from_pdf(pdf)
        
        logging.info(f'{blob.name} embedded')
    except Exception as e:
        logging.error(f"Error processing PDF: {e}")
