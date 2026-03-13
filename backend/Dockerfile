FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Upgrade pip and install CPU-only PyTorch + dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Add local bin to PATH (for --user installs)
ENV PATH=/root/.local/bin:$PATH

# Expose the port your app will run on
EXPOSE 8000

# Run your FastAPI app
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]