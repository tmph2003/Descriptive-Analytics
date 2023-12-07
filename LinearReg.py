from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
import time

def main():
    df = pd.read_csv("data/result/pre-process-data.csv")

    X = df[['PM2.5', 'PM10']]
    Y = df['AQI index']

    # Compare the dependence of variables
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
    for i, column in enumerate(X.columns):
        axes[i].scatter(X[column], Y, label=f'{column} vs AQI index')

        model = LinearRegression()
        model.fit(X[[column]], Y)
        axes[i].plot(X[column], model.predict(X[[column]]), color='red', linestyle='--', label='Linear Regression')

        axes[i].set_xlabel(column)
        axes[i].set_ylabel('AQI index')
        axes[i].legend()

    plt.tight_layout()
    plt.show()

    # Multivariable regression model
    model = LinearRegression()
    model.fit(X, Y)
    r2 = model.score(X, Y)
    for i, column in enumerate(X.columns):
        print("Coefficient", f'{column}: {model.coef_[i]}')
    print("Intercept:", model.intercept_)
    print("R2-square: ", r2)

    pm25_new = float(input("Enter PM2.5: "))
    pm10_new = float(input("Enter PM10 : "))
    predicted_aqi = model.predict([[pm25_new, pm10_new]])[0]
    print("PM2.5 =", pm25_new, "; PM10 =", pm10_new, "\n=> AQI index =", round(predicted_aqi, 2))
    
if __name__ == "main":
    main()