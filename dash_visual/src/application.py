import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

df_all = pd.read_csv("result_all.csv")
df_kanto = pd.read_csv("result_kanto.csv")
df_kanto_groupby = df_kanto.groupby("station_id", as_index=False).mean()

# Or using s3 bucket.
# df = pd.read_csv("s3://your-bucket/result.csv")

mapbox_access_token = "pk.eyJ1IjoidHVib25lIiwiYSI6ImNqdG85aDhuZTBramE0NG4ybGFxNWRsM3IifQ.2RyoyqPBvjrBHRb8Hk1ciQ"
# FIXME: input your mapbox token
# https://docs.mapbox.com/help/how-mapbox-works/access-tokens/

app = dash.Dash()
application = app.server

app.layout = html.Div(children=[
    html.H1(children="全国の温度マップ"),

    dcc.Graph(
        id="temp-map",
        figure={
            "data": [
                go.Scattermapbox(
                    lat=df_all[df_all["prefecture"] == i]["latitude"],
                    lon=df_all[df_all["prefecture"] == i]["longitude"],
                    mode="markers",
                    marker=dict(
                        symbol="circle",
                        size=16,
                        opacity=0.8,
                        colorscale="RdBu",
                        cmin=df_all["avg_temperature"].min(),
                        color=df_all[df_all["prefecture"] == i]["avg_temperature"],
                        cmax=df_all["avg_temperature"].max(),
                    ),
                    text=df_all[df_all["prefecture"] == i]["avg_temperature"],
                    name=str(df_all[df_all["prefecture"] == i]["prefecture"].values),
                ) for i in df_all["prefecture"].unique()
            ],
            'layout':
                go.Layout(
                    autosize=True,
                    hovermode="closest",
                    mapbox=dict(
                        accesstoken=mapbox_access_token,
                        bearing=0,
                        center=dict(
                            lat=np.mean(df_all["latitude"]),
                            lon=np.mean(df_all["longitude"])
                        ),
                        pitch=100,
                        zoom=6,
                    ),
                    height=900
                )
        }
    ),
    dcc.Graph(
        id="tempkanto-map",
        figure={
            "data": [
                go.Scattermapbox(
                    lat=df_kanto_groupby[df_kanto_groupby["station_id"] == i]["latitude"],
                    lon=df_kanto_groupby[df_kanto_groupby["station_id"] == i]["longitude"],
                    mode="markers",
                    marker=dict(
                        symbol="circle",
                        size=16,
                        opacity=0.8,
                        colorscale="RdBu",
                        cmin=df_kanto_groupby["avg_temperature"].min(),
                        color=df_kanto_groupby[df_kanto_groupby["station_id"] == i]["avg_temperature"],
                        cmax=df_kanto_groupby["avg_temperature"].max(),
                    ),
                    text=df_kanto_groupby[df_kanto_groupby["station_id"] == i]["avg_temperature"],
                    name=str(df_kanto_groupby[df_kanto_groupby["station_id"] == i]["station_id"].values),
                ) for i in df_kanto_groupby["station_id"].unique()
            ],
            'layout':
                go.Layout(
                    autosize=True,
                    hovermode="closest",
                    mapbox=dict(
                        accesstoken=mapbox_access_token,
                        bearing=0,
                        center=dict(
                            lat=np.mean(df_kanto_groupby["latitude"]),
                            lon=np.mean(df_kanto_groupby["longitude"])
                        ),
                        pitch=100,
                        zoom=8,
                    ),
                    height=900
                )
        }
    )
])



if __name__ == "__main__":
    application.run(debug=True, port=8080)
