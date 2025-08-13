import json
import sys
from orchestrator import orchestrate

def main():
    # Load pipeline config
    with open("pipeline_config.json") as f:
        config = json.load(f)

    # Get input JSON from CLI argument or fallback to sample input
    if len(sys.argv) > 1:
        try:
            input_json = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            print("Invalid JSON input. Please provide valid JSON as first argument.")
            sys.exit(1)
    else:
        # Default sample input
        input_json = {
            "user_id": "abc123",
            "platform": "instagram",
            "message_text": "Did you finalize the pitch deck?",
            "timestamp": "2025-08-05T13:00:00Z"
        }

    # Call orchestrator
    output = orchestrate(input_json, config)

    # Pretty print output
    print("Final orchestrator output:")
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
