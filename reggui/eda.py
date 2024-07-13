"""
EDA panel for the RegGUI application.
"""
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
from regdbot.brain.analysis import EDA
import os

def run_eda(event, page):
    """
    Run the EDA analysis.
    :param event: the event object
    """
    print("Running EDA")
    page.appbar.actions[0].value = page.client_storage.get("dburl")
    page.RDB.bot.load_database(page.client_storage.get("dburl"))
    if page.client_storage.contains_key("table"):
        table = page.client_storage.get("table")
        df = page.RDB.bot.active_db.get_table_df(table)
        page.eda = EDA(df)
        page.plot_corr_button.disabled = False
        page.update()

def plot_correlation(event, page):
    """
    Plot the correlation matrix.
    :param event: the event object
    """
    df = page.eda.df_filtered
    fig = page.eda.plot_correlation()
    page.plot_panel.content = MatplotlibChart(fig, isolated=True , expand=True)
    page.update()

def show_categorical(event, page):
    """
    Show the categorical data.
    :param event: the event object
    """
    df = page.eda.df_filtered
    table = page.client_storage.get("table")
    df = page.eda.show_categorical(table)


def build_eda_panel(page: ft.Page):
    """
    Build the EDA panel.
    :param page: the page object
    :return: the EDA panel
    """
    page.plot_panel =  ft.Card()
    page.plot_corr_button = ft.ElevatedButton(
        text="Plot Correlation",
        disabled=True,
        on_click=lambda event:  plot_correlation(event, page)
    )
    page.eda_panel = ft.Column(
        [
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.ElevatedButton(
                                text="Run EDA",
                                on_click=lambda event:  run_eda(event, page)
                            ),
                            page.plot_corr_button,
                            ft.ElevatedButton(
                                text="Show Categorical",
                                disabled=True,
                                on_click=lambda event: show_categorical(event, page)
                            ),
                        ],
                        expand=True
                    ),
                   page.plot_panel
                ]
            ),
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.TextField(
                                value="",
                                label="Description",
                                read_only=True,
                            ),
                            ft.TextField(
                                value="",
                                label="Correlation",
                                read_only=True,
                            ),
                            ft.TextField(
                                value="",
                                label="Categorical",
                                read_only=True,
                            ),
                        ],
                        expand=True
                    ),
                    ft.Column(
                        controls=[
                            ft.TextField(
                                value="",
                                label="Nulls",
                                read_only=True,
                            ),
                            ft.TextField(
                                value="",
                                label="Mostly Nulls",
                                read_only=True,
                            ),
                        ],
                        expand=True
                    )
                ]
            )
        ],
        expand=True,
    )
    return page.eda_panel