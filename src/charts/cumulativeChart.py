import pandas as pd

import plotly.express as px

import json

import datetime
from dash_bootstrap_templates import load_figure_template

load_figure_template("slate")

f = open("../../data/losses.json")
losses = json.load(f)
f.close()

f = open("../../data/meta.json")
metaData = json.load(f)
lastUpdateDate = metaData["last_update_date"]
title = f"Cumulative Count Of Lost Russiant Tanks<br><sup>Updated: {lastUpdateDate}</sup>"
f.close()

lastRecordedDate = datetime.datetime.strptime(losses[0]["date"], "%d %b %Y")
firstRecordedDate = datetime.datetime.strptime(losses[len(losses) - 1]["date"], "%d %b %Y")
dates = list(pd.date_range(start=firstRecordedDate, end=lastRecordedDate))

data = {
    "T-54": [0] * len(dates), 
    "T-55": [0] * len(dates), 
    "T-62": [0] * len(dates), 
    "T-64": [0] * len(dates), 
    "T-72": [0] * len(dates),
    "T-80": [0] * len(dates),
    "T-90": [0] * len(dates),
    "T-14": [0] * len(dates),
    "Date": [] 
}

for idx, date in enumerate(dates):
    data["Date"].append(date.date())

    for loss in losses:
        modelMatch = loss["model_match"]
        losstime = datetime.datetime.strptime(loss["date"], "%d %b %Y")
        if modelMatch != "No Match Found" and losstime < date:
            data[modelMatch][idx] += 1


formatedData = pd.melt(pd.DataFrame(data=data), id_vars="Date").sort_values(by=["Date", "value", "variable"])

fig = px.bar(formatedData, x="value", y="variable", animation_frame="Date", title=title, text_auto=True, orientation='h')

fig.update_layout(xaxis_title="", yaxis_title="")

fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 100
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 0
fig.update_layout(xaxis_range=[0, formatedData.max()["value"] + 50])

with open("../../charts/cumulative.html", 'w') as f:
    f.write(fig.to_html(include_plotlyjs='cdn', auto_play=False))