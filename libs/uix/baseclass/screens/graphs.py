import logging
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd
from kivy.clock import Clock
from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivymd.uix.screen import MDScreen

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class GraphScreen(MDScreen):
    # Property to hold the shared Username
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.candlestick_data = self.generate_dummy_data()
        self.fig, self.ax = plt.subplots()
        self.plot_candlestick(self.candlestick_data)
        self.graph = FigureCanvasKivyAgg(self.fig)
        self.ids.graph_container.add_widget(self.graph)

        # Schedule the chart update every second
        Clock.schedule_interval(self.update_chart, 1)

    def generate_dummy_data(self):
        # Create some dummy candlestick data for demonstration
        num_data_points = 30
        date_rng = pd.date_range(
            datetime.now() - timedelta(days=num_data_points),
            periods=num_data_points,
            freq="D",
        )
        data = pd.DataFrame(date_rng, columns=["Date"])
        data["Open"] = np.random.uniform(100, 200, size=(num_data_points,))
        data["High"] = data["Open"] + np.random.uniform(0, 20, size=(num_data_points,))
        data["Low"] = data["Open"] - np.random.uniform(0, 20, size=(num_data_points,))
        data["Close"] = np.random.uniform(100, 200, size=(num_data_points,))
        data.set_index("Date", inplace=True)
        return data

    def plot_candlestick(self, data):
        self.ax.clear()
        mpf.plot(data, type="candle", ax=self.ax, style="charles")

    def update_chart(self, dt):
        # Simulate real-time updates by adding new random data
        new_data = {
            "Open": np.random.uniform(100, 200),
            "High": np.random.uniform(200, 220),
            "Low": np.random.uniform(100, 200),
            "Close": np.random.uniform(100, 200),
        }
        now = datetime.now()
        self.candlestick_data.loc[now] = pd.Series(new_data)

        # Keep the latest 30 data points for display
        self.candlestick_data = self.candlestick_data.tail(30)

        # Update the candlestick plot
        self.plot_candlestick(self.candlestick_data)
        self.graph.draw()
