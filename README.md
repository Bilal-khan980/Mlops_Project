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



