# **Weather Prediction System**

A fully containerized weather prediction application deployed on Kubernetes. It uses MLFlow for model tracking, Airflow for pipeline automation, Flask for API service, and Docker for containerization.

---

## **Table of Contents**

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Clone the Repository](#1-clone-the-repository)
  - [Build Docker Images](#2-build-docker-images)
  - [Start MLFlow Server](#3-start-mlflow-server)
  - [Deploy Airflow](#4-deploy-airflow)
  - [Kubernetes Deployment](#5-kubernetes-deployment)
- [Running the Application](#running-the-application)
- [Cleaning Up](#cleaning-up)
- [Future Enhancements](#future-enhancements)
- [License](#license)
- [Contributors](#contributors)
- [Architecture](#architecture)

---

## **Features**
- **Weather Prediction**: Predicts weather using trained ML models.
- **Containerized**: Fully containerized using Docker.
- **Kubernetes Deployment**: Easily scalable via Kubernetes.
- **Model Tracking**: MLFlow for experiment and model tracking.
- **Pipeline Orchestration**: Airflow for automating workflows.

---

## **Prerequisites**

Before you begin, ensure the following are installed on your system:
- **Docker**
- **Kubernetes** (Minikube or any Kubernetes cluster)
- **kubectl**
- **Python 3.8+**
- **Helm** (for Kubernetes package management)

---

## **Setup**

### 1. **Clone the Repository**
```bash

git clone https://github.com/bilalkhan980/Mlops_Project.git
cd Mlops_Project 
```

### 2. **Make a Virtual Environment**


```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. **Download Packages Required**


```bash
pip install dvc apache-airflow requests pandas scikit-learn
```

### 4. **Setup DVC**

```bash
dvc init
pip install 'dvc[gdrive]'
dvc remote add -d myremote gdrive://<GDRIVE_FOLDER_ID>
  
```

### 5. **Collect Data using collection_data.py and process data using data_preprocessing.py**


```bash
python3 data_collection.py
python3 data_preprocessing.py
  
```

### 6. **Track data using csv**


```bash
dvc add raw_data.csv
git add raw_data.csv raw_data.csv.dvc .gitignore
git commit -m "Add raw weather data"
dvc push

dvc add processed_data.csv
git add processed_data.csv processed_data.csv.dvc
git commit -m "Add processed weather data"
dvc push

  
```

### 7. **Setup And Initializa Airflow**


```bash
airflow db init
airflow webserver --port 8080
airflow scheduler
```

### 8. **Create a folder in airflow named dags and a file in it named weather_pipeline.py**


```bash
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from data_collection import fetch_weather_data
from data_preprocessing import preprocess_data

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 1, 1),
    "retries": 1,
}

with DAG(
    "weather_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
) as dag:

    collect_data = PythonOperator(
        task_id="collect_data",
        python_callable=fetch_weather_data,
    )

    preprocess = PythonOperator(
        task_id="preprocess_data",
        python_callable=preprocess_data,
    )

    collect_data >> preprocess

```



### 9. **Train model and track using DVC and airflow is used to train model continuously**


```bash
dvc add model.pkl
git add model.pkl model.pkl.dvc
git commit -m "Add trained model"
dvc push
```

### 10. **Setup MLflow to check the model training each time a version is created**


```bash
pip install mlflow
```
```bash
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 \
  --port 5000
```

### 11. **Run frontend**


```bash
cd my-app
npm run start
```


### 11. **Run Backend**


```bash

uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
```bash
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 \
  --port 5000
```


