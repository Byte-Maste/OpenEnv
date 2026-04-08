import os
import sys
import traceback
from openai import OpenAI
from server.environment import CodeReviewEnv

# -------------------------------------------------------------------
# Configuration & Environment Variables
# -------------------------------------------------------------------
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# -------------------------------------------------------------------
# Main Inference Loop
# -------------------------------------------------------------------
def main():

    # Initialize OpenAI Client
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN
    )

    for diff in ["easy", "medium", "hard"]:
        env = CodeReviewEnv(difficulty=diff)
        
        # [START] Output
        print(f"[START] task={env.task_name} env={env.benchmark_name} model={MODEL_NAME}", flush=True)

        success = False
        
        try:
            obs = env.reset()
            done = False
            
            while not done:
                # Replace dummy action with actual LLM generation using the standard OpenAI client
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are a precise code reviewer. Your ONLY allowed outputs are: 'COMMENT <line_number> <text>', 'APPROVE', or 'REQUEST_CHANGES'."},
                        {"role": "user", "content": obs}
                    ],
                    max_tokens=100
                )
                action_str = response.choices[0].message.content.strip().replace("\n", " ")
                
                obs, reward_str, done, error = env.step(action_str)
                
                error_str = error if error else "null"
                done_str = "true" if done else "false"

                # [STEP] Output
                print(f"[STEP] step={env.steps_taken} action={action_str} reward={reward_str} done={done_str} error={error_str}", flush=True)

            success = True

        except Exception as e:
            error_msg = str(e).replace('\n', ' ')
            print(f"[STEP] step={env.steps_taken} action=error reward=0.00 done=true error={error_msg}", flush=True)
            success = False
        finally:
            # [END] Output MUST ALWAYS be emitted, even on exceptions
            success_str = "true" if success else "false"
            
            # For our Code Review Environment, the maximum optimal reward is 1.8 (0.8 comment + 1.0 request_changes)
            sum_rewards = sum(env.rewards) if env.rewards else 0.0
            score = max(0.0, min(sum_rewards / 1.8, 1.0))
            score_str = f"{score:.3f}"
            
            rewards_str = ",".join([f"{r:.2f}" for r in env.rewards])
            print(f"[END] success={success_str} steps={env.steps_taken} score={score_str} rewards={rewards_str}", flush=True)

if __name__ == "__main__":
    main()
