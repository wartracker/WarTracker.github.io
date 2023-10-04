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
f.close()

start = datetime.datetime.strptime("23 Feb 2022", "%d %b %Y")
end = datetime.datetime.strptime(losses[0]["date"], "%d %b %Y")
dates = list(pd.date_range(start=start, end=end))

data = {
    "T-54/55": [0] * len(dates), 
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
    endDate = date
    startDate = date - datetime.timedelta(weeks=8)
    total = 0

    for loss in losses:
        losstime = datetime.datetime.strptime(loss["date"], "%d %b %Y")
        modelMatch = loss["model_match"]
        if losstime >= startDate and losstime <= endDate and modelMatch != "No Match Found":
            total += 1
    for loss in losses:
        losstime = datetime.datetime.strptime(loss["date"], "%d %b %Y")
        modelMatch = loss["model_match"]
        if losstime >= startDate and losstime <= endDate and modelMatch != "No Match Found":
            data[modelMatch][idx] += 1/total * 100

formatedData = pd.melt(pd.DataFrame(data=data), id_vars="Date")

fig = px.bar(formatedData, x="variable", y="value", animation_frame="Date", template = "slate", title=f'Percentage Of Russian Tanks Lost Last 4 Weeks By Model (Updated: {metaData["last_update_date"]})')
fig.update_layout(yaxis_range=[0, 100])
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 100
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 40

fig.update_layout(xaxis_title="", yaxis_title="")

with open("../../charts/precentage.html", 'w') as f:
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn', auto_play=False))