# 📞 Phonebook App - Cloud Computing Project

A simple Phonebook web application built with Flask and MongoDB, containerized with Docker, and deployed on Kubernetes using Minikube. The project also includes CI/CD with GitHub Actions.

---

## 📦 Features

- User registration and login with session-based authentication
- Add, view, and delete phonebook contacts per user
- RESTful API for managing contacts
- Responsive UI with Bootstrap 5
- Containerized with Docker
- Kubernetes deployment (with scaling & monitoring)
- GitHub Actions CI/CD pipeline

---

## 🛠️ Tech Stack

- Python (Flask)
- MongoDB
- Docker
- Kubernetes (Minikube)
- GitHub Actions
- HTML + CSS + Bootstrap 5

---

## 🧱 Project Structure


phonebook/
├── app.py # Flask backend

├── requirements.txt

├── Dockerfile

├── templates/

│ ├── login.html

│ ├── register.html

│ └── dashboard.html

├── static/

│ └── style.css

├── deployment.yaml # Kubernetes deployment for app

├── service.yaml # Kubernetes service for app

├── mongo-deployment.yaml # MongoDB deployment

├── mongo-service.yaml # MongoDB service

└── .github/

└── workflows/

└── deploy.yml # GitHub Actions CI/CD




---

## 🚀 Deployment Steps

### 1. Build & Push Docker Image

```bash
docker build -t sinazeynali/phonebook-app .
docker push sinazeynali/phonebook-app
```bash


### 2. Start Minikube (Docker driver recommended)

```bash
minikube start --driver=docker
```bash


### 3. Deploy MongoDB and App to Kubernetes

```bash
kubectl apply -f mongo-deployment.yaml
kubectl apply -f mongo-service.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```bash


### 4. Access the App

```bash
minikube service phonebook-service
```bash


## ⚖️ Scaling & Monitoring

### Manual scaling:

```bash
kubectl scale deployment phonebook-app --replicas=3
```bash


### Autoscaling (HPA):

```bash
kubectl autoscale deployment phonebook-app --cpu-percent=50 --min=2 --max=5
```bash


Liveness & Readiness probes added to deployment.yaml using a /health endpoint.

## ⚙️ GitHub Actions CI/CD

### 1. On push to main:
Docker image is built and pushed to Docker Hub.
Uses secrets: DOCKER_USERNAME and DOCKER_PASSWORD

### 2. File path:
.github/workflows/deploy.yml


## 🔗 Demo Repository
📁 GitHub Repo: https://github.com/sinazb/phonebook

## 🧩 Challenges Faced
ImagePullBackOff due to missing push or registry access

Required use of --driver=docker with Minikube

YAML formatting and pod health probe tuning

## 🧑‍💻 Developed By
Sina Zeynali
Cloud Computing - Spring 1404
