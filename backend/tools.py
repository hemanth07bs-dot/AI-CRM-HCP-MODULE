from datetime import datetime

# Tool 1: Log Interaction
def log_interaction_tool(data):
    return {
        "status": "logged",
        "hcp": data.get("hcp_name"),
        "time": str(datetime.now())
    }

# Tool 2: Edit Interaction
def edit_interaction_tool(data):
    return {
        "status": "edited",
        "hcp": data.get("hcp_name")
    }

# Tool 3: Summarize Interaction
def summarize_interaction_tool(text):
    return {
        "summary": f"Summary of interaction: {text}"
    }

# Tool 4: Suggest Followup
def suggest_followup_tool(text):
    return {
        "followup": "Schedule follow-up meeting next week"
    }

# Tool 5: Fetch HCP History
def get_hcp_history_tool(name):
    return {
        "hcp": name,
        "history": ["Previous meeting", "Product discussion"]
    }