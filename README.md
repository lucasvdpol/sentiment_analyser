YouTube Sentiment & Analytics Pipeline
Project Overview

This project involved developing an automated data pipeline designed to ingest, process, and analyze YouTube video data. The system was engineered to run autonomously on a recurring schedule, building a longitudinal database of video performance metrics and audience sentiment over time.
Objective

The goal was to move from raw data ingestion to actionable insights by building a robust ETL (Extract, Transform, Load) pipeline that provides a daily snapshot of video performance and viewer sentiment.
The Pipeline Workflow

The project was executed in four distinct phases:
-Data Ingestion: Developed a service to communicate with the YouTube API. This component fetches metadata (views, likes, comments, etc.) for target videos and           stores them in a relational database.
-Transcription: Integrated OpenAI Whisper to perform automated speech-to-text conversion on video content.
-Sentiment Analysis: Built and trained a classification model to analyze the transcripts, determining the underlying sentiment of the video content.
-Automation & Integration: Encapsulated the entire pipeline within Docker containers. The system was configured to run as a nightly job, ensuring the database           maintained an accurate historical record of daily metric changes.

Architecture

The system is built to be scalable and maintainable:
    Database: PostgreSQL (used for storing historical metadata and analytical results).
    Processing: Python-based ETL scripts for data transformation.
    Infrastructure: Docker & Docker Compose for containerized deployment.
    Automation: Orchestrated via cron to ensure daily execution.
    Visualization: All processed data was aggregated and visualized through a dedicated dashboard (providing clear insights into sentiment trends over time).

Status

Note: This project was developed as part of an educational curriculum. While the production environment on the school server is currently inactive, the architectural design is modular and ready for deployment on cloud infrastructure (e.g., AWS, GCP, or Azure).
