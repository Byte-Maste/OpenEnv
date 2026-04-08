# OpenEnv Environment Submission

This repository contains the submission for the **Meta PyTorch OpenEnv Hackathon — Round 1**.

## Overview
Implement an RL-style environment that follows the OpenEnv framework by Meta and Hugging Face. The environment exposes tasks, actions, step execution, and reward scoring.

**Domain:** Custom Domain (e.g. Email triage, Scheduling, Code Review)

## Project Structure
```
openEnv/
├── inference.py     # Main execution script emitting required [START], [STEP], [END] logs.
├── requirements.txt # Project dependencies
├── README.md        # This file
├── spec.md          # Full Hackathon Specification
└── checklist.md     # Submission Verification Checklist
```

## Setup & Execution

### Prerequisites
- Python 3.9+
- OpenAI Python client (`openai>=1.0.0`)

### Installation
```bash
pip install -r requirements.txt
```

### Environment Variables
For inference script to run, the following environment variables are supported/required:
- `HF_TOKEN`: Required. Hugging Face Access Token.
- `API_BASE_URL`: Base URL for OpenAI client (Default: `https://api.openai.com/v1`)
- `MODEL_NAME`: The Language Model name (Default: `gpt-3.5-turbo`)
- `OPENAI_API_KEY`: API Key if hitting OpenAI directly or external OpenAI-compatible APIs.

```bash
export HF_TOKEN="your_hf_token"
export OPENAI_API_KEY="your_api_key"
```

### Run
Ensure you output exactly to `stdout` for the metrics collection:

```bash
python inference.py
```

### Output Formatting
The script outputs logs specifically formatted for the autograder:
- `[START] task=xyz env=abc model=mymodel`
- `[STEP] step=1 action=abc reward=0.00 done=false error=null`
- `[END] success=true steps=5 rewards=0.00,1.00`

## Hugging Face Spaces Deployment
*URL: `https://huggingface.co/spaces/YOUR_USER_ID/YOUR_SPACE_NAME`*

This project is configured to run efficiently on Hugging Face Spaces under the **2 vCPU & 8 GB RAM** limitation constraint, with valid docker-based build processes. 
