FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir torch==2.10.0 -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

CMD ["uvicorn","src.api:app","--host","0.0.0.0","--port","8000"]