# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables to avoid writing .pyc files and buffer stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Hugging Face Spaces requires running as a non-root user
RUN useradd -m -u 1000 user
USER user

# Set up the home directory and path
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory inside the container
WORKDIR $HOME/app

# Copy the current directory contents into the container and set ownership
COPY --chown=user:user . $HOME/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Command to run the Gradio UI
CMD ["python", "app.py"]
