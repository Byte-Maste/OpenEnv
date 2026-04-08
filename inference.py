import os
import sys
import traceback
from openai import OpenAI
from code_review_env import CodeReviewEnv

# -------------------------------------------------------------------
# Configuration & Environment Variables
# -------------------------------------------------------------------
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN")

def validate_environment():
    """Ensure required environment variables like HF_TOKEN are present."""
    if not HF_TOKEN:
        print("[STEP] step=0 action=init reward=0.00 done=true error=HF_TOKEN_missing")
        print("[END] success=false steps=0 rewards=")
        sys.exit(1)

# -------------------------------------------------------------------
# Main Inference Loop
# -------------------------------------------------------------------
def main():
    validate_environment()

    # Initialize OpenAI Client (per requirements, use OpenAI Python client)
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=os.getenv("OPENAI_API_KEY", "dummy_if_not_needed_for_custom_endpoint")
    )

    env = CodeReviewEnv()
    
    # [START] Output
    print(f"[START] task={env.task_name} env={env.benchmark_name} model={MODEL_NAME}")

    success = False
    
    try:
        obs = env.reset()
        done = False
        
        while not done:
            # Replace dummy action with actual LLM generation using the standard OpenAI client
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a precise code reviewer. Your ONLY allowed outputs are: 'COMMENT <line> <text>', 'APPROVE', or 'REQUEST_CHANGES'."},
                    {"role": "user", "content": obs}
                ],
                max_tokens=100
            )
            action_str = response.choices[0].message.content.strip()
            
            obs, reward_str, done, error = env.step(action_str)
            
            error_str = error if error else "null"
            done_str = "true" if done else "false"

            # [STEP] Output
            print(f"[STEP] step={env.steps_taken} action={action_str} reward={reward_str} done={done_str} error={error_str}")

        success = True

    except Exception as e:
        error_msg = str(e).replace('\n', ' ')
        print(f"[STEP] step={env.steps_taken} action=error reward=0.00 done=true error={error_msg}")
        success = False
    finally:
        # [END] Output MUST ALWAYS be emitted, even on exceptions
        success_str = "true" if success else "false"
        rewards_str = ",".join([f"{r:.2f}" for r in env.rewards])
        print(f"[END] success={success_str} steps={env.steps_taken} rewards={rewards_str}")

if __name__ == "__main__":
    main()
