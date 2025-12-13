import hashlib
from worlds.Files import InvalidDataError
from worlds.apworld_manager.world_manager import SortStages
from .world_manager import RepositoryManager, parse_version, refresh_apworld_table, repositories
from worlds.LauncherComponents import install_apworld


def launch():
    from kvui import (
        Builder,
        RecycleDataViewBehavior,
        ClientTabs,
        MDTabsItem,
        )
    from kivy.properties import DictProperty

    try:
        from worlds.Files import APWorldContainer
    except ImportError:
        from ._vendor.world_container import APWorldContainer

    from kivymd.app import MDApp
    # from kivy.lang import Builder
    # from kivy.properties import DictProperty
    from kivymd.uix.boxlayout import BoxLayout
    from kivymd.uix.label import MDLabel
    from kivymd.uix.recycleview import MDRecycleView
    kv = """
<ApworldDirectoryWindow>:
    tab_width: root.width / 2
    default_tab_text: "APWorlds"

<ApworldDirectoryItem>
    Label:
        text: root.details["title"]
        size_hint: .5, 1
    Label:
        text: root.details["description"]
        size_hint: .3, 1
    Button:
        text: root.details["install_text"]
        size_hint: .2, 1
        on_press: root.download_latest()
        disabled: root.details["install_text"] == "-"
    Button:
        text: "Details"
        size_hint: .2, 1
        on_press: root.switch_to_detail()

<RV>:
    viewclass: 'ApworldDirectoryItem'
    RecycleBoxLayout:
        default_size: root.width, dp(30)
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'

<ApworldDetails>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: root.details["title"]
            size_hint: 1, 0.1
        # Label:
        #     text: root.details["description"]
        #     size_hint: 1, 0.1
        Button:
            text: root.latest_text
            size_hint: 1, 0.1
            on_press: root.download_latest()

"""
    Builder.load_string(kv)

    class DirectoryApp(MDApp):
        tab_count = 1  # kvui for some reason monkeypatches tab_length to require this,,

        def __init__(self, *args, apworlds={}, **kwargs):
            super().__init__(*args, **kwargs)
            self.apworlds = apworlds
            from . import RepoWorld
            self.title = f'APWorld Manager {RepoWorld.world_version}'

        def build(self):
            window = ApworldDirectoryWindow()
            window.default_tab_content = RV(self.apworlds)
            return window

    class ApworldDirectoryWindow(TabbedPanel):
        def switch_to(self, header, do_scroll=False):
            if header == self.default_tab:
                self.clear_tabs()
            super().switch_to(header, do_scroll=do_scroll)

    class ApworldDetails(TabbedPanelItem):
        def __init__(self, details, *args, **kwargs):
            self.details = details
            super().__init__(*args, **kwargs)

        def download_latest(self):
            print("Downloading latest version")
            path = repositories.download_remote_world(self.details["latest_version"])
            install_apworld(path)
            app.apworlds = refresh_apworld_table()

        @property
        def latest_text(self):
            if self.details["installed"] and self.details["update_available"]:
                return f"Update available: {self.details['latest_version'].world_version}"
            elif self.details["installed"]:
                return "Up to date"
            else:
                return f"Install {self.details['latest_version'].world_version}"

    class ApworldDirectoryItem(RecycleDataViewBehavior, BoxLayout):
        details = DictProperty({"title": "game name", "description": "short description", "install_text": "N/A"})

        def refresh_view_attrs(self, rv, index, details):
            self.details = details
            super().refresh_view_attrs(rv, index, details)

        def switch_to_detail(self):
            details_tab = ApworldDetails(self.details, text=self.details["title"])
            directory_window = App.get_running_app().root
            directory_window.add_widget(details_tab)
            directory_window.switch_to(details_tab)

        def download_latest(self):
            print("Downloading latest version")
            path = repositories.download_remote_world(self.details["latest_version"])
            install_apworld(path)
            app.apworlds = refresh_apworld_table()


    class RV(RecycleView):
        def __init__(self, data, **kwargs):
            super().__init__(**kwargs)
            self.data = data

    class VersionView(RecycleView):
        def __init__(self, data, **kwargs):
            super().__init__(**kwargs)
            self.data = data

    repositories.load_repos_from_settings()
    repositories.refresh()



    apworlds = refresh_apworld_table()

    app = DirectoryApp(apworlds=apworlds)
    app.run()


if __name__ == '__main__':
    launch()
