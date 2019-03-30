import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

df = pd.read_csv("result.csv")
# Or using s3 bucket.
# df = pd.read_csv("s3://your-bucket/result.csv")

mapbox_access_token = "your token"
# FIXME: input your mapbox token
# https://docs.mapbox.com/help/how-mapbox-works/access-tokens/

app = dash.Dash()
application = app.server

app.layout = html.Div(children=[
    html.H1(children="温度マップ"),

    dcc.Graph(
        id="temp-map",
        figure={
            "data": [
                go.Scattermapbox(
                    lat=df[df["station_id"] == i]["latitude"],
                    lon=df[df["station_id"] == i]["longitude"],
                    mode="markers",
                    marker=dict(
                        symbol="circle",
                        size=16,
                        opacity=0.8,
                        colorscale="RdBu",
                        cmin=df["avg_temperature"].min(),
                        color=df[df["station_id"] == i]["avg_temperature"],
                        cmax=df["avg_temperature"].max(),
                    ),
                    text=df[df["station_id"] == i]["avg_temperature"],
                    name=str(df[df["station_id"] == i]["first_name"].values),
                ) for i in df["station_id"].unique()
            ],
            'layout':
                go.Layout(
                    autosize=True,
                    hovermode="closest",
                    mapbox=dict(
                        accesstoken=mapbox_access_token,
                        bearing=0,
                        center=dict(
                            lat=np.mean(df["latitude"]),
                            lon=np.mean(df["longitude"])
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
