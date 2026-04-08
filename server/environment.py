import os
import sys
import json
from datasets import load_dataset

class CodeReviewEnv:
    def __init__(self, dataset_name="Krish-05/krish-bug-detect-fix", split="train", difficulty="medium"):
        self.benchmark_name = "krish_bug_detect_benchmark"
        self.dataset_name = dataset_name
        self.split = split
        self.difficulty = difficulty
        self.task_name = f"code_review_task_{difficulty}"
        
        self.steps_taken = 0
        self.rewards = []
        self.max_steps = 4 
        
        self.current_sample = None
        self.correct_comments = 0
        
        self._load_dataset()

    def _load_dataset(self):
        try:
            self.dataset = load_dataset(self.dataset_name, split=self.split)
            
            # Filter dataset by difficulty based on code length
            filtered_ds = []
            for item in self.dataset:
                num_lines = len(item['modified_code'].split('\n'))
                if self.difficulty == "easy" and num_lines <= 10:
                    filtered_ds.append(item)
                elif self.difficulty == "medium" and 10 < num_lines <= 30:
                    filtered_ds.append(item)
                elif self.difficulty == "hard" and num_lines > 30:
                    filtered_ds.append(item)
            
            self.filtered_datasets = filtered_ds if filtered_ds else list(self.dataset)
            self.current_idx = 0
        except Exception as e:
            print(f"Error loading dataset: {e}")
            self.dataset = None
            self.filtered_datasets = []

    def reset(self):
        self.steps_taken = 0
        self.rewards = []
        self.correct_comments = 0
        
        if not self.filtered_datasets:
            return "Error: Dataset not loaded or empty."
            
        self.current_sample = self.filtered_datasets[self.current_idx % len(self.filtered_datasets)]
        self.current_idx += 1
        
        buggy_code_raw = self.current_sample.get('modified_code', 'No code found')
        
        # Enumerate lines 1-indexed for the agent to review
        enumerated_lines = [f"{i+1} | {line}" for i, line in enumerate(buggy_code_raw.split('\n'))]
        buggy_code = '\n'.join(enumerated_lines)
        
        observation = f"""You are a strict code reviewer. Please review the following code identifying any bugs. Note that line numbers are provided on the left.
        
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
        true_bug_line = self.current_sample.get('number_of_line', -1)
        
        if action.startswith("COMMENT"):
            try:
                parts = action.split(' ', 2)
                line_str = parts[1]
                # Strip punctuation just in case
                for p in ['.', ':', ',']:
                    line_str = line_str.replace(p, '')
                    
                comment_line = int(line_str)
                
                # Deterministic Grader Check
                if comment_line == true_bug_line:
                    reward = 0.8  # High intermediate reward for locating the exact bug line
                    self.correct_comments += 1
                    obs = f"Valid bug identified on line {comment_line}. Will you APPROVE or REQUEST_CHANGES?"
                else:
                    reward = -0.2 # False positive penalty
                    obs = f"Line {comment_line} appears correct. False positive. Continue review or APPROVE/REQUEST_CHANGES."
            except Exception as e:
                reward = -0.1
                obs = f"Malformed format. Use COMMENT <line_number> <description>. Action parsed error: {e}"
        
        elif action.startswith("APPROVE"):
            if self.correct_comments == 0: # Missed the bug entirely
                reward = -1.0 
                obs = "You approved buggy code. deployment failed."
            else: # Found the bug but still approved?
                reward = -0.5 
                obs = "You found a bug but approved the PR anyway."
            done = True
            
        elif action.startswith("REQUEST_CHANGES"):
            if self.correct_comments > 0: # Perfectly identified the bug and rejected the PR
                reward = 1.0 
                obs = "Code review complete. Changes requested successfully."
            else: # Rejected without pointing out the correct bug
                reward = -0.5 
                obs = "You requested changes without accurately commenting on the bug line."
            done = True
            
        else:
            reward = -0.1
            obs = "Invalid action format. Use COMMENT <line_number>, APPROVE, or REQUEST_CHANGES."
               
        if self.steps_taken >= self.max_steps:
            done = True
            if not action.startswith("APPROVE") and not action.startswith("REQUEST_CHANGES"):
                obs = "Time limit exceeded. PR auto-closed."
            
        self.rewards.append(reward)
        formatted_reward = f"{reward:.2f}"
        
        return obs, formatted_reward, done, None
