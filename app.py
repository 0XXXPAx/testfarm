import asyncio
from contextlib import suppress

import flet as ft


async def main(page: ft.Page) -> None:
    page.title = "Mandarin Clicker"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#141221"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {"FulboArgenta": "fonts/FulboArgenta.ttf"}
    page.theme = ft.Theme(font_family="FulboArgenta")

    async def score_up(event: ft.ContainerTapEvent) -> None:
        score.data += 1
        score.value = str(score.data)

        image.scale = 0.95
        progress_bar.value += (1 / 100)

        audio = ft.Audio(src="audio/cute.mp3", autoplay=True)
        page.overlay.append(audio)

        if score.data % 100 == 0:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    value="🍊 +100",
                    size=20,
                    color="#ff8b1f",
                    text_align=ft.TextAlign.CENTER
                ),
                bgcolor="#25223a"
            )
            page.snack_bar.open = True
            progress_bar.value = 0

        await page.update_async()
        
        with suppress(AttributeError):
            await audio.play_async()

        await asyncio.sleep(0.1)
        image.scale = 1

        await page.update_async()
        page.overlay.clear()

    score = ft.Text(value="0", size=100, data=0)
    image = ft.Image(
        src="mandarin.png",
        fit=ft.ImageFit.CONTAIN,
        animate_scale=ft.Animation(duration=600, curve=ft.AnimationCurve.EASE)
    )
    progress_bar = ft.ProgressBar(
        value=0,
        width=page.width - 100,
        bar_height=20,
        color="#ff8b1f",
        bgcolor="#bf6524"
    )

    await page.add_async(
        score,
        ft.Container(
            content=ft.Stack(controls=[image]),
            on_click=score_up,
            margin=ft.Margin(0, 0, 0, 30)
        ),
        ft.Container(
            content=progress_bar,
            border_radius=ft.BorderRadius(10, 10, 10, 10)
        )
    )


if __name__ == "__main__":
    ft.app(target=main, view=None, port=8000)