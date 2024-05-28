import asyncio
import flet as ft


def build_navigation_bar(page: ft.Page):
    page.nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME ,label="Home"),
            ft.NavigationDestination(icon=ft.icons.INFO, label="About"),
        ],
    )

def build_app_bar(page: ft.Page):
    appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.DATASET),
        leading_width=40,
        title=ft.Text("Reg D. Bot"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        adaptive=True,
        toolbar_height=80,
        actions=[
            ft.Dropdown(
                value='',
                width=200,
                label="Sources",
                tooltip="Select a dataset",
                options=[
                    ft.dropdown.Option(text="PostgreSQL", key="postgresql://"),
                    ft.dropdown.Option(text="DuckDB", key="duckdb://"),
                    ft.dropdown.Option(text="CSV", key="csv://"),
                ]
            ),
            ft.Dropdown(
                value='',
                width=200,
                label="Tables",
                tooltip="Select a dataset",
                options=[

                ]
                        ),
            ft.IconButton(icon=ft.icons.SEARCH),
            ft.IconButton(icon=ft.icons.NOTIFICATIONS),
            ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE),
        ],
    )
    return appbar
async def main(page: ft.Page):
    page.title = "Reg D. Bot"
    page.theme = ft.Theme(color_scheme_seed="green")
    page.appbar = build_app_bar(page)
    build_navigation_bar(page)
    page.update()

    def handle_submit(event):
        user_message = page.user_input.value
        page.chat_history.value += f"User: {user_message}\n\n"

        # Simulate AI response by echoing the user's message
        ai_response = f"AI: {user_message}\n\n"
        page.chat_history.value += ai_response

        page.user_input.value = ""
        page.update()

    page.chat_history = ft.Markdown(
        value="# Chat History\n\n",
        selectable=True,
        expand=False,
        extension_set="gitHubWeb",
        code_theme="atom-one-dark",
        code_style=ft.TextStyle(font_family="Roboto Mono")
    )
    page.user_input = ft.TextField(label="Type your message here...", on_submit=handle_submit)
    def route_change(route):
        # print(route)
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    page.appbar,
                    ft.Column(
                        [
                            page.chat_history,
                            page.user_input,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=40
                    ),
                    page.nav_bar
                ],
                scroll=ft.ScrollMode.AUTO,

            )
        )

        if page.route == "/about":
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
    page.route = "/"
    page.go(page.route)


def run():
    ft.app(
        target=main,
        export_asgi_app=True,
        assets_dir="assets",

    )

def run_web():
    ft.app(target=main, export_asgi_app=True)


if __name__ == "__main__":
    run()
