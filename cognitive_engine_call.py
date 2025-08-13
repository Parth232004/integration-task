def call_cognitive_engine(input_data):
    """
    Dummy cognitive engine: decides message type and task_type based on summary.
    """
    summary = input_data.get("summary", "").lower()
    # Simple heuristic
    if "reminder" in summary or "notify" in summary:
        task_type = "reminder"
        type_ = "follow-up"
    else:
        task_type = "general"
        type_ = "info"

    return {"type": type_, "task_type": task_type}
