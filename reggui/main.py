import os

import dotenv
import flet as ft
from reggui.workflow import Reggie
from reggui.eda import build_eda_panel

dotenv.load_dotenv()


def build_navigation_bar(page: ft.Page):
    page.nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS, label="Settings", tooltip="Click to select a dataset"),
            ft.NavigationBarDestination(icon=ft.Icons.LIST, label="Log", tooltip="log of questions and answers"),
            ft.NavigationBarDestination(icon=ft.Icons.INFO, label="About"),
        ],
        on_change=lambda e: page.go('/' + e.control.destinations[e.control.selected_index].label.lower())
    )


def build_app_bar(page: ft.Page):
    def set_language(e):
        page.client_storage.set("language", e.control.value)

    def set_table(e):
        page.client_storage.set("table", e.control.value)
        page.chat_history.controls[0].value += f"***Reg:*** You have selected the table: {e.control.value}\n\n"
        page.chat_history.controls[0].value += f"***Reg:*** What would you like to know about this table?\n\n"
        page.user_input.disabled = False
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
            ft.Text(
                width=350,
                value="Source URL",
                expand=True,
            ),
            ft.Dropdown(
                value='',
                width=300,
                label="Tables",
                tooltip="Select a dataset",
                options=[],
                expand=True,
                visible=False,
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
                disabled=True,
                on_change=lambda event: set_language(event)

            ),
            # ft.IconButton(icon=ft.icons.NOTIFICATIONS),
            # ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE),
        ],
    )
    return appbar


def build_settings_page(page: ft.Page):
    def on_dataset_selection(event):
        page.client_storage.remove("dburl")
        page.client_storage.remove("table")
        page.client_storage.set("dburl", event.control.value)
        page.appbar.actions[0].value = event.control.value
        page.RDB.bot.load_database(event.control.value)
        page.appbar.actions[1].options = [ft.dropdown.Option(text=tbl, key=tbl) for tbl in
                                          page.RDB.bot.active_db.tables]

        if page.RDB.bot.active_db.tables:
            page.client_storage.set("table", page.RDB.bot.active_db.tables[0])
            page.appbar.actions[1].value = page.client_storage.get("table")
            page.appbar.actions[1].visible = True
            page.eda_results.value = ""
            page.plot_corr_button.disabled = True
            page.show_categorical_button.disabled = True
            try:
                page.cat_list.visible = False
            except AttributeError:
                pass
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
                                    value="",
                                    options=[
                                        # ft.dropdown.Option(text="regdbot", key=os.environ.get("PGURL")),
                                        ft.dropdown.Option(text="netflix_titles", key=os.environ.get("DUCKURL")),
                                        ft.dropdown.Option(text="Open Access Journals", key=os.environ.get("DUCKURL2")),
                                        ft.dropdown.Option(text="California Housing",
                                                           key="duckdb://reggui/data/cal_housing.db"),
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


def build_chat_log(page: ft.Page):
    page.chat_log = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                ],
                scroll=ft.ScrollMode.ALWAYS,
                expand=True,
            )
        )
    )
    return page.chat_log


def add_log_entry(page: ft.Page, entry: dict):
    page.chat_log.content.content.controls.append(
        ft.Card(
            content=ft.Container(
                ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.PERSON),
                            title=ft.Text(entry.question),
                            subtitle=ft.Text(entry.timestamp),
                        ),
                        ft.Markdown(
                            value=f"```sql\n{entry.code}\n```",
                            selectable=True,
                            expand=False,
                            extension_set="gitHubWeb",
                            code_theme="atom-one-dark",
                            code_style=ft.TextStyle(font_family="Roboto Mono")
                        ),
                        ft.Text(entry.explanation),
                        ft.Row(
                            [
                                ft.ElevatedButton(text="Run query", tooltip="Run the query and export it as CSV",
                                                  disabled=True, icon=ft.icons.PLAY_ARROW, on_click=lambda e: None),
                            ],
                            spacing=10
                        )

                    ],
                    spacing=10
                )
            ),
            margin=ft.margin.symmetric(vertical=5),
            elevation=2,
        )
    )
    page.update()


def build_about_page(page):
    about_page = ft.Container(
        content=ft.ResponsiveRow(
            controls=[
                ft.Column(
                    col=6,
                    controls=[ft.Markdown("""
# About Reggie D. Bot
            
Reggie D. Bot is a database AI expert that can help you explore your data. 
                    
He is powered by the RegDBot library, which is a Python package that provides a 
natural language interface to databases. 
                    
Reggie is built using the Flet web framework, which allows you to build web applications with Python. Reggie can help you with a wide 
range of tasks, such as querying databases, generating reports, and even creating visualizations. 

Reggie is designed by [Deeplearn](www.deeplearn.ltd) to be easy to use and flexible, so you can customize him to suit your needs. 
 If you have any questions or feedback, please feel free to reach out to us. We're always happy to help!
""",
                                          extension_set=ft.MarkdownExtensionSet.GITHUB_WEB
                                          )]),
                ft.Column(col=6,
                          controls=[
                              ft.Image(src="/images/reggie.webp", fit=ft.ImageFit.CONTAIN)
                          ])]
        ),
        padding=20
    )
    return about_page


