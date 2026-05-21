FROM python:3.10-bookworm

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install -r requirements.txt
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir openai-whisper


COPY main.py .
COPY metadata.py .
COPY dim_category.py .
COPY dim_channel.py .
COPY dim_video.py .
COPY engagement.py .
COPY scaler.pkl .
COPY kmeans_model.pkl .
COPY classifier.py .
COPY model.pkl .
COPY vectorizer.pkl .
COPY transcript.py .
COPY dim_time.py .


CMD python3 main.py

#& jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root
