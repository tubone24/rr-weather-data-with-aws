import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

app = dash.Dash()

result = pd.read_csv("result.csv")

minokamo_result = result[result.path == "s3://athena-origin-data20190317/"
                                        "weather-data/gifu__minokamo-kana__minocamo.csv"]

nagoya_result = result[result.path == "s3://athena-origin-data20190317/"
                                      "weather-data/aichi__nagoya-kana__nagoya.csv"]

tazawako_result = result[result.path == "s3://athena-origin-data20190317/"
                                        "weather-data/akita__tazawako-kana__tazawaco.csv"]

seto_result = result[result.path == "s3://athena-origin-data20190317/"
                                    "weather-data/ehime__seto-kana__NONE.csv"]


app.layout = html.Div(children=[
    html.H1(children="気象データ"),

    html.Div(children="全国の気象データです"),

    dcc.Graph(
        id="temp-graph",
        figure={
            "data": [
                {"x": minokamo_result["datetime"],
                 "y": minokamo_result["avg_temperature"],
                 "type": "line",
                 "name": "minokamo"},

                {"x": nagoya_result["datetime"],
                 "y": nagoya_result["avg_temperature"],
                 "type": "line",
                 "name": "nagoya"},

                {"x": tazawako_result["datetime"],
                 "y": tazawako_result["avg_temperature"],
                 "type": "line",
                 "name": "tazawako"},

                {"x": seto_result["datetime"],
                 "y": seto_result["avg_temperature"],
                 "type": "line",
                 "name": "seto"},

            ],
            "layout": {
                "title": "平均気温推移"
            }
        }
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