async def start_reg(page):
    page.RDB = Reggie(model="gpt")


async def main(page: ft.Page):
    page.title = "Reg D. Bot"
    page.theme = ft.Theme(color_scheme_seed="black")
    page.appbar = build_app_bar(page)
    page.prog_ring = ft.ProgressRing(value=None, visible=False)
    build_navigation_bar(page)
    build_chat_log(page)
    page.update()
    await start_reg(page)

    def handle_submit(event):
        page.prog_ring.visible = True
        user_message = page.user_input.value
        page.chat_history.controls[0].value += f"User: {user_message}\n\n"
        page.user_input.value = ""
        page.prog_ring.value = None
        page.update()
        # Simulate AI response by echoing the user's message
        response = page.RDB.ask(user_message, page.client_storage.get("table"))
        page.prog_ring.value = 100
        ai_response = f"***Reg:*** {response}\n\n"
        log_entry = page.RDB.bot.chat_history.recall(page.RDB.bot.session_id)
        add_log_entry(page, log_entry[-1])
        page.chat_history.controls[0].value += ai_response
        page.prog_ring.visible = False
        page.go("/home")
        page.update()

    page.chat_history = ft.Column(
        [
            ft.Markdown(
                value="Hi! I am *Reggie D. Bot*, your friendly database AI expert. Please select a dataset for us to analyze!\n\n",
                selectable=True,
                expand=False,
                extension_set="gitHubWeb",
                code_theme="atom-one-dark",
                code_style=ft.TextStyle(font_family="Roboto Mono")
            )
        ],
        scroll=ft.ScrollMode.ALWAYS,
    )
    page.user_input = ft.TextField(label="Type your message here...",
                                   on_submit=handle_submit,
                                   disabled=True,
                                   expand=True
                                   )

    mugshot = ft.Card(
        col=2.5,
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Image(src="/images/reggie.webp", width=200, height=200, fit=ft.ImageFit.CONTAIN),
                    ft.Text("Reggie D. Bot", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Database AI Expert", size=16, weight=ft.FontWeight.NORMAL),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            padding=10,
        )
    )

    def pick_files_result(e: ft.FilePickerResultEvent):
        files = e.files
        upload_list = []
        if files:
            for f in files:
                upload_list.append(
                    ft.FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )
        pick_files_dialog.upload(upload_list)

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)

    page.overlay.append(pick_files_dialog)

    def validate_source(e):
        page.chat_history.controls[0].value += f"***Reg:*** Database loaded: {page.client_storage.get('dburl')}\n\n"
        tlist = '\n'.join([f"- {t}\n" for t in page.RDB.bot.active_db.tables])
        page.chat_history.controls[
            0].value += f"***Reg:*** These are the tables available in this database: \n{tlist}\n\n"
        page.chat_history.controls[
            0].value += f"***Reg:*** Why don't you select one of these in the pull down menu above so we can explore it together?\n\n"
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
                    ft.ResponsiveRow(
                        [
                            mugshot,
                            ft.Column(col=9.5,
                                      controls=[
                                          page.chat_history,
                                          ft.Row([page.user_input, page.prog_ring]),
                                      ],
                                      alignment=ft.MainAxisAlignment.START,
                                      spacing=40,
                                      height=page.height-200 if page.web else page.window_height-200, #window attibutes are only available for desktop apps
                                      expand=True,
                                      # auto_scroll=True,
                                      scroll=ft.ScrollMode.ALWAYS
                                      )
                        ]
                    ),
                    page.nav_bar
                ],
                # scroll=ft.ScrollMode.AUTO,
            )
        )
        if page.route == "/settings":
            page.views.append(
                ft.View(
                    "/settings",
                    [
                        page.appbar,
                        build_settings_page(page),
                        ft.Row(
                            [ft.ElevatedButton(text="Test connection", icon=ft.icons.POWER, on_click=validate_source),
                             ft.ElevatedButton(text="Upload dataset", icon=ft.icons.UPLOAD_SHARP, disabled=True,
                                               on_click=lambda e: pick_files_dialog.pick_files(
                                                   dialog_title="Select DuckDB file"))]),
                        page.nav_bar
                    ],
                    scroll=ft.ScrollMode.AUTO
                )
            )
        elif page.route == "/log":
            page.views.append(
                ft.View(
                    "/log",
                    [
                        page.appbar,
                        page.chat_log,
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
                        build_about_page(page),
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
    upload_dir="data"
)


def run():
    ft.app(
        target=main,
        assets_dir="assets",
        upload_dir="data"
    )


if __name__ == "__main__":
    pass
    run()
