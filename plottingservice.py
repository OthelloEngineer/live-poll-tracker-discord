import os

import plotly.express as px
import numpy as np
import pandas as pd
from polldata import PollData


class PlottingService:

    def generate_plot(self, data: PollData):
        chart_value: list[int] = []
        chart_labels: list[str] = []
        for option in data.options:
            chart_value.append(data.options[option])
            chart_labels.append(option)

        df = px.data.tips()
        fig = px.pie(df, values=chart_value, names=chart_labels, title=data.question)

        fig.write_image(data.reference_name + ".png")

    def update_plot(self, data: PollData):
        chart_value: list[int] = []
        chart_labels: list[str] = []
        for option in data.options:
            chart_value.append(data.options[option])
            chart_labels.append(option)

        df = px.data.tips()
        fig = px.pie(df, values=chart_value, names=chart_labels, title=data.question)
        if data.reference_name + "_old.png" in os.listdir():
            os.remove(data.reference_name + "_old.png")
        if data.reference_name + ".png" in os.listdir():
            os.rename(data.reference_name + ".png", data.reference_name + "_old.png")
        fig.write_image(data.reference_name + ".png")


if __name__ == "__main__":
    service = PlottingService()
    poll_data = PollData(question="Test", options={"A": 1, "B": 2, "C": 3}, total_votes=6,
                         link="https://api.strawpoll.com/v3/polls/PKgl3wqaQnp", reference_name="manual_test")
    service.generate_plot(poll_data)
