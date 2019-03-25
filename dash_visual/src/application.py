import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

df = pd.read_csv("result.csv", index_col=0)
# Or using s3 bucket.
# df = pd.read_csv("s3://your-bucket/result.csv", index_col=0)

max_temp = df.groupby("station_id", as_index=False).max()

mapbox_access_token = "Your Access Token"
app = dash.Dash()
application = app.server

app.layout = html.Div(children=[
    html.H1(children="温度マップ"),

    dcc.Graph(
        id="temp-map",
        figure={
            "data": [
                go.Scattermapbox(
                    lat=max_temp[max_temp["station_id"] == i]["latitude"],
                    lon=max_temp[max_temp["station_id"] == i]["longitude"],
                    mode="markers",
                    marker=dict(
                        symbol="circle",
                        size=16,
                        opacity=0.8,
                        colorscale="RdBu",
                        cmin=max_temp["avg_temperature"].min(),
                        color=max_temp[max_temp["station_id"] == i]["avg_temperature"],
                        cmax=max_temp["avg_temperature"].max(),
                    ),
                    text=max_temp[max_temp["station_id"] == i]["avg_temperature"],
                    name=str(max_temp[max_temp["station_id"] == i]["first_name"].values),
                ) for i in max_temp["station_id"].unique()
            ],
            'layout':
                go.Layout(
                    autosize=True,
                    hovermode="closest",
                    mapbox=dict(
                        accesstoken=mapbox_access_token,
                        bearing=0,
                        center=dict(
                            lat=np.mean(max_temp["latitude"]),
                            lon=np.mean(max_temp["longitude"])
                        ),
                        pitch=100,
                        zoom=6,
                    ),
                    height=900
                )
        }
    )

])

if __name__ == "__main__":
    application.run(debug=True, port=8080)
