
import sys
from CommonClient import get_base_parser
from .world_manager import SortStages, install_world, refresh_apworld_table, repositories


def launch(*launch_args: str):
    import kvui  # noqa
    from kivy.properties import DictProperty

    from kivy.app import App
    from kivy.lang import Builder
    # from kivy.properties import DictProperty
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.recycleview import RecycleView
    from kivy.uix.recycleview.views import RecycleDataViewBehavior
    from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
    from kivy.uix.popup import Popup
    from kivy.core.window import Window

    # I do not like this, but kivyMD messageboxes don't work with non-MD Apps, so we'll backport the original messagebox so install_apworld can use it
    class MessageBox(Popup):
        class MessageBoxLabel(Label):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self._label.refresh()
                self.size = self._label.texture.size
                if self.width + 50 > Window.width:
                    self.text_size[0] = Window.width - 50
                    self._label.refresh()
                    self.size = self._label.texture.size

        def __init__(self, title, text, error=False, **kwargs):
            label = MessageBox.MessageBoxLabel(text=text)
            separator_color = [217 / 255, 129 / 255, 122 / 255, 1.] if error else [47 / 255., 167 / 255., 212 / 255, 1.]
            super().__init__(title=title, content=label, size_hint=(None, None), width=max(100, int(label.width) + 40),
                            separator_color=separator_color, **kwargs)
            self.height += max(0, label.height - 18)

    kvui.MessageBox = MessageBox

    kv = """
<ApworldDirectoryWindow>:
    tab_width: root.width / 2
    default_tab_text: "APWorlds"

<ApworldDirectoryItem>
    canvas.before:
        Color:
            rgba: 0.6, 0.6, 0.6, 1  # Light gray lines
        Line:
            rectangle: (self.x, self.y, self.width, self.height)  # Border around the row
    Label:
        text: root.details["title"]
        size_hint: .5, 1
        canvas.before:
            Color:
                rgba: 0.6, 0.6, 0.6, 1
            Line:
                points: (self.right, self.y, self.right, self.top)  # Vertical separator
    Label:
        text: root.details["description"]
        size_hint: .3, 1
        canvas.before:
            Color:
                rgba: 0.6, 0.6, 0.6, 1
            Line:
                points: (self.right, self.y, self.right, self.top)
    Button:
        text: root.details["install_text"]
        size_hint: .2, 1
        on_press: root.download_latest()
        disabled: root.details["description"] == "Up to date"
    Button:
        text: "Details"
        size_hint: .2, 1
        on_press: root.switch_to_detail()

<RV>:
    viewclass: 'ApworldDirectoryItem'
    bar_width: 20
    scroll_type: ['bars', 'content']  # Show both content scroll & bars
    bar_color: 0.2, 0.6, 1, 1  # Bright blue active bar
    bar_inactive_color: 0.2, 0.6, 1, 0.6  # Slightly faded when inactive
    effect_cls: 'ScrollEffect'  # Keeps smooth scrolling
    canvas.before:
        Color:
            rgba: 0.2, 0.6, 1, 0.4  # Background track color
        RoundedRectangle:
            pos: (self.width - self.bar_width, self.y)
            size: (self.bar_width, self.height)
            radius: [10,]  # Rounded ends for the track
    RecycleBoxLayout:
        default_size: root.width, dp(30)
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'

<ApworldDetails>:
    BoxLayout:
        orientation: 'vertical'
        # Label:
        #     text: root.details["title"]
        #     size_hint: 1, 0.1
        Label:
            text: root.details["world_description"]
            size_hint: 1, 0.8
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, 0.2
            Button:
                text: root.latest_text
                size_hint: 1, 1
                on_press: root.download_latest()
            Button:
                text: root.tracker_text
                size_hint: 1, 1
                disabled: root.tracker_disabled
                on_press: root.open_tracker()
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, 0.2
            Button:
                text: "View GitHub"
                size_hint: 1, 1
                on_press: root.open_release()
            Button:
                text: "View Wiki Page"
                size_hint: 1, 1
                on_press: root.open_wiki()

"""
    Builder.load_string(kv)

    class DirectoryApp(App):
        tab_count = 1  # kvui for some reason monkeypatches tab_length to require this,,

        def __init__(self, *args, apworlds: list = None, **kwargs):
            super().__init__(*args, **kwargs)
            if apworlds is None:
                apworlds = refresh_apworld_table()
            self.apworlds = apworlds
            from . import RepoWorld
            if hasattr(RepoWorld, 'world_version'):
                self.title = f'APWorld Manager {RepoWorld.world_version}'
            else:
                self.title = f'APWorld Manager {RepoWorld.world_version_str}'

        def build(self):
            window = ApworldDirectoryWindow()
            self.rv = window.default_tab_content = RV(self.apworlds)
            self.apworlds = self.rv.data
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
            install_world(self.details)
            app.apworlds.clear()
            app.apworlds.extend(refresh_apworld_table())
            app.root.default_tab_content.refresh_from_data()

        def open_tracker(self):
            import webbrowser
            if self.tracker_url:
                webbrowser.open(self.tracker_url)

        def open_release(self):
            import webbrowser
            if self.details['latest_version'].release_url:
                webbrowser.open(self.details['latest_version'].release_url)
            else:
                webbrowser.open(self.details['latest_version'].download_url.split('/releases')[0])

        def open_wiki(self):
            import webbrowser
            webbrowser.open(f'https://archipelago.miraheze.org/wiki/{self.details["title"]}')

        @property
        def latest_text(self):
            if self.details["installed"] and self.details["update_available"]:
                return f"Update available: {self.details['latest_version'].world_version}"
            elif self.details["installed"]:
                return "Up to date"
            else:
                return f"Install {self.details['latest_version'].world_version}"

        @property
        def tracker_url(self):
            return self.details.latest_version.data['metadata'].get('tracker', '')

        @property
        def tracker_text(self):
            if self.details.latest_version.tracker_included:
                return "Has Integrated Tracker"
            return "View Tracker" if self.tracker_url else "(No tracker known)"

        @property
        def tracker_disabled(self):
            return not self.tracker_url

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
            install_world(self.details)

            app.apworlds.clear()
            app.apworlds.extend(refresh_apworld_table())
            app.root.default_tab_content.refresh_from_data()

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

    import argparse
    parser = argparse.ArgumentParser()
    if sys.stdout:  # If terminal output exists, offer gui-less mode
        parser.add_argument('--nogui', default=False, action='store_true', help="Turns off Client GUI.")

    parser.add_argument("--update-all", action="store_true", help="Run in non-GUI mode to just install/update worlds then exit")

    args, rest = parser.parse_known_args(launch_args)

    if args.update_all:
        for world in apworlds:
            if world['sort'] == SortStages.UPDATE_AVAILABLE:
                print(f"Updating {world['title']} to version {world['latest_version'].world_version}...")
                install_world(world)
        repositories.cleanup_downloads()
        return

    app = DirectoryApp(apworlds=apworlds)
    app.run()

    repositories.cleanup_downloads()


if __name__ == '__main__':
    launch()
