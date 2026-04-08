import os
import sys
import json
from datasets import load_dataset

class CodeReviewEnv:
    def __init__(self, dataset_name="Krish-05/krish-bug-detect-fix", split="train"):
        self.task_name = "code_review_task"
        self.benchmark_name = "krish_bug_detect_benchmark"
        self.dataset_name = dataset_name
        self.split = split
        self.steps_taken = 0
        self.rewards = []
        self.current_sample = None
        self.max_steps = 5
        self._load_dataset()

    def _load_dataset(self):
        try:
            self.dataset = load_dataset(self.dataset_name, split=self.split)
            self.current_idx = 0
        except Exception as e:
            print(f"Error loading dataset: {e}")
            self.dataset = None

    def reset(self):
        self.steps_taken = 0
        self.rewards = []
        
        if self.dataset is None:
            return "Error: Dataset not loaded."
            
        self.current_sample = self.dataset[self.current_idx]
        self.current_idx = (self.current_idx + 1) % len(self.dataset)
        
        # NOTE: Adjusting these keys ('instruction', 'input', 'output' or similar) 
        # depending on the actual schema of Krish-05/krish-bug-detect-fix
        buggy_code = self.current_sample.get('buggy_code', self.current_sample.get('input', 'No code found'))
        
        observation = f"""You are a senior code reviewer. Please review the following code:
        
{buggy_code}

Available actions:
1. COMMENT <line_number> <issue_description>
2. APPROVE
3. REQUEST_CHANGES
"""
        return observation

    def step(self, action):
        self.steps_taken += 1
        done = False
        reward = 0.0
        
        action = action.strip()
        
        if action.startswith("COMMENT"):
            # Acknowledge comment but typically delay final reward until the end
            reward = 0.5  # Intermediate reward for finding something to comment on
            obs = "Comment recorded. Any other issues, or are you ready to APPROVE / REQUEST_CHANGES?"
        
        elif action == "APPROVE":
            # If the code had bugs but the agent approved, negative reward. Let's assume there's always a bug in this dataset.
            reward = -1.0
            done = True
            obs = "You approved flawed code."
            
        elif action == "REQUEST_CHANGES":
            # Good job, they rejected buggy code
            reward = 1.0
            done = True
            obs = "Changes requested successfully."
            
        else:
            reward = -0.1
            obs = "Invalid action format. Use COMMENT <line> <text>, APPROVE, or REQUEST_CHANGES."
            if self.steps_taken >= self.max_steps:
               done = True
               
        if self.steps_taken >= self.max_steps:
            done = True
            
        self.rewards.append(reward)
        formatted_reward = f"{reward:.2f}"
        
        return obs, formatted_reward, done, None

