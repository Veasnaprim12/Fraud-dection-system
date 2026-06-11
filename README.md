# 🛡️ Fraud Detection System Using Deep Learning & PySpark

## 📌 Overview
This project is a **Fraud Detection System** built using **Deep Learning and Distributed Computing (PySpark)**.  
It detects fraudulent financial transactions using the **PaySim dataset (6.3 million records)** and provides a **web interface using Streamlit** for real-time prediction.

---

## 🎯 Objectives
- Detect fraudulent transactions using Deep Learning
- Process large-scale data using PySpark
- Build an interactive web application
- Demonstrate Big Data + AI integration

---

## 📊 Dataset

### PaySim Financial Dataset
- **Rows:** 6,362,604
- **Format:** CSV
- **Target:** `isFraud`

### Features
- step
- type
- amount
- oldbalanceOrg
- newbalanceOrig
- oldbalanceDest
- newbalanceDest
- isFraud
- isFlaggedFraud

---

## ⚙️ Technologies Used

### 🔹 Big Data / Distributed Computing
- PySpark

### 🔹 Deep Learning
- TensorFlow / Keras

### 🔹 Data Visualization
- Matplotlib
- Seaborn

### 🔹 Web App
- Streamlit

---

## 🏗️ System Architecture

```text
PaySim Dataset (6.3M rows)
        ↓
      PySpark
        ↓
Data Preprocessing & Feature Engineering
        ↓
Deep Learning Model (DNN)
        ↓
Fraud Prediction
        ↓
Streamlit Web App