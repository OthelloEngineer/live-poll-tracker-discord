import os

import plotly.express as px
import numpy as np
import pandas as pd
from polldata import PollData


class PlottingService:
    def __init__(self):
        self.directory = "plots/"

    def create_plot(self, data: PollData):
        fig = self.__generate_plot(data)
        new_file_name = self.directory + data.reference_name + ".png"
        fig.write_image(new_file_name)

    def update_plot(self, data: PollData):
        fig = self.__generate_plot(data)
        new_file_name = self.directory + data.reference_name + ".png"
        self.__replace_file(data.reference_name)

        fig.write_image(new_file_name)

    def __generate_plot(self, data: PollData) -> px.pie:
        chart_value: list[int] = []
        chart_labels: list[str] = []
        for option in data.options:
            chart_value.append(data.options[option])
            chart_labels.append(option)

        df = px.data.tips()
        return px.pie(df, values=chart_value, names=chart_labels, title=data.question)

    def __replace_file(self, file_name: str):
        if self.directory + file_name + "_old.png" in os.listdir():
            os.remove(self.directory + file_name + "_old.png")
        if self.directory + file_name + ".png" in os.listdir():
            os.rename(self.directory + file_name + ".png", self.directory + str + "_old.png")


if __name__ == "__main__":
    service = PlottingService()
    poll_data = PollData(question="Test", options={"A": 1, "B": 2, "C": 3}, total_votes=6,
                         link="https://api.strawpoll.com/v3/polls/PKgl3wqaQnp", reference_name="manual_test")
    service.create_plot(poll_data)
