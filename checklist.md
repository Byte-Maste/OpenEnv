# Submission Verification Checklist

Before submitting your project, double-check that all constraints and formats are satisfied.

### Required Files
- [ ] `inference.py` exists in the project root
- [ ] `requirements.txt` is updated and working
- [ ] `README.md` features clear instructions and your Demo URL
- [ ] Demo script/video (if applicable)

### Environment & Integrations
- [ ] `API_BASE_URL` reads properly and falls back to a default value
- [ ] `MODEL_NAME` reads properly and falls back to a default value
- [ ] `HF_TOKEN` is verified and successfully read
- [ ] The OpenAI Python Client SDK is strictly used for all LLM calls (no `requests` module directly) 

### Evaluation Constraints 
- [ ] Exact output format for `[START]` is used 
- [ ] Exact output format for `[STEP]` is used 
- [ ] Exact output format for `[END]` is used (always emitted)
- [ ] Rewards log formatted exactly to `2` decimal places (e.g. `1.00`, not `1.0` or `1`)
- [ ] Booleans printed strictly as lowercase `true` or `false` (e.g., `success=true`, `done=false`)

### Hugging Face Space & Operations
- [ ] Hugging Face Space is Public and deployed in a 'Running' state
- [ ] Unnecessary unused Spaces are disabled or turned off
- [ ] The Space/inference runs cleanly within `2 vCPU` and `8 GB RAM` limits
- [ ] The dockerization / environment does not rely on unpublished local-only dependencies

Good luck on Round 1!
