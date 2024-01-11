# Burger Sales Forecast using LSTM and AWS Sagemaker

## Business Overview

The Weather is a significant factor influencing product sales, especially in retail stores. This project focuses on understanding the impact of various weather conditions on burger sales in a retail chain with stores across ten regions. The primary objective is to forecast burger sales based on historical data. The project includes deploying the model using AWS Sagemaker.

---

## Aim

1. Fetch data from SQL server hosted on Amazon RDS to Python.
2. Analyze the influence of weather on burger sales.
3. Build LSTM model on AWS Sagemaker.
4. Forecast next day's sales based on historical data.
5. Deploy the model using AWS Sagemaker.

---

## Data Description
- Data period: 1/1/2014 to 15/9/2020.
- Total rows: 24,500, Columns: 8.
- Data stored in MySQL server hosted on Amazon RDS.

---

## Tech Stack
- **Language:** `Python`
- **Libraries:** `pandas`, `numpy`, `tensorflow`, `boto3`, `pymysql`, `matplotlib`, `sklearn`, `tarfile`, `keras`, `lightgbm`
- **Platform:** `AWS Sagemaker`, `AWS S3`

---

## Approach
1. **Loading Data:**
   - Using pymysql library to fetch data from the MySQL server.
2. **Exploratory Data Analysis:**
   - Plotting date vs sales graph based on regions.
   - Autocorrelation and partial correlation plot.
   - Plotting average, maximum, and minimum of features.
   - Scatterplot and histograms of the features.
3. **Data Preprocessing:**
4. **Windowing the Data:**
5. **Train-Validation Split:**
6. **Data Rescaling using QuantileTransformer:**
7. **Building Baseline Model (lightgbm) and Feature Importance:**
8. **Building LSTM Model:**
9. **Predictions for One Day into Future:**
10. **Creating an Endpoint and Deploying the Model:**

---

## Code Overview

   1. `Burger_data.csv`: Data used in the project.
   2. `burger_stores.ipynb`: Main file for training and deploying the model using Sagemaker.
   3. `Config.yml`: Store DB connection credentials.
   4. `empty_train.py`: Empty file created during model deployment on Sagemaker.
   5. `Predict_from_endpoint.ipynb`: File for predictions using the endpoint.
   6. `Requirements.txt`: File with required libraries and versions.
   7. `utils.py`: File containing functions called in `burger_stores.ipynb`.

  ---