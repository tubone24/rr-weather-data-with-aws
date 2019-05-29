import pandas as pd
from fbprophet import Prophet
from matplotlib import pyplot as plt


def main():
    df = pd.read_csv("result_timeserias_all.csv")

    df = df.rename(columns={"datetime": "ds", "avg_temperature": "y"})

    model = Prophet(daily_seasonality=False)
    model.add_seasonality(name="yearly", period=365, fourier_order=5)
    model.fit(df)

    future_df = model.make_future_dataframe(720)

    forecast_df = model.predict(future_df)

    model.plot_components(forecast_df)

    # model.plot(forecast_df)
    plt.show()


if __name__ == '__main__':
    main()