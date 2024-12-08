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

Once the repository is cloned, navigate to the project directory and build the Docker images using Docker Compose:

```bash
python3 -m venv venv
source venv/bin/activate
```


