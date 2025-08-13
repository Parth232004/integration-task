def call_rl_feedback(input_data):
    """
    Dummy RL feedback learner: returns a feedback score based on action scheduled.
    """
    scheduled_action = input_data.get("scheduled_action", "")
    if scheduled_action and "Notify" in scheduled_action:
        RL_score = "+1"
    else:
        RL_score = "0"

    return {"RL_score": RL_score}
