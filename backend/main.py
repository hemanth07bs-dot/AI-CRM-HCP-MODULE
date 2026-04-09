from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/chat")
def chat(input: str):

    text = input.lower()

    hcp = ""
    interaction = ""
    sentiment = ""
    followup = ""
    clear = False

    # TOOL 5 CLEAR
    if "clear" in text:
        return {
            "response": {
                "response": {
                    "clear": True
                }
            }
        }

    # HCP
    if "dr" in text:
        words = text.split()
        for i, w in enumerate(words):
            if w == "dr" and i + 1 < len(words):
                hcp = "Dr " + words[i + 1].capitalize()

    # TOOL 4 TYPE
    if "call" in text:
        interaction = "Call"

    if "meeting" in text or "met" in text:
        interaction = "Meeting"

    if "visit" in text:
        interaction = "Visit"

    # SENTIMENT
    if "positive" in text or "interested" in text:
        sentiment = "Positive"

    if "negative" in text:
        sentiment = "Negative"

    if "neutral" in text:
        sentiment = "Neutral"

    # TOOL 3 FOLLOWUP
    if "next week" in text:
        followup = "Next week"

    if "tomorrow" in text:
        followup = "Tomorrow"

    if "next month" in text:
        followup = "Next month"

    return {
        "response": {
            "response": {
                "hcp": hcp,
                "type": interaction,
                "date": str(date.today()),
                "notes": input,
                "sentiment": sentiment,
                "followup": followup
            }
        }
    }