import os
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

df_all = pd.read_csv("result_all.csv")
df_kanto = pd.read_csv("result_kanto.csv")
df_kanto_groupby = df_kanto.groupby("station_id", as_index=False).mean()
df_timeserias_all = pd.read_csv("result_timeserias_all.csv")

# Or using s3 bucket.
# df = pd.read_csv("s3://your-bucket/result.csv")

MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN", "YOUR TOKEN")
# FIXME: input your mapbox token
# https://docs.mapbox.com/help/how-mapbox-works/access-tokens/

app = dash.Dash()
application = app.server

app.css.append_css({
    "external_url": "https://cdn.rawgit.com/plotly/dash-app-stylesheets/"
                    "2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css"})

app.layout = html.Div(children=[
    html.H1(children="温度マップ"),

    html.H2(children="全国の温度マップ"),

    html.Div([
        html.Div([
            dcc.Graph(id="temp-map",)
        ], className="eight columns"),

        html.Div([
            html.Button("平均気温", id="btn-avg", n_clicks_timestamp="0"),
            html.Button("最高気温", id="btn-high", n_clicks_timestamp="0"),
            html.Button("最低気温", id="btn-low", n_clicks_timestamp="0"),
            html.Div(id="container-button-temp-select")
        ], className="four columns"),

        html.Div([
            dcc.Graph(id="low-and-high",
                      figure={
                          "data": [
                              go.Scatter(
                                  x=df_all[df_all["prefecture"] == i]["low_temperature"],
                                  y=df_all[df_all["prefecture"] == i]["high_temperature"],
                                  text=df_all[df_all["prefecture"] == i]["prefecture"],
                                  mode="markers",
                                  opacity=0.7,
                                  marker={
                                      "size": 15,
                                      "line": {"width": 0.5, "color": "white"}
                                  },
                                  name=i
                              )for i in df_all["prefecture"].unique()
                          ],
                          "layout": go.Layout(
                              xaxis={"title": "最低気温"},
                              yaxis={"title": "最高気温"},
                              margin={"l": 50, "b": 50, "t": 10, "r": 10},
                              showlegend=False,
                              hovermode="closest")
                      })
        ], className="four columns")
    ], className="row"),

    html.H2(children="関東の温度マップ"),

    html.Div([
        html.Div([
            dcc.Graph(
                id="temp-kanto-map",
                figure={
                    "data": [
                        go.Scattermapbox(
                            lat=df_kanto_groupby[df_kanto_groupby["station_id"] == i]["latitude"],
                            lon=df_kanto_groupby[df_kanto_groupby["station_id"] == i]["longitude"],
                            mode="markers",
                            customdata=df_kanto_groupby[df_kanto_groupby["station_id"] == i]["station_id"],
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
                        ) for i in df_kanto_groupby["station_id"].unique()
                    ],
                    "layout":
                        go.Layout(
                            autosize=True,
                            showlegend=False,
                            hovermode="closest",
                            mapbox=dict(
                                accesstoken=MAPBOX_ACCESS_TOKEN,
                                bearing=0,
                                center=dict(
                                    lat=np.mean(df_kanto_groupby["latitude"]),
                                    lon=np.mean(df_kanto_groupby["longitude"])
                                ),
                                pitch=100,
                                zoom=8,
                            ),
                            height=600
                        )
                }
            )
        ], className="six columns"),
        html.Div([
            dcc.Graph(id="temp-timesearias")
        ],  className="six columns",)
    ], className="row"),
])


@app.callback(dash.dependencies.Output("temp-map", "figure"),
              [dash.dependencies.Input("btn-avg", "n_clicks_timestamp"),
               dash.dependencies.Input('btn-high', "n_clicks_timestamp"),
               dash.dependencies.Input("btn-low", "n_clicks_timestamp")])
def update_temp_map(btn1, btn2, btn3):
    if int(btn1) > int(btn2) and int(btn1) > int(btn3):
        index = "avg_temperature"
    elif int(btn2) > int(btn1) and int(btn2) > int(btn3):
        index = "high_temperature"
    elif int(btn3) > int(btn1) and int(btn3) > int(btn2):
        index = "low_temperature"
    else:
        index = "avg_temperature"
    return {
        "data": [
            go.Scattermapbox(
                lat=df_all[df_all["prefecture"] == i]["latitude"],
                lon=df_all[df_all["prefecture"] == i]["longitude"],
                mode="markers",
                marker=dict(
                    symbol="circle",
                    size=20,
                    opacity=0.8,
                    colorscale="RdBu",
                    cmin=df_all[index].min(),
                    color=df_all[df_all["prefecture"] == i][index],
                    cmax=df_all[index].max(),
                ),
                text=df_all[df_all["prefecture"] == i][index],
                name=str(df_all[df_all["prefecture"] == i]["prefecture"].values),
            ) for i in df_all["prefecture"].unique()
        ],
        "layout":
            go.Layout(
                autosize=True,
                showlegend=False,
                hovermode="closest",
                mapbox=dict(
                    accesstoken=MAPBOX_ACCESS_TOKEN,
                    bearing=0,
                    center=dict(
                        lat=np.mean(df_all["latitude"]),
                        lon=np.mean(df_all["longitude"])
                    ),
                    pitch=100,
                    zoom=6,
                ),
                height=700
            )
    }


@app.callback(dash.dependencies.Output("temp-timesearias", "figure"),
              [dash.dependencies.Input("temp-kanto-map", "hoverData")])
def update_temp_timeseries(hoverData):
    dff = df_kanto[df_kanto["station_id"] == hoverData["points"][0]["customdata"]]
    return {
        "data": [
            {"x": dff["datetime"], "y": dff["avg_temperature"],
             "type": "line", "name": "hover"},
            {"x": df_timeserias_all["datetime"], "y": df_timeserias_all["avg_temperature"],
             "type": "line", "name": "japan avg"}],
        "layout": {
            "title": hoverData["points"][0]["customdata"],
            "mode": "lines+markers"
        }
    }


if __name__ == "__main__":
    application.run(debug=True, port=8080)
