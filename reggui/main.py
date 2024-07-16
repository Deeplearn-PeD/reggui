import os

import dotenv
import flet as ft
from reggui.workflow import Reggie
from reggui.eda import build_eda_panel

dotenv.load_dotenv()


def build_navigation_bar(page: ft.Page):
    page.nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
            ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Settings"),
            ft.NavigationDestination(icon=ft.icons.INFO, label="About"),
        ],
        on_change=lambda e: page.go('/' + e.control.destinations[e.control.selected_index].label.lower())
    )


def build_app_bar(page: ft.Page):
    def set_language(e):
        page.client_storage.set("language", e.control.value)

    def set_table(e):
        page.client_storage.set("table", e.control.value)
        page.chat_history.value += f"***Reg:*** You have selected the table: {e.control.value}\n\n"
        page.chat_history.value += f"***Reg:*** What would you like to know about this table?\n\n"
        page.update()

    appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.DATASET),
        leading_width=40,
        title=ft.Text("Reg D. Bot"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        adaptive=True,
        toolbar_height=80,
        actions=[
            ft.TextField(
                label="Source URL",
                width=350,
                value="",
                expand=True,
                read_only=True,
            ),
            ft.Dropdown(
                value='',
                width=300,
                label="Tables",
                tooltip="Select a dataset",
                options=[],
                expand=True,
                on_change=lambda event: set_table(event)
            ),
            ft.Dropdown(
                value='en_US',
                width=200,
                label="Language",
                tooltip="Select a language",
                options=[
                    ft.dropdown.Option(text="English", key="en_US"),
                    ft.dropdown.Option(text="Portuguese", key="pt_BR"),
                ],
                on_change=lambda event: set_language(event)

            ),
            ft.IconButton(icon=ft.icons.NOTIFICATIONS),
            ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE),
        ],
    )
    return appbar


def build_settings_page(page: ft.Page):
    def on_dataset_selection(event):
        page.client_storage.remove("dburl")
        page.client_storage.remove("table")
        page.client_storage.set("dburl", event.control.value)
        page.appbar.actions[0].value = page.client_storage.get("dburl")
        page.RDB.bot.load_database(page.client_storage.get("dburl"))
        page.appbar.actions[1].options = [ft.dropdown.Option(text=tbl, key=tbl) for tbl in
                                          page.RDB.bot.active_db.tables]

        if page.RDB.bot.active_db.tables:
            page.client_storage.set("table", page.RDB.bot.active_db.tables[0])
            page.appbar.actions[1].value = page.client_storage.get("table")
            page.eda_results.value = ""
            page.plot_corr_button.disabled = True
            page.show_categorical_button.disabled = True
        else:
            page.client_storage.set("table", "")
        page.update()

    page.settings_form = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Container(
                        padding=20,
                        content=ft.Column(
                            controls=[
                                ft.Text("Data Source Configuration", size=28, weight=ft.FontWeight.BOLD),
                                ft.Dropdown(
                                    label="Database",
                                    value="postgresql://",
                                    options=[
                                        ft.dropdown.Option(text="regdbot", key=os.environ.get("PGURL")),
                                        ft.dropdown.Option(text="netflix_titles", key=os.environ.get("DUCKURL")),
                                        ft.dropdown.Option(text="Open Access Journals", key=os.environ.get("DUCKURL2")),
                                    ],
                                    on_change=on_dataset_selection
                                ),
                            ],
                            # expand=True,
                            # alignment=ft.MainAxisAlignment.START
                        )
                    ),
                    build_eda_panel(page)
                ],
                # expand=True
            )]
    )
    return page.settings_form


async def start_reg(page):
    page.RDB = Reggie(model="gpt")


async def main(page: ft.Page):
    page.title = "Reg D. Bot"
    page.theme = ft.Theme(color_scheme_seed="green")
    page.appbar = build_app_bar(page)
    page.prog_ring = ft.ProgressRing(value=None, visible=False)
    build_navigation_bar(page)
    page.update()
    await start_reg(page)

    def handle_submit(event):
        page.prog_ring.visible = True
        user_message = page.user_input.value
        page.chat_history.value += f"User: {user_message}\n\n"
        page.user_input.value = ""
        page.prog_ring.value = None
        page.update()
        # Simulate AI response by echoing the user's message
        response = page.RDB.ask(user_message, page.client_storage.get("table"))
        page.prog_ring.value = 100
        ai_response = f"***Reg:*** {response}\n\n"
        page.chat_history.value += ai_response
        page.prog_ring.visible = False

        page.update()

    page.chat_history = ft.Markdown(
        value="Hi! I am *Reggie D. Bot*, your friendly database AI expert. How can I help you today?\n\n",
        selectable=True,
        expand=False,
        extension_set="gitHubWeb",
        code_theme="atom-one-dark",
        code_style=ft.TextStyle(font_family="Roboto Mono")
    )
    page.user_input = ft.TextField(label="Type your message here...",
                                   on_submit=handle_submit,
                                   expand=True
                                   )

    mugshot = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Image(src="/images/reggie.png", width=200, height=200, fit=ft.ImageFit.CONTAIN),
                    ft.Text("Reggie D. Bot", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Database AI Expert", size=16, weight=ft.FontWeight.NORMAL),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            padding=10,
        )
    )

    def validate_source(e):
        page.chat_history.value += f"***Reg:*** Database loaded: {page.client_storage.get('dburl')}\n\n"
        tlist = '\n'.join([f"- {t}\n" for t in page.RDB.bot.active_db.tables])
        page.chat_history.value += f"***Reg:*** These are the tables available in this database: \n{tlist}\n\n"
        page.chat_history.value += f"***Reg:*** Why don't you select one of these in the pull down menu above so we can explore it together?\n\n"
        page.go("/home")
        page.update()

    async def route_change(route):
        # print(route)
        page.views.clear()
        page.views.append(
            ft.View(
                "/home",
                [
                    page.appbar,
                    ft.Column(
                        [
                            mugshot,
                            page.chat_history,
                            ft.Row([page.user_input, page.prog_ring])
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=40
                    ),
                    page.nav_bar
                ],
                scroll=ft.ScrollMode.AUTO,

            )
        )
        if page.route == "/settings":
            page.views.append(
                ft.View(
                    "/settings",
                    [
                        page.appbar,
                        build_settings_page(page),
                        ft.ElevatedButton(text="Test connection", icon=ft.icons.POWER, on_click=validate_source),
                        page.nav_bar
                    ],
                    scroll=ft.ScrollMode.AUTO
                )
            )
        elif page.route == "/about":
            page.views.append(
                ft.View(
                    "/about",
                    [
                        page.appbar,
                        ft.Text("About page"),
                        page.nav_bar
                    ],
                    scroll=ft.ScrollMode.AUTO
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # page.add(context, write_button, response_card)
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.route = "/home"
    page.go(page.route)


# def run_web():
app = ft.app(
    target=main,
    export_asgi_app=True,
    assets_dir="assets",
)


def run():
    ft.app(target=main, assets_dir="assets")


if __name__ == "__main__":
    pass
    run()
