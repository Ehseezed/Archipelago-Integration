# Zig's original UI.
# Unfortunately, this isn't useful because KivyMD isn't bundled in frozen yet.
# Turns out it's also MD 1.1, so it's not useful regardless


from kivymd.app import MDApp
from kivy.properties import StringProperty
# from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.uix.dropdown import DropDown
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
import packaging.version
import os
from Utils import title_sorted
from worlds import AutoWorldRegister, WorldSource

from .world_manager import ApWorldMetadata, RepositoryManager
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
# Config.set('graphics', 'width', '1600')
Config.write()

ap_worlds = {w.zip_path.name.replace('.apworld', ''):w for n, w in AutoWorldRegister.world_types.items() if w.zip_path is not None}

class CustomDropDown(DropDown):
    pass

class MainLayout(GridLayout):

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.cols = 1

from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp

from kivymd.uix.list import OneLineAvatarIconListItem

from kivymd.uix.list import OneLineListItem

KV = '''
<Item>
    MDRaisedButton:
        text: root.text
    ImageLeftWidget:
        source: root.source

'''
class Item(OneLineListItem):
    divider = None
    source = StringProperty()

class WorldManagerApp(MDApp):
    def __init__(self, repositories: RepositoryManager) -> None:
        self.repositories = repositories
        super().__init__()

    def get_world_info(self):
        world_info = []
        self.world_name_to_id = {}
        self.available_versions = {}
        self.descriptions = {}
        self.installed_version = {}
        for world_id in self.repositories.all_known_package_ids:
            available_versions: dict[str, ApWorldMetadata] = {}
            self.available_versions[world_id] = available_versions
            world_name = world_id

            for world in self.repositories.packages_by_id_version[world_id].values():
                # Note, probably we need to use actual "properties" here to get good refresh
                world_name = world.name
                #world_info['available.text'] = str(world.world_version)
                available_versions[world.world_version] = world
                self.descriptions[world_id] = world.data['metadata']['description']

            if world_id in self.repositories.local_packages_by_id:
                world = self.repositories.local_packages_by_id[world_id]
                world_name = world.name
                #world_info['installed.text'] = str(world.world_version)
                available_versions[world.world_version] = world
                self.descriptions[world_id] = world.data['metadata']['description']
                self.installed_version[world_id] = world.world_version

            if not world_name:
                # Missing data
                if w := ap_worlds.get(world_id):
                    world_name = w.game
                else:
                    world_name = world_id + ".apworld"
                world.data['metadata']['game'] = world_name

            if installed := AutoWorldRegister.world_types.get(world_name):
                if world_id not in self.installed_version:
                    self.installed_version[world_id] = installed.world_version
                else:
                    local = packaging.version.parse(self.installed_version[world_id])
                    installed = packaging.version.parse(installed.world_version)
                    if installed > local:
                        self.installed_version[world_id] = installed

            installed_version = self.installed_version.get(world_id, 'N/A')

            # Unfortunate
            self.world_name_to_id[world_name] = world_id

            max_version = max(available_versions, key=packaging.version.parse)
            world_info.append([
                world_name,
                installed_version,
                max_version,
                'Info/Set Version...',
            ])

        world_info = title_sorted(world_info, key=lambda x: x[0])
        return world_info

    def refresh(self):
        self.repositories.refresh()
        self.data_tables.update_row_data(self.data_tables, self.get_world_info())

    def do_install(self):
        print(repr(self.data_tables.get_row_checks()))
        for row in self.data_tables.get_row_checks():
            world_name = row[0]
            world_id = self.world_name_to_id[world_name]
            available_versions = self.available_versions[world_id]
            max_version = max(available_versions, key=packaging.version.parse)
            source = available_versions[max_version]
            print(f"Downloading {world_name} {max_version}")
            path = self.repositories.download_remote_world(source)
            print("Testing")
            loader = WorldSource(path, True, False)
            if world_id in AutoWorldRegister.world_types:
                # unload existing version
                del AutoWorldRegister.world_types[world_id]
            if not loader.load():
                print("Failed to load apworld")
                return

            # test_suite = unittest.defaultTestLoader.discover("test", top_level_dir=os.path.split(test.__file__)[0])
            # logging.info(test_suite)
            # import test.worlds
            # test_suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(test.worlds))
            # return test_suite




    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.rows = self.get_world_info()
        self.data_tables = MDDataTable(
            use_pagination=False,
            check=True,
            column_data=[
                ("Game", dp(80)),
                ("Installed Version", dp(30)),
                ("Newest Available", dp(30)),
                ("Set Version...", dp(40)),
            ],
            row_data=self.rows,
            sorted_on="Game",
            sorted_order="ASC",
            # elevation=200,
            rows_num=10000,
        )
        self.data_tables.bind(on_row_press=self.on_row_press)
        # self.data_tables.bind(on_check_press=self.on_check_press)
        screen = MDScreen()
        layout = MDBoxLayout(orientation='vertical')
        header = MDBoxLayout(orientation='horizontal', adaptive_height=True)
        header.add_widget(MDRaisedButton(text="Refresh", on_release=lambda x: self.refresh()))

        footer = MDBoxLayout(orientation='horizontal', adaptive_height=True)

        footer.add_widget(MDRaisedButton(text="Update"))
        footer.add_widget(MDRaisedButton(text="Install", on_release=lambda x: self.do_install()))
        footer.add_widget(MDRaisedButton(text="Uninstall"))
        layout.add_widget(header)
        layout.add_widget(self.data_tables)
        layout.add_widget(footer)
        screen.add_widget(layout)

        return screen

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''

        index = instance_row.index
        cols_num = len(instance_table.column_data)
        row_num = int(index/cols_num)
        col_num = index%cols_num

        cell_row = instance_table.table_data.view_adapter.get_visible_view(row_num*cols_num)

        # instance_table.background_color = self.theme_cls.primary_light
        # for id, widget in instance_row.ids.items():
        #     if id == "label":
        #         widget.color = self.theme_cls.primary_color

        # instance_row.add_widget(MDFlatButton(text="test"))
        #print(instance_table, instance_row, cell_row)
        #print(instance_row.text)
        if cols_num - 1 == col_num:
            # menu_items = [
            #     {
            #         "text": f"1.{i}.0",
            #         "viewclass": "OneLineListItem",

            #         "on_release": lambda x=f"Item {i}": print(x),
            #     } for i in range(3)
            # ]
            # MDDropdownMenu(
            #     caller=instance_row,
            #     items=menu_items,
            #     width_mult=2,
            #     opening_time=0,

            # ).open()
            from kivymd.uix.dialog import MDDialog
            from inspect import cleandoc
            world_name = cell_row.text
            world_id = self.world_name_to_id[world_name]
            available_versions = self.available_versions[world_id]

            install_text = [
                f'Install {version}' if version != self.installed_version.get(world_id, 'N/A') else f'Install {version} (Installed)' for version in available_versions
            ]
            disabled = [
                version == self.installed_version.get(world_id, 'N/A') for version in available_versions
            ]
            desc = cleandoc(self.descriptions[world_id]).replace('\n',' ')
            dialog = MDDialog(
                    type="simple",
                    # TODO: type="custom", would let us make our own buttons

                    text=f"[b]{cell_row.text}[/b]\n\n{desc}",
                    items = [
                       OneLineAvatarIconListItem(text=t, disabled=disabled[i]) for i, t in enumerate(install_text)
                    ],
                    buttons=[
                        MDRaisedButton(
                            text="Close",
                            on_release=lambda x: dialog.dismiss(force=True),
                        ),
                    ],
                    on_release=lambda x: print(x)
                )
            # dialog.add_widget(
            #         MDRaisedButton(
            #             text="v1.1.0",
            #             on_release=lambda x: dialog.dismiss(force=True))
            #     )
            dialog.open()
        # if cell_row.ids.check.state == 'normal':
        #     instance_table.table_data.select_all('normal')
        #     cell_row.ids.check.state = 'down'
        # else:
        #     cell_row.ids.check.state = 'normal'
        # instance_table.table_data.on_mouse_select(instance_row)
