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
def run_agent(input: str, data=None):

    if "summary" in input:
        return summarize_interaction_tool(input)

    if "follow" in input:
        return suggest_followup_tool(input)

    if "history" in input:
        return {
            "history": data
        }

    return {
        "message": "Agent working",
        "input": input
    }
from langgraph.graph import StateGraph, END


def run_agent(input: str, data=None):

    def router(state):
        text = input.lower()

        if "history" in text:
            return "history"
        elif "summary" in text:
            return "summary"
        elif "follow" in text:
            return "followup"
        elif "edit" in text:
            return "edit"
        else:
            return "log"

    def log_node(state):
        return {"response": log_interaction_tool({"hcp_name": input})}

    def history_node(state):
        return {"response": get_hcp_history_tool(input)}

    def summary_node(state):
        return {"response": summarize_interaction_tool(input)}

    def followup_node(state):
        return {"response": suggest_followup_tool(input)}

    def edit_node(state):
        return {"response": edit_interaction_tool({"hcp_name": input})}

    graph = StateGraph(dict)

    graph.add_node("router", router)
    graph.add_node("log", log_node)
    graph.add_node("history", history_node)
    graph.add_node("summary", summary_node)
    graph.add_node("followup", followup_node)
    graph.add_node("edit", edit_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        router,
        {
            "log": "log",
            "history": "history",
            "summary": "summary",
            "followup": "followup",
            "edit": "edit",
        },
    )

    graph.add_edge("log", END)
    graph.add_edge("history", END)
    graph.add_edge("summary", END)
    graph.add_edge("followup", END)
    graph.add_edge("edit", END)

    app = graph.compile()

    return app.invoke(input)
                        

        

