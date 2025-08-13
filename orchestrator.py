import json
import os
import time
from datetime import datetime
from summarizer_call import call_summarizer
from cognitive_engine_call import call_cognitive_engine
from action_responder_call import call_action_responder
from insight_dashboard_call import call_insight_dashboard
from rl_feedback_call import call_rl_feedback

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def save_log(stage, data):
    filename = os.path.join(LOG_DIR, f"log_{stage}.json")
    with open(filename, "a") as f:
        f.write(json.dumps({"timestamp": datetime.utcnow().isoformat(), **data}) + "\n")

def load_pipeline_config():
    with open("pipeline_config.json") as f:
        return json.load(f)

def orchestrate(message, config=None):
    if config is None:
        config = load_pipeline_config()

    state = {}
    current_data = {**message}  # copy input

    def call_with_retry(func, *args, stage_name):
        retries = config.get("retry_count", 1)
        for attempt in range(retries + 1):
            try:
                result = func(*args)
                save_log(stage_name, result)
                return result
            except Exception as e:
                print(f"Error in {stage_name}, attempt {attempt + 1}: {e}")
                if attempt == retries:
                    print(f"Skipping {stage_name} after {retries+1} attempts")
                    return {}
                time.sleep(1)

    # Stage 1: Summarizer
    if config.get("summarizer", True):
        out = call_with_retry(call_summarizer, current_data["message_text"], current_data["user_id"], stage_name="summaries")
        current_data.update(out)
        state["summary"] = out.get("summary", "")

    # Stage 2: Cognitive Engine
    if config.get("cognitive_engine", True):
        out = call_with_retry(call_cognitive_engine, current_data, stage_name="tasks")
        current_data.update(out)
        state["type"] = out.get("type", "")
        state["task_type"] = out.get("task_type", "")

    # Stage 3: Action Responder
    if config.get("action_responder", True):
        out = call_with_retry(call_action_responder, current_data, stage_name="actions")
        current_data.update(out)
        state["scheduled_action"] = out.get("scheduled_action", "")

    # Stage 4: Insight Dashboard
    if config.get("insight_dashboard", True):
        call_with_retry(call_insight_dashboard, current_data, stage_name="logs")

    # Stage 5: RL Feedback
    if config.get("rl_feedback", True):
        out = call_with_retry(call_rl_feedback, current_data, stage_name="feedback")
        state["RL_score"] = out.get("RL_score", "")

    state["timestamp"] = datetime.utcnow().isoformat()

    # Save final output
    with open(os.path.join(LOG_DIR, "final_output.json"), "a") as f:
        f.write(json.dumps(state) + "\n")

    return state

if __name__ == "__main__":
    import sys
    config = load_pipeline_config()
    if len(sys.argv) > 1:
        input_json = json.loads(sys.argv[1])
    else:
        input_json = {
            "user_id": "abc123",
            "platform": "instagram",
            "message_text": "Did you finalize the pitch deck?",
            "timestamp": "2025-08-05T13:00:00Z"
        }
    output = orchestrate(input_json, config)
    print(json.dumps(output, indent=2))
