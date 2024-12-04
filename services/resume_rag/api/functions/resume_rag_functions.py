import azure.functions as func
import logging
import json
from datetime import datetime

# Services
from services.resume_rag.api.services.resume_rag_service import ResumeRagService

# Requests/Response
from services.resume_rag.api.functions.models.get_resume_inference_request import GetResumeInferenceRequest
from services.resume_rag.api.functions.models.get_resume_inference_response import GetResumeInferenceResponse

# App Registration
bp = func.Blueprint()

# Service Registration
_videoRagService = ResumeRagService()
    
@bp.function_name('GetResumeInference')
@bp.route(route="getresumeinference", methods=[func.HttpMethod.POST])
async def get_resume_inference(req: func.HttpRequest) -> func.HttpResponse:
    # Log for Azure App Insights
    logging.info('Python HTTP trigger function processed a request.')

    # Parse request body
    try:
        request = GetResumeInferenceRequest(**req.get_json())

        # Service Layer Call
        get_resume_inference_model = await _videoRagService.get_resume_inference_async(request.query)
        
        # Map to response
        # response = response_model
        get_resume_inference_response = GetResumeInferenceResponse(
            llm_response = get_resume_inference_model.llm_response,
            context_sources = get_resume_inference_model.context_sources
        )
        
        return func.HttpResponse(
            get_resume_inference_response.model_dump_json(),
            status_code=200
        )
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
    
        return func.HttpResponse(str(e), status_code=getattr(e, 'status_code', 400))

# TODO: Replace with Blob Storage
@bp.function_name(name="embedresumetimer")
@bp.schedule(schedule="0 0 * * *", arg_name="embedresumetimer", run_on_startup=True, use_monitor=False)
async def embed_resume_timer(embedresumetimer: func.TimerRequest) -> None:
    await _videoRagService.delete_resume_embeddings()
    
    iframe_url = 'https://resume.creddle.io/embed/6x3f8thxdss'
    await _videoRagService.save_resume_embeddings_from_iframe(iframe_url)
    
    logging.info(f'Timer trigger function ran at {datetime.now()}. Resume embeddingss deleted.')
