import pandas as pd

import plotly.express as px
import json

from datetime import datetime
from dash_bootstrap_templates import load_figure_template

load_figure_template("slate")

x = []
y = []
z = []

f = open("../../data/losses.json")
losses = json.load(f)
f.close()

f = open("../../data/meta.json")
metaData = json.load(f)
lastUpdateDate = metaData["last_update_date"]
f.close()

for loss in losses:
    if loss["model_match"] != "No Match Found" and loss["date"]:
        date = datetime.strptime(loss["date"], "%d %b %Y")
        x.append(date)
        y.append(int(loss["t_value"]))
        z.append(loss["name"])

lastAverage = 0
for i in range(len(y) -50 , len(y)):
    lastAverage += y[i]
lastAverage = lastAverage/50

df = pd.DataFrame({'Date': x, 'T': y, 'Name': z})
title = f"Average Russian Tank is a T-{df.head(50)['T'].mean()}<br><sup>Updated: {lastUpdateDate}</sup>"


fig = px.scatter(df, x="Date", y="T", trendline="rolling", trendline_options=dict(window=50), opacity=0.15, template = "slate", title=title, hover_data="Name")
fig.update_layout(xaxis_title="", yaxis_title="")

with open("../../charts/average.html", 'w') as f:
    f.write(fig.to_html(include_plotlyjs='cdn'))
