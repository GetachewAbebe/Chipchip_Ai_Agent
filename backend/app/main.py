from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import json

app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic model to match the frontend's exact structure
class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)

@app.post("/ask")
async def ask(request: Request):
    try:
        # Parse JSON body
        body = await request.json()
        
        # Validate the request using Pydantic model
        question_request = QuestionRequest(**body)
        
        # Extract question
        question = question_request.question
        
        # Placeholder AI response logic
        answer = generate_ai_response(question)
        
        return {
            "status": "success",
            "question": question,
            "answer": answer
        }
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except ValueError as ve:
        # Handle validation errors
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(status_code=500, detail="Internal server error")

def generate_ai_response(question: str) -> str:
    """
    Placeholder function for AI response generation
    """
    if not question:
        return "Please provide a valid question."
    
    # Simple placeholder logic
    return f"AI response to: '{question}'. This is a placeholder response."

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Service is up and running"}
