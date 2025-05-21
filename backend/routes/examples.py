from fastapi import APIRouter

router = APIRouter()

@router.get("/examples")
def get_example_queries():
    return {
        "examples": [
            "Get me a list of group leaders who had zero orders last weekend.",
            "Which registration channel shows the highest 30-day retention rate for users who signed up in July?",
            "Which fresh produce items had the highest sales volume in August? Show me a daily sales breakdown for the top 3 items.",
            "Identify the top 10 group leaders who brought the most new, first-time purchasing customers to ChipChip.",
            "What are the peak shopping times for 'Working Professionals' during weekdays?"
        ]
    }
