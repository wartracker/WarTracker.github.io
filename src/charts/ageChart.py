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
title = f"Rolling Average Model Age Of Lost Russian Tanks        Updated: " + lastUpdateDate
f.close()

for loss in losses:
    if loss["model_match"] != "No Match Found":
        date = datetime.strptime(loss["date"], "%d %b %Y")
        x.append(date)
        y.append(int(loss["model_year"]))
        z.append(loss["name"])

df = pd.DataFrame({'Date': x, 'Model Year': y, 'Name': z})

fig = px.scatter(df, x="Date", y="Model Year", trendline="rolling", trendline_options=dict(window=50), opacity=0.15, template = "slate", title=title, hover_data="Name")
fig.update_layout(xaxis_title="", yaxis_title="")

with open("../../charts/age.html", 'w') as f:
    f.write(fig.to_html(include_plotlyjs='cdn'))