"""
EDA panel for the RegGUI application.
"""
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
from regdbot.brain.analysis import EDA


def run_eda(event, page):
    """
    Run the EDA analysis.
    :param event: the event object
    """
    print("Running EDA")
    page.pr_eda.value = None
    page.appbar.actions[0].value = page.client_storage.get("dburl")
    page.RDB.bot.load_database(page.client_storage.get("dburl"))
    if page.client_storage.contains_key("table"):
        table = page.client_storage.get("table")
        df = page.RDB.bot.active_db.get_table_df(table)
        page.eda = EDA(df)
        page.eda_panel.content.controls[0].controls.append(build_cat_dropdown(page))
        page.eda_results.value += "## Descriptive Statistics for numeric columns\n\n"
        page.eda_results.value += page.eda.describe().to_markdown()
        page.eda_results.visible = True
        page.plot_corr_button.disabled = False
        page.show_categorical_button.disabled = False
        page.pr_eda.value = 100
        page.update()


def plot_correlation(event, page):
    """
    Plot the correlation matrix.
    :param event: the event object
    """
    df = page.eda.df_filtered
    fig = page.eda.plot_correlation()
    page.plot_card.content.content = MatplotlibChart(fig, isolated=False, expand=True)
    page.bottom_sheet.open = True
    page.bottom_sheet.update()


def show_categorical(event, page):
    """
    Show the categorical data.
    :param event: the event object
    """
    df = page.eda.df_filtered
    table = page.client_storage.get("table")
    df = page.eda.show_categorical(page.cat_list.value)
    page.eda_results.value += "\n\n## Category counts for column: *" + page.cat_list.value + "* (top 20)\n\n"
    page.eda_results.value += "\n\n" + df.iloc[:20].to_markdown()
    page.update()

def build_cat_dropdown(page: ft.Page):
    cats = page.eda.categorical_columns
    page.cat_list = ft.Dropdown(
        label="Categorical Columns",
        value=cats[0],
        key=cats[0],
        options=[ft.dropdown.Option(text=col, key=col) for col in cats],
        tooltip="Select a column to show the categorical data."
    )
    return page.cat_list

def build_eda_panel(page: ft.Page):
    """
    Build the EDA panel.
    :param page: the page object
    :return: the EDA panel
    """

    def bs_close(event):
        page.bottom_sheet.open = False
        page.bottom_sheet.update()

    page.pr_eda = ft.ProgressBar(value=0, visible=True)
    page.plot_card = ft.Card(ft.Container(padding=10))
    page.bottom_sheet = ft.BottomSheet(
        content=ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    page.plot_card,
                    ft.ElevatedButton("Close", on_click=bs_close)
                ]
            )
        )
    )
    page.plot_corr_button = ft.ElevatedButton(
        text="Plot Correlation",
        disabled=True,
        on_click=lambda event: plot_correlation(event, page)
    )
    page.show_categorical_button = ft.ElevatedButton(
        text="Show Categorical",
        disabled=True,
        on_click=lambda event: show_categorical(event, page)
    )

    page.eda_results = ft.Markdown(
        value="",
        visible=True,
        selectable=True,
        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB
    )

    page.eda_panel = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            text="Run EDA",
                            on_click=lambda event: run_eda(event, page)
                        ),
                        page.plot_corr_button,
                        page.show_categorical_button,
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                page.pr_eda,
                ft.Text("Results", size=20),
                page.eda_results
            ],
            # expand=True
        ),
    expand = True,
    )
    return page.eda_panel
