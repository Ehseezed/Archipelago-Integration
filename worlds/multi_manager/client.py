import Utils
import os
import sys

# try:
#     if getattr(sys, "frozen", False):
#         bundle_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
#     else:
#         # Prefer the user's data path if available (Utils.user_path()), otherwise module dir.
#         try:
#             bundle_dir = Utils.user_path()
#         except Exception:
#             bundle_dir = os.path.abspath(os.path.dirname(__file__))
#
#     kivy_data_dir = os.path.join(bundle_dir, "data")
#     kivy_home = os.path.join(bundle_dir, "data")
#
#     print(f"Setting KIVY_DATA_DIR to: {kivy_data_dir}")
#     print(f"Setting KIVY_HOME to: {kivy_home}")
#
#     os.environ.setdefault("KIVY_DATA_DIR", kivy_data_dir)
#     os.environ.setdefault("KIVY_HOME", kivy_home)
#
# except Exception as e:
#     print(f"Failed to set KIVY_DATA_DIR to: {e}")
#     pass


from Launcher import identify, run_component

import re
import json
import logging
import stat
import subprocess
import tempfile
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, List
from urllib.parse import urlparse, unquote
from urllib.request import urlopen



from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown




APClient = None

KV = '''
<SlotRow>:
    size_hint_y: None
    height: dp(48)
    spacing: dp(8)
    padding: dp(8)
    Label:
        text: root.text
        halign: "left"
        valign: "middle"
        text_size: self.size
    Button:
        text: "Edit"
        size_hint_x: None
        width: dp(64)
        on_release: root.on_edit()
    Button:
        text: "Run"
        size_hint_x: None
        width: dp(64)
        on_release: root.on_run()
    Button:
        text: "Delete"
        size_hint_x: None
        width: dp(64)
        on_release: root.on_delete()

BoxLayout:
    orientation: "horizontal"

    BoxLayout:
        orientation: "vertical"
        size_hint_x: None
        width: dp(200)
        padding: dp(8)
        spacing: dp(8)

        BoxLayout:
            size_hint_y: None
            height: dp(48)
            spacing: dp(8)
            Button:
                text: "Add new multiworld"
                on_release: app.open_new_multiworld_dialog()

        ScrollView:
            do_scroll_x: False
            BoxLayout:
                id: mw_list
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(4)

    BoxLayout:
        orientation: "vertical"
        padding: dp(8)
        spacing: dp(8)

        BoxLayout:
            size_hint_y: None
            height: dp(56)
            spacing: dp(8)
            # Titlebar row: label expands, edit + slot controls inline on the right
            Label:
                id: toolbar
                text: "No multiworld selected"
                size_hint_x: 1
                valign: "middle"
                halign: "left"
                text_size: self.size

            Button:
                id: edit_mw_btn
                text: "Edit MW"
                size_hint_x: None
                width: dp(100)
                disabled: True
                on_release: app.open_edit_multiworld_dialog()
                
            Button:
                id: delete_mw_btn
                text: "Delete MW"
                size_hint_x: None
                width: dp(100)
                disabled: True
                on_release: app.confirm_delete_multiworld(app.selected_multiworld)

            Button:
                id: add_slot_btn
                text: "Add Slot"
                size_hint_x: None
                width: dp(100)
                disabled: True
                on_release: app.open_add_slot_dialog()

            # Button:
            #     id: debug_btn
            #     text: "Debug"
            #     size_hint_x: None
            #     width: dp(80)
            #     on_release: app.debug_print_multiworlds()

        BoxLayout:
            size_hint_y: None
            height: dp(56)
            spacing: dp(8)
            Widget:
                id: spinner
                size_hint: None, None
                size: (0, 0)
            Widget:
                id: _dummy
                size_hint: None, None
                size: (0, 0)
            Label:
                text: ""
            Widget:
                size_hint: None, None
                size: (0, 0)

        ScrollView:
            BoxLayout:
                id: slots_box
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(4)
'''


class SlotRow(BoxLayout):
    slot = ObjectProperty(None)
    text = StringProperty("")

    def on_edit(self):
        app = self.get_app()
        app.open_slot_editor(self.slot)

    def on_delete(self):
        app = self.get_app()
        app.confirm_delete_slot(self.slot)

    def on_run(self):
        app = self.get_app()
        try:
            app.run_clients(self.slot)
        except Exception as e:
            logging.exception(e)
            pass

    def get_app(self):
        return App.get_running_app()


def _make_apclient_enum(as_enum: bool = True):
    from worlds.LauncherComponents import components as _launcher_components, Type as _LauncherType
    members = {}
    comp_map = {}
    for comp in _launcher_components:
        if getattr(comp, "type", None) is _LauncherType.CLIENT:
            base = "".join(ch if ch.isalnum() else "_" for ch in comp.display_name).upper()
            if not base or base[0].isdigit():
                base = "C_" + base
            name = base
            i = 1
            while name in members:
                name = f"{base}_{i}"
                i += 1
            members[name] = comp.display_name
            comp_map[name] = comp

    if not members:
        members = {"NONE": "NONE"}

    if not as_enum:
        return {name: {"display_name": display, "component": comp_map.get(name)} for name, display in members.items()}

    EnumClass = Enum("APClient", members)
    for member in EnumClass:
        setattr(member, "component", comp_map.get(member.name))
    return EnumClass


APClient = _make_apclient_enum()


class ClientType(Enum):
    AP = auto()
    Steam_Game = auto()
    NonSteam_Game = auto()
    Patch_File = auto()
    Website = auto()
    Manual = auto()
    Default = -1


def _apclient_member_by_display(display_name):
    try:
        if not APClient:
            return None
        for m in APClient:
            try:
                if m.value == display_name:
                    return m
            except Exception:
                continue
    except Exception:
        pass
    return None


@dataclass
class ClientInfo:
    client_type: ClientType
    ap_client_type: Optional[APClient] = None
    launch_options: str = ""
    steam_app_id: Optional[str] = None
    executable_path: Optional[str] = None
    instructions: Optional[str] = None

    def __post_init__(self):
        if self.client_type == ClientType.AP and self.ap_client_type is None:
            logging.debug("Warning: No AP Client specified for AP client_type this has no actual function.")
        if self.client_type == ClientType.Steam_Game and not self.steam_app_id:
            logging.debug("Warning: No Steam Game specified this has no actual function.")
        if self.client_type == ClientType.NonSteam_Game and not self.executable_path:
            logging.debug("Warning: No Executable specified this has no actual function.")
        if self.client_type == ClientType.Patch_File and not self.executable_path:
            logging.debug("Warning: No file specified for Open_Patch_File client_type.")
        if self.client_type == ClientType.Website and not self.executable_path:
            logging.debug("Warning: No URL specified for Website client_type this has no actual function.")

        if self.client_type == ClientType.Default:
            logging.debug("Warning: ClientInfo created with Default client_type this has no actual function.")


@dataclass
class Slot:
    name: str
    Clients_to_open: List[ClientInfo] = field(default_factory=list)


@dataclass
class Multiworld:
    name: str
    url: Optional[str] = ""
    slots: List[Slot] = field(default_factory=list)


def normalize_to_local_path(selection: str, timeout=5) -> str:
    if not selection:
        raise ValueError("No selection given")

    parsed = urlparse(selection)
    if parsed.scheme in ("", "file"):
        path = unquote(parsed.path or selection)
        return os.path.abspath(path)

    try:
        import requests
        resp = requests.get(selection, stream=True, timeout=timeout)
        resp.raise_for_status()
        fd, tmp_path = tempfile.mkstemp(prefix="ap_exec_", suffix=os.path.splitext(parsed.path)[1] or "")
        os.close(fd)
        with open(tmp_path, "wb") as fh:
            for chunk in resp.iter_content(8192):
                fh.write(chunk)
        return tmp_path
    except Exception:
        return selection


def make_executable(path: str) -> None:
    try:
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except Exception:
        pass


def launch_local_executable(path: str, args: list[str] | None = None):
    local_path = normalize_to_local_path(path)
    if not os.path.isfile(local_path):
        raise FileNotFoundError(f"Executable not found: {local_path}")

    make_executable(local_path)
    argv = [local_path] + (args or [])
    subprocess.Popen(argv, close_fds=True)


def _looks_like_native_executable(path: str) -> bool:
    try:
        with open(path, "rb") as fh:
            hdr = fh.read(4)
        return hdr.startswith(b"\x7fELF") or hdr.startswith(b"#!")
    except Exception:
        return False


def launch_nonsteam_game(path: str, args: list | None = None) -> None:
    current_wd = os.getcwd()
    print(f'current_wd: {current_wd}')
    print(f'Path: {os.path.dirname(path)}')
    os.chdir(os.path.dirname(path))
    args = args or []
    local = normalize_to_local_path(path)
    if not os.path.isfile(local):
        raise FileNotFoundError(f"Executable not found: {local}")

    if _looks_like_native_executable(local):
        make_executable(local)
        try:
            subprocess.Popen([local] + args, close_fds=True)
            return
        except OSError as e:
            logging.exception(f"Direct execute failed for {local}: {e}")

    try:
        Utils.open_file(local)
    except Exception:
        try:
            subprocess.Popen(["xdg-open", local], close_fds=True)
        except Exception:
            logging.exception(f"Failed to open {local} with desktop handler")

    os.chdir(current_wd)
    return


class MultiManagerApp(App):
    dialog_new: Optional[Popup] = None
    dialog_slot: Optional[Popup] = None
    dialog_edit: Optional[Popup] = None
    dialog_add: Optional[Popup] = None
    _new_slot_type_dropdown = None

    def run_clients(self, slot: Slot):
        if not slot or not getattr(self, "selected_multiworld", None):
            return

        import subprocess

        try:
            from Launcher import get_exe, launch as launcher_launch
        except Exception:
            get_exe = None
            launcher_launch = None

        mw_url = (getattr(self.selected_multiworld, "url", None) or "").strip()
        slot_name = getattr(slot, "name", "")

        if mw_url and mw_url != "localhost":
            try:
                if re.fullmatch(r"\d+", mw_url):
                    mw_url = f"archipelago.gg:{mw_url}"
                elif re.fullmatch(r"(\d{1,3}\.){3}\d{1,3}:\d+|[A-Za-z0-9\.-]+:\d+", mw_url):
                    pass
                else:
                    room_marker = "/room/"
                    if room_marker in mw_url:
                        try:
                            import requests
                            parts = mw_url.split(room_marker, 1)[1].split("/")
                            room_id = parts[0]
                            base = mw_url.split(room_marker, 1)[0]
                            api_url = base.rstrip("/") + f"/api/room_status/{room_id}"
                            resp = requests.get(api_url, timeout=5)
                            resp.raise_for_status()
                            data = resp.json()
                            port = data.get("last_port")
                            if port:
                                mw_url = f"{base.split('://')[-1].split('/')[0]}:{port}"
                            else:
                                mw_url = ""
                        except Exception as e:
                            logging.warning(f"Failed to resolve room URL '{mw_url}': {e}")
                            mw_url = ""
                    else:
                        logging.debug(f"Unrecognized multiworld URL format: '{mw_url}'")
                        mw_url = ""
            except Exception as e:
                logging.exception(f"Unexpected error while resolving multiworld URL '{mw_url}': {e}")
                mw_url = ""

        for ci in slot.Clients_to_open:
            if ci.client_type == ClientType.Website:
                if ci.executable_path:
                    try:
                        Utils.open_file(ci.executable_path)
                    except Exception:
                        logging.exception(f"Failed to open website URL: {ci.executable_path}")
            if ci.client_type == ClientType.Steam_Game:
                if getattr(ci, "steam_app_id", None):
                    Utils.open_file(f'steam://rungameid/{ci.steam_app_id}')

            if ci.client_type == ClientType.NonSteam_Game:
                if ci.executable_path and os.path.exists(ci.executable_path):
                    try:
                        launch_nonsteam_game(ci.executable_path)
                    except Exception as e:
                        logging.exception(f"Failed to launch NonSteam_Game executable '{ci.executable_path}': {e}")

            if ci.client_type == ClientType.Manual:
                Utils.open_file(ci.instructions or "")

            if ci.client_type == ClientType.Patch_File:
                file, component = identify(ci.executable_path or "")
                if file and component:
                    run_component(component, file)

            if ci.client_type == ClientType.AP:
                comp = getattr(ci.ap_client_type, "component", None) if ci.ap_client_type else None
                if not comp:
                    logging.debug("No component attached to AP client choice; skipping.")
                    continue

                launch_args = [f"--connect archipelago://{slot_name}:None@{mw_url}", f'--url {mw_url}', ""]

                for arg in launch_args:
                    try:
                        print(f'Launching AP client for slot {slot_name} with component {comp} and arg {arg}')
                        run_component(comp, arg)
                        # if get_exe:
                        #     exe = get_exe(comp)
                        # else:
                        #     exe = None
                        #     if getattr(comp, "script_name", None):
                        #         exe = [comp.script_name]
                        #
                        # if not exe:
                        #     logging.warning(f"Unable to determine executable for component {comp}; skipping.")
                        #     continue
                        #
                        # cmd = [*exe, launch_args]
                        # logging.debug(cmd)
                        #
                        # if launcher_launch:
                        #     try:
                        #         launcher_launch(cmd, getattr(comp, "cli", False))
                        #     except Exception:
                        #         subprocess.Popen(cmd)
                        # else:
                        #     subprocess.Popen(cmd)
                    except Exception as e:
                        print(f'Error launching AP client for slot {slot_name} with component {comp}: {e}')
                        logging.exception(f"Failed to launch AP client for slot '{getattr(slot, 'name', '')}' with component {comp}")
                        continue

    def pick_file_via_dialog(self):
        import os

        if Utils.is_windows:
            default_paths = [
                os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Downloads"),
            ]
            filetypes = [
                ("Executable", ("*.exe", "*.bat", "*.com", "*")),
                ("All files", ("*",))
            ]
        else:
            default_paths = [
                os.path.join(os.path.expanduser("~"), "Documents"),
                os.path.join(os.path.expanduser("~"), "Downloads"),
            ]
            filetypes = [
                ("Executable", ("*",)),
                ("All files", ("*",))
            ]

        default_path = next((p for p in default_paths if os.path.exists(p)), None) or ""
        try:
            selection = Utils.open_filename("Select file", filetypes, suggest=default_path)
        except Exception:
            selection = None

        return selection

    def confirm_delete_multiworld(self, mw: Multiworld):
        if not mw:
            return

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=f"Delete multiworld '{mw.name}'?\nThis action cannot be undone."))

        btns = BoxLayout(size_hint_y=None, height=dp(40), spacing=8)
        popup = Popup(title="Confirm Delete Multiworld", content=content, size_hint=(None, None),
                      size=(dp(360), dp(160)))

        btn_cancel = Button(text="CANCEL", on_release=lambda *a: popup.dismiss())
        btn_delete = Button(text="DELETE", on_release=lambda *a: self._do_delete_multiworld(mw, popup))
        btns.add_widget(btn_cancel)
        btns.add_widget(btn_delete)
        content.add_widget(btns)

        popup.open()

    def _do_delete_multiworld(self, mw: Multiworld, popup: Popup):
        try:
            if getattr(self, "multiworlds", None) and mw in self.multiworlds:
                self.multiworlds.remove(mw)
        except Exception:
            pass

        # If the deleted multiworld was selected, clear selection and disable controls
        try:
            if getattr(self, "selected_multiworld", None) is mw:
                self.selected_multiworld = None
                try:
                    self.root.ids.edit_mw_btn.disabled = True
                except Exception:
                    pass
                try:
                    self.root.ids.add_slot_btn.disabled = True
                except Exception:
                    pass
                try:
                    # disable Delete MW button as well
                    self.root.ids.delete_mw_btn.disabled = True
                except Exception:
                    pass
        except Exception:
            pass

        try:
            popup.dismiss()
        except Exception:
            pass
        try:
            serialized = self._serialize_multiworlds()
            Utils.persistent_store("multi_manager_data", "multiworlds", serialized, force_store=True)
        except Exception:
            pass

        try:
            self.populate_multiworld_list()
            self.refresh_slots_view()
        except Exception:
            pass

    def confirm_delete_slot(self, slot: Slot):
        if not slot or not getattr(self, "selected_multiworld", None):
            return

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=f"Delete slot '{slot.name}'?\nThis action cannot be undone."))

        btns = BoxLayout(size_hint_y=None, height=dp(40), spacing=8)
        popup = Popup(title="Confirm Delete Slot", content=content, size_hint=(None, None),
                      size=(dp(360), dp(160)))

        btn_cancel = Button(text="CANCEL", on_release=lambda *a: popup.dismiss())
        btn_delete = Button(text="DELETE", on_release=lambda *a: self._do_delete_slot(slot, popup))
        btns.add_widget(btn_cancel)
        btns.add_widget(btn_delete)
        content.add_widget(btns)

        popup.open()

    def _do_delete_slot(self, slot: Slot, popup: Popup):
        try:
            if getattr(self, "selected_multiworld", None) and slot in self.selected_multiworld.slots:
                self.selected_multiworld.slots.remove(slot)
        except Exception:
            pass

        if getattr(self, "_editor_slot", None) is slot:
            self._close_slot_editor()

        try:
            popup.dismiss()
        except Exception:
            pass
        self.refresh_slots_view()

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        self.multiworlds: List[Multiworld] = []
        self.selected_multiworld: Optional[Multiworld] = None

        try:
            Utils.logging.debug(self._deserialize_multiworlds(Utils.persistent_load().get("multi_manager_data", {}).get("multiworlds", [])))
            self.multiworlds = self._deserialize_multiworlds(Utils.persistent_load().get("multi_manager_data", {}).get("multiworlds", []))
        except Exception as e:
            Utils.logging.exception(f"Failed to load multiworld data: {e}")
            pass


        global APClient
        try:
            APClient = _make_apclient_enum()
        except Exception:
            APClient = None

        try:
            self.root.ids.edit_mw_btn.disabled = True
        except Exception:
            pass

        try:
            self.root.ids.add_slot_btn.disabled = True
        except Exception:
            pass
        self.populate_multiworld_list()

    def open_new_multiworld_dialog(self):
        if self.dialog_new:
            self.dialog_new.open()
            return

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self._new_name = TextInput(hint_text="Multiworld name", multiline=False,
                                   size_hint_y=None, height=dp(40), font_size=dp(16))
        self._new_url = TextInput(hint_text="[ip]:[port]/webpage URL (optional)", multiline=False,
                                  size_hint_y=None, height=dp(40), font_size=dp(16))
        content.add_widget(self._new_name)
        content.add_widget(self._new_url)
        btns = BoxLayout(size_hint_y=None, height=dp(40), spacing=8)
        btn_cancel = Button(text="CANCEL", on_release=lambda *a: self.dialog_new.dismiss())
        btn_create = Button(text="CREATE", on_release=self.create_multiworld_from_dialog)
        btns.add_widget(btn_cancel)
        btns.add_widget(btn_create)
        content.add_widget(btns)

        self.dialog_new = Popup(title="Create Multiworld", content=content, size_hint=(None, None),
                                size=(dp(360), dp(220)))
        self.dialog_new.open()

    def create_multiworld_from_dialog(self, *args):
        name = getattr(self, "_new_name", None) and self._new_name.text.strip()
        url = getattr(self, "_new_url", None) and self._new_url.text.strip()
        if not name:
            if self.dialog_new:
                self.dialog_new.dismiss()
            return
        mw = Multiworld(name=name, url=url or "")
        self.multiworlds.append(mw)
        if self.dialog_new:
            self.dialog_new.dismiss()
            self.dialog_new = None
        self.populate_multiworld_list()
        self.select_multiworld(mw)

    def open_edit_multiworld_dialog(self):
        if not self.selected_multiworld:
            return
        if self.dialog_edit:
            self.dialog_edit.open()
            return

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self._edit_name = TextInput(text=self.selected_multiworld.name, hint_text="Multiworld name", multiline=False,
                                    size_hint_y=None, height=dp(40), font_size=dp(16))
        self._edit_url = TextInput(text=(self.selected_multiworld.url or ""), hint_text="Multiworld URL (optional)",
                                   multiline=False,
                                   size_hint_y=None, height=dp(40), font_size=dp(16))
        content.add_widget(self._edit_name)
        content.add_widget(self._edit_url)
        btns = BoxLayout(size_hint_y=None, height=dp(40), spacing=8)
        btn_cancel = Button(text="CANCEL", on_release=lambda *a: self.dialog_edit.dismiss())
        btn_save = Button(text="SAVE", on_release=self.save_edited_multiworld)
        btns.add_widget(btn_cancel)
        btns.add_widget(btn_save)
        content.add_widget(btns)

        self.dialog_edit = Popup(title="Edit Multiworld", content=content, size_hint=(None, None),
                                 size=(dp(360), dp(220)))
        self.dialog_edit.open()

    def save_edited_multiworld(self, *args):
        if not self.selected_multiworld:
            if self.dialog_edit:
                self.dialog_edit.dismiss()
            return
        name = getattr(self, "_edit_name", None) and self._edit_name.text.strip()
        url = getattr(self, "_edit_url", None) and self._edit_url.text.strip()
        if not name:
            if self.dialog_edit:
                self.dialog_edit.dismiss()
            return
        self.selected_multiworld.name = name
        self.selected_multiworld.url = url or ""
        if self.dialog_edit:
            self.dialog_edit.dismiss()
            self.dialog_edit = None
        self.populate_multiworld_list()
        self.select_multiworld(self.selected_multiworld)

    def populate_multiworld_list(self, filter_text: str = ""):
        mw_list = self.root.ids.mw_list
        mw_list.clear_widgets()
        for mw in self.multiworlds:
            if filter_text and filter_text.lower() not in mw.name.lower():
                continue
            item = Button(text=mw.name, size_hint_y=None, height=dp(40))
            item.multiworld = mw
            item.bind(on_release=lambda inst, mw=mw: self.select_multiworld(mw))
            mw_list.add_widget(item)

    def select_multiworld(self, mw: Optional[Multiworld]):
        self.selected_multiworld = mw
        try:
            # update toolbar text
            if mw:
                try:
                    self.root.ids.toolbar.text = f"{mw.name}"
                except Exception:
                    pass
            else:
                try:
                    self.root.ids.toolbar.text = "No multiworld selected"
                except Exception:
                    pass
        except Exception:
            pass

        try:
            # enable/disable controls according to selection
            try:
                self.root.ids.edit_mw_btn.disabled = (mw is None)
            except Exception:
                pass
            try:
                self.root.ids.add_slot_btn.disabled = (mw is None)
            except Exception:
                pass
            try:
                # new Delete MW button toggle
                self.root.ids.delete_mw_btn.disabled = (mw is None)
            except Exception:
                pass
        except Exception:
            pass

        try:
            self.root.ids.edit_mw_btn.disabled = False if mw else True
        except Exception:
            pass
        try:
            self.root.ids.add_slot_btn.disabled = False if mw else True
        except Exception:
            pass
        self.refresh_slots_view()

    def refresh_slots_view(self):
        slots_box = self.root.ids.slots_box
        slots_box.clear_widgets()
        if not self.selected_multiworld:
            return
        for idx, slot in enumerate(self.selected_multiworld.slots):
            row = SlotRow()
            row.slot = slot
            row.text = f"{idx + 1}: {slot.name}: {len(slot.Clients_to_open)} function(s)"
            slots_box.add_widget(row)

    def open_add_slot_dialog(self):
        if getattr(self, "dialog_add", None):
            self.dialog_add.open()
            return

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self._new_slot_name = TextInput(hint_text="Slot name", multiline=False,
                                        size_hint_y=None, height=dp(40), font_size=dp(16))

        # Client type selector (button + dropdown). _on_add_slot_create expects _new_slot_type.text
        self._new_slot_type = Button(text="Client Type", size_hint_y=None, height=dp(40))
        self._new_slot_type_dropdown = DropDown()
        for opt in (n for n in ClientType.__members__ if n != "Default"):
            b = Button(text=opt, size_hint_y=None, height=dp(40))
            b.bind(on_release=lambda btn, val=opt: self._new_slot_type_dropdown.select(val))
            self._new_slot_type_dropdown.add_widget(b)
        self._new_slot_type.bind(on_release=self._new_slot_type_dropdown.open)
        self._new_slot_type_dropdown.bind(on_select=lambda inst, val: setattr(self._new_slot_type, "text", val))

        content.add_widget(self._new_slot_name)
        content.add_widget(self._new_slot_type)

        btns = BoxLayout(size_hint_y=None, height=dp(40), spacing=8)
        btn_cancel = Button(text="CANCEL", on_release=lambda *a: self._dismiss_add_dialog())
        btn_create = Button(text="CREATE", on_release=self._on_add_slot_create)
        btns.add_widget(btn_cancel)
        btns.add_widget(btn_create)
        content.add_widget(btns)

        self.dialog_add = Popup(title="Create Slot", content=content, size_hint=(None, None), size=(dp(420), dp(220)))
        self.dialog_add.open()

    def open_add_slot_details_dialog(self, slot_type: ClientType, name: str, mode: str = "SPEC"):
        if self.dialog_add:
            self.dialog_add.dismiss()

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self._details_slot_type = slot_type
        self._details_slot_name = name

        if mode == "AP":
            self._ap_select_btn = Button(text="Select AP client", size_hint_y=None, height=dp(40), font_size=dp(16))
            self._ap_select_dropdown = DropDown()
            try:
                if APClient:
                    ap_members = [m for m in APClient]
                else:
                    ap_members = []
            except Exception:
                ap_members = []
            if not ap_members:
                ap_members = [None]

            for member in ap_members:
                if member is None:
                    b = Button(text="NONE", size_hint_y=None, height=dp(40))
                    b.bind(on_release=lambda btn, m=None: self._ap_select_dropdown.select(m))
                else:
                    b = Button(text=member.value, size_hint_y=None, height=dp(40))
                    b.bind(on_release=lambda btn, m=member: self._ap_select_dropdown.select(m))
                self._ap_select_dropdown.add_widget(b)

            def _on_ap_selected(inst, val):
                try:
                    if val is None:
                        self._ap_select_btn.text = "NONE"
                        self._ap_select_btn._selected_ap = None
                    else:
                        self._ap_select_btn.text = val.value
                        self._ap_select_btn._selected_ap = val
                except Exception:
                    pass

            self._ap_select_btn.bind(on_release=self._ap_select_dropdown.open)
            self._ap_select_dropdown.bind(on_select=_on_ap_selected)
            content.add_widget(self._ap_select_btn)
        else:
            if slot_type == ClientType.Steam_Game:
                hint = "Steam App ID"
            elif slot_type == ClientType.Website:
                hint = "Website URL"
            else:
                hint = "Primary spec (steam id / exe path / instructions)"

            row = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height=dp(40))
            self._details_spec_input = TextInput(hint_text=hint, multiline=False,
                                                 size_hint_y=None, height=dp(40), font_size=dp(16))
            row.add_widget(self._details_spec_input)

            # Keep Browse for NonSteam and Patch/File types only — DO NOT include Steam_Game or Website
            if slot_type in (ClientType.NonSteam_Game, ClientType.Patch_File):
                btn_browse = Button(text="Browse", size_hint_x=None, width=dp(100), size_hint_y=None, height=dp(40))

                def _on_browse(_inst):
                    try:
                        selection = self.pick_file_via_dialog()
                    except Exception:
                        selection = None
                    if selection:
                        try:
                            self._details_spec_input.text = selection
                        except Exception:
                            pass

                btn_browse.bind(on_release=_on_browse)
                row.add_widget(btn_browse)

            content.add_widget(row)

        btns = BoxLayout(size_hint_y=None, height=dp(40), spacing=8)
        btn_cancel = Button(text="CANCEL", on_release=lambda *a: self._dismiss_add_dialog())
        btn_create = Button(text="CREATE", on_release=self._on_details_create)
        btns.add_widget(btn_cancel)
        btns.add_widget(btn_create)
        content.add_widget(btns)

        self.dialog_add_details = Popup(title=f"Add Slot details ({slot_type.name})", content=content,
                                        size_hint=(None, None), size=(dp(420), dp(220)))
        self.dialog_add_details.open()

    def _on_add_slot_create(self, *args):
        from kivy.clock import Clock

        name = getattr(self, "_new_slot_name", None) and self._new_slot_name.text.strip()
        if not name:
            self._dismiss_add_dialog()
            return

        type_text = getattr(self, "_new_slot_type", None) and self._new_slot_type.text.strip()
        slot_type = ClientType.Default
        if type_text and type_text in ClientType.__members__:
            slot_type = ClientType[type_text]

        self._dismiss_add_dialog()

        if slot_type == ClientType.AP:
            self.open_add_slot_details_dialog(slot_type, name, mode="AP")
            return

        if slot_type == ClientType.Manual:
            self.open_add_slot_details_dialog(slot_type, name, mode="SPEC")
            return

        if slot_type in (ClientType.Steam_Game, ClientType.Website):
            self.open_add_slot_details_dialog(slot_type, name, mode="SPEC")
            return

        if slot_type in (ClientType.NonSteam_Game, ClientType.Patch_File):
            # Ensure the file dialog is opened on the main/Kivy thread.
            def open_picker(dt):
                try:
                    selection = self.pick_file_via_dialog()
                except Exception:
                    selection = None

                if selection:
                    try:
                        self._finalize_create_slot(slot_type, name, spec=selection)
                    except Exception:
                        pass

            Clock.schedule_once(open_picker, 0)
            return

        if slot_type == ClientType.Default:
            content = BoxLayout(orientation='vertical', spacing=10, padding=10)
            content.add_widget(
                Label(text="Please select a client type before creating a slot.", size_hint_y=None, height=dp(60)))
            btn_ok = Button(text="OK", size_hint_y=None, height=dp(40))
            content.add_widget(btn_ok)
            popup = Popup(title="Select Client Type", content=content, size_hint=(None, None), size=(dp(420), dp(140)))
            btn_ok.bind(on_release=lambda *a: popup.dismiss())
            popup.open()
            return

        self._finalize_create_slot(slot_type, name, spec=None)

    def _on_details_create(self, *args):
        slot_type = getattr(self, "_details_slot_type", ClientType.Default)
        name = getattr(self, "_details_slot_name", None)
        spec = None
        ap_choice_name = None
        try:
            if slot_type == ClientType.AP:
                ap_choice_name = getattr(self, "_ap_select_btn", None) and self._ap_select_btn.text
                if ap_choice_name == "Select AP client":
                    ap_choice_name = None
            else:
                spec = getattr(self, "_details_spec_input", None) and self._details_spec_input.text.strip()
        except Exception:
            pass

        self._finalize_create_slot(slot_type, name, spec=spec, ap_choice_name=ap_choice_name)
        self._dismiss_add_dialog()

    def _finalize_create_slot(self, slot_type: ClientType, name: str, spec: Optional[str] = None,
                              ap_choice_name: Optional[str] = None):
        try:
            new_slot = Slot(name=name)
            if not hasattr(new_slot, "Clients_to_open") or new_slot.Clients_to_open is None:
                new_slot.Clients_to_open = []
        except Exception:
            return

        try:
            if getattr(self, "selected_multiworld", None) is None:
                return
            self.selected_multiworld.slots.append(new_slot)
        except Exception:
            return

        try:
            if slot_type == ClientType.AP:
                ap_enum_member = None
                try:
                    if ap_choice_name:
                        ap_enum_member = _apclient_member_by_display(ap_choice_name)
                except Exception:
                    ap_enum_member = None

                ci = self._make_clientinfo_for_type(ClientType.AP, None)
                if ap_enum_member:
                    ci.ap_client_type = ap_enum_member
            else:
                ci = self._make_clientinfo_for_type(slot_type, spec)
            if ci and ci.client_type != ClientType.Default:
                self.add_client_to_slot(new_slot, ci.client_type, ap=ci.ap_client_type,
                                        launch=ci.launch_options, steam=ci.steam_app_id,
                                        exe=ci.executable_path, instr=ci.instructions)
                try:
                    pass
                except Exception:
                    pass
            else:
                try:
                    self.add_client_to_slot(new_slot, ClientType.Default)
                except Exception:
                    pass
        except Exception:
            pass

    def _dismiss_add_dialog(self):
        if getattr(self, "dialog_add", None):
            try:
                self.dialog_add.dismiss()
            except Exception:
                pass
            self.dialog_add = None
        if getattr(self, "dialog_add_details", None):
            try:
                self.dialog_add_details.dismiss()
            except Exception:
                pass
            self.dialog_add_details = None
        self._new_slot_type_dropdown = None

    def _make_clientinfo_for_type(self, ct: ClientType, spec: Optional[str]) -> ClientInfo:
        if ct == ClientType.AP:
            ap_choice = None
            try:
                if APClient:
                    ap_choice = None
            except Exception:
                ap_choice = None
            return ClientInfo(client_type=ClientType.AP, ap_client_type=ap_choice)
        if ct == ClientType.Steam_Game:
            return ClientInfo(client_type=ClientType.Steam_Game, steam_app_id=(spec or ""))
        if ct == ClientType.NonSteam_Game:
            return ClientInfo(client_type=ClientType.NonSteam_Game, executable_path=(spec or ""))
        if ct == ClientType.Patch_File:
            return ClientInfo(client_type=ClientType.Patch_File, executable_path=(spec or ""))
        if ct == ClientType.Website:
            return ClientInfo(client_type=ClientType.Website, executable_path=(spec or ""))
        if ct == ClientType.Manual:
            return ClientInfo(client_type=ClientType.Manual, instructions=(spec or ""))
        return ClientInfo(client_type=ClientType.Default)

    def create_slot_from_dialog(self, *args):
        if not getattr(self, "selected_multiworld", None):
            self._dismiss_add_dialog()
            return
        name = getattr(self, "_new_slot_name", None) and self._new_slot_name.text.strip()
        type_text = getattr(self, "_new_slot_type", None) and self._new_slot_type.text.strip()
        if not name:
            self._dismiss_add_dialog()
            return
        slot_type = ClientType.Default
        if type_text and type_text in ClientType.__members__:
            slot_type = ClientType[type_text]

        try:
            new_slot = Slot(name=name)
            if not hasattr(new_slot, "Clients_to_open") or new_slot.Clients_to_open is None:
                new_slot.Clients_to_open = []
        except Exception:
            self._dismiss_add_dialog()
            return

        try:
            self.selected_multiworld.slots.append(new_slot)
        except Exception:
            self._dismiss_add_dialog()
            return

        try:
            ci = self._make_clientinfo_for_type(slot_type, None)
            if ci and ci.client_type != ClientType.Default:
                self.add_client_to_slot(new_slot, ci.client_type, ap=ci.ap_client_type,
                                        launch=ci.launch_options, steam=ci.steam_app_id,
                                        exe=ci.executable_path, instr=ci.instructions)
        except Exception:
            pass

        self._dismiss_add_dialog()
        self.refresh_slots_view()

    def add_client_to_slot(self, slot: Slot, type: ClientType, ap: Optional[APClient] = None, launch: str = "",
                           steam: str = "", exe: str = "", instr: str = ""):
        if not slot or not type:
            return
        try:
            client = ClientInfo(client_type=type, ap_client_type=ap, launch_options=launch, steam_app_id=steam,
                                executable_path=exe, instructions=instr)
            slot.Clients_to_open.append(client)
            self.refresh_slots_view()
        except Exception:
            return

    def open_slot_editor(self, slot: Slot):
        if self.dialog_slot:
            self.dialog_slot.open()
            return

        self._editor_slot = slot

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self._slot_name_input = TextInput(text=getattr(slot, "name", ""), multiline=False,
                                          size_hint_y=None, height=dp(40), font_size=dp(16))
        content.add_widget(self._slot_name_input)

        self._slot_clients_list = BoxLayout(orientation='vertical', spacing=6, size_hint_y=None)
        self._slot_clients_list.bind(minimum_height=self._slot_clients_list.setter('height'))

        def _build_clients_list():
            self._slot_clients_list.clear_widgets()
            clients = getattr(slot, "Clients_to_open", []) or []
            for i, ci in enumerate(clients):
                row = BoxLayout(size_hint_y=None, height=dp(40), spacing=6)
                ct = getattr(ci, "client_type", None)
                ct_text = ct.name if ct else "Unknown"
                extra = ""
                # print(f'RIGHT HERE is the  stuff ci', ci)
                if getattr(ci, "executable_path", None):
                    if ci.client_type == ClientType.NonSteam_Game:
                        extra = os.path.basename(ci.executable_path)
                        extra = extra.split(".")[0]


                    elif ci.client_type == ClientType.Patch_File:

                        basename = os.path.basename(ci.executable_path or "")

                        # locate the last "P<digits>_" occurrence

                        last_match = None

                        for m in re.finditer(r'P\d+_', basename):
                            last_match = m

                        if last_match:

                            remainder = basename[last_match.end():]

                            remainder_no_ext = os.path.splitext(remainder)[0]

                            tokens = remainder_no_ext.split('_')

                            # Heuristic: if the last token is a long alphanumeric blob (likely a random id),

                            # drop it; otherwise keep the full remainder (so underscores inside names are preserved).

                            extra = remainder_no_ext

                            if len(tokens) >= 2:

                                last_tok = tokens[-1]

                                if len(last_tok) >= 8 and re.fullmatch(r'[A-Za-z0-9]+', last_tok) and any(
                                        ch.isdigit() for ch in last_tok):
                                    extra = '_'.join(tokens[:-1])

                                    print("Displayed name: " + extra)

                            if not extra:
                                extra = os.path.splitext(basename)[0] or "Unknown_patch"

                        else:

                            # fallback: filename without extension or a default label

                            extra = os.path.splitext(basename)[0] or "Unknown_patch"

                    elif ci.client_type == ClientType.Website:
                        try:
                            import html
                            website = urlopen(ci.executable_path).read()
                            # print(f'RIGHT HERE is website data', website)
                            title = str(website).split("<title>")[1].split("</title>")[0]
                            title = html.unescape(title)
                        except ValueError:
                            title = "Webpage Title Not Found"

                        extra = title

                    else:
                        extra = ci.executable_path

                elif getattr(ci, "steam_app_id", None):
                    try:
                        app_id = json.load(urlopen(f'https://store.steampowered.com/api/appdetails?appids={ci.steam_app_id}'))
                        app_id = app_id[ci.steam_app_id]["data"]["name"]
                    except Exception:
                        app_id = ci.steam_app_id

                    extra = app_id
                elif getattr(ci, "instructions", None):
                    extra = ci.instructions
                elif getattr(ci, "ap_client_type", None):
                    extra = getattr(ci.ap_client_type, "name", "")
                lbl = Label(text=f"{ct_text}{(': ' + extra) if extra else ''}", halign="left", valign="middle",
                            text_size=(None, dp(40)))
                row.add_widget(lbl)
                btn_edit = Button(text="Edit", size_hint_x=None, width=dp(64))
                btn_remove = Button(text="Remove", size_hint_x=None, width=dp(80))
                btn_edit.bind(on_release=lambda inst, idx=i: self._open_client_edit_dialog(slot, idx))

                def _remove(inst, idx=i):
                    try:
                        clients = getattr(slot, "Clients_to_open", []) or []
                        if 0 <= idx < len(clients):
                            clients.pop(idx)
                            if getattr(self, "_slot_clients_list_builder", None):
                                self._slot_clients_list_builder()
                            self.refresh_slots_view()
                    except Exception:
                        pass

                btn_remove.bind(on_release=_remove)
                row.add_widget(btn_edit)
                row.add_widget(btn_remove)
                self._slot_clients_list.add_widget(row)

        _build_clients_list()
        content.add_widget(self._slot_clients_list)

        btns = BoxLayout(size_hint_y=None, height=dp(40), spacing=8)
        btn_add = Button(text="Add Client", size_hint_x=None, width=dp(120))
        btn_cancel = Button(text="CANCEL")
        btn_save = Button(text="SAVE")

        btn_add.bind(on_release=lambda *a: self._open_client_edit_dialog(slot, None))
        btn_cancel.bind(on_release=lambda *a: (self._close_slot_editor()))
        btn_save.bind(on_release=lambda *a: self.save_slot_edits(slot))

        btns.add_widget(btn_add)
        btns.add_widget(btn_cancel)
        btns.add_widget(btn_save)
        content.add_widget(btns)

        self.dialog_slot = Popup(title=f"Edit slot ({getattr(slot, 'name', '')})", content=content,
                                 size_hint=(None, None),
                                 size=(dp(480), dp(360)))
        self.dialog_slot.open()

        self._slot_clients_list_builder = _build_clients_list

    def _open_client_edit_dialog(self, slot: Slot, client_index: Optional[int]):
        if getattr(self, "dialog_slot_client", None):
            self.dialog_slot_client.open()
            return

        existing_ci = None
        if client_index is not None:
            clients = getattr(slot, "Clients_to_open", []) or []
            if 0 <= client_index < len(clients):
                existing_ci = clients[client_index]

        from kivy.clock import Clock
        import threading

        def _create_spec_row(initial_text: str = "", show_browse: bool = True):
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=8)
            ti = TextInput(text=initial_text, multiline=False)
            row.add_widget(ti)

            if show_browse:
                btn_browse = Button(text="Browse...", size_hint_x=None, width=dp(100))

                def _on_browse(_inst):
                    def worker():
                        try:
                            selection = self.pick_file_via_dialog()
                        except Exception:
                            selection = None

                        def finalize(dt):
                            if selection:
                                try:
                                    ti.text = selection
                                except Exception:
                                    pass

                        Clock.schedule_once(finalize, 0)

                    threading.Thread(target=worker, daemon=True).start()

                btn_browse.bind(on_release=_on_browse)
                row.add_widget(btn_browse)

            return row, ti

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        if existing_ci:
            lbl = Label(text=f"Client Type: {existing_ci.client_type.name}", size_hint_y=None, height=dp(30))
            content.add_widget(lbl)

            if existing_ci.client_type in (ClientType.AP,):
                self._client_ap_select_btn = Button(text="Select AP client", size_hint_y=None, height=dp(40))
                self._client_ap_select_dropdown = DropDown()

                members = []
                try:
                    if APClient:
                        members = [m for m in APClient]
                except Exception:
                    members = []

                for member in members:
                    b = Button(text=member.value, size_hint_y=None, height=dp(40))
                    b.bind(on_release=lambda btn, m=member: self._client_ap_select_dropdown.select(m))
                    self._client_ap_select_dropdown.add_widget(b)

                def _on_client_ap_selected(inst, val):
                    try:
                        if val is None:
                            self._client_ap_select_btn.text = "NONE"
                            self._client_ap_select_btn._selected_ap = None
                        else:
                            self._client_ap_select_btn.text = val.value
                            self._client_ap_select_btn._selected_ap = val
                    except Exception:
                        pass

                self._client_ap_select_dropdown.bind(on_select=_on_client_ap_selected)
                self._client_ap_select_btn.bind(on_release=self._client_ap_select_dropdown.open)

                self._client_ap_select_btn._selected_ap = getattr(existing_ci, "ap_client_type", None)
                if getattr(existing_ci, "ap_client_type", None):
                    try:
                        self._client_ap_select_btn.text = existing_ci.ap_client_type.value
                    except Exception:
                        pass
                content.add_widget(self._client_ap_select_btn)
            else:
                initial = getattr(existing_ci, "executable_path", "") or getattr(existing_ci, "steam_app_id",
                                                                                 "") or getattr(existing_ci,
                                                                                                "instructions", "")
                if initial == None:
                    initial = ""

                if existing_ci.client_type in (ClientType.Steam_Game, ClientType.Website):
                    ti = TextInput(text=initial, multiline=False, size_hint_y=None, height=dp(40))
                    content.add_widget(ti)
                    self._client_spec_input = ti
                else:
                    show_browse = existing_ci.client_type in (ClientType.NonSteam_Game, ClientType.Patch_File)
                    spec_row, spec_input = _create_spec_row(initial, show_browse=show_browse)
                    content.add_widget(spec_row)
                    self._client_spec_input = spec_input
        else:
            self._client_type_btn = Button(text="Client Type", size_hint_y=None, height=dp(40))
            self._client_type_dropdown = DropDown()
            for opt in (n for n in ClientType.__members__ if n != "Default"):
                b = Button(text=opt, size_hint_y=None, height=dp(40))
                b.bind(on_release=lambda btn, val=opt: self._client_type_dropdown.select(val))
                self._client_type_dropdown.add_widget(b)
            self._client_type_btn.bind(on_release=self._client_type_dropdown.open)
            spec_holder = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height=dp(40))
            spec_row, spec_input = _create_spec_row("", show_browse=False)
            spec_holder.add_widget(spec_row)
            self._client_spec_input = spec_input
            spec_holder.size_hint_x = 1

            def _on_type_selected(inst, value):
                try:
                    print(f"Selected client type: {value}")
                    # update selected text on the button
                    self._client_type_btn.text = value

                    # rebuild the spec area depending on selected client type
                    try:
                        spec_holder.clear_widgets()
                    except Exception:
                        pass

                    if value == "Steam_Game":
                        ti = TextInput(text="", multiline=False, size_hint_y=None, height=dp(40))
                        ti.hint_text = "Steam App ID"
                        spec_holder.add_widget(ti)
                        self._client_spec_input = ti
                        # clear any AP selectors
                        self._client_ap_select_btn = None
                        self._client_ap_select_dropdown = None

                    elif value == "Website":
                        ti = TextInput(text="", multiline=False, size_hint_y=None, height=dp(40))
                        ti.hint_text = "Website URL"
                        spec_holder.add_widget(ti)
                        self._client_spec_input = ti
                        self._client_ap_select_btn = None
                        self._client_ap_select_dropdown = None

                    elif value == "AP":
                        # create AP selector button + dropdown
                        btn = Button(text="Select AP client", size_hint_y=None, height=dp(40))
                        dropdown = DropDown()
                        members = []
                        try:
                            if APClient:
                                members = [m for m in APClient]
                        except Exception:
                            members = []

                        if not members:
                            b = Button(text="NONE", size_hint_y=None, height=dp(40))
                            b.bind(on_release=lambda btn, m=None: dropdown.select(m))
                            dropdown.add_widget(b)
                        else:
                            for member in members:
                                b = Button(text=member.value, size_hint_y=None, height=dp(40))
                                b.bind(on_release=lambda btn, m=member: dropdown.select(m))
                                dropdown.add_widget(b)

                        def _on_ap_selected(inst2, val):
                            try:
                                if val is None:
                                    btn.text = "NONE"
                                    btn._selected_ap = None
                                else:
                                    btn.text = val.value
                                    btn._selected_ap = val
                            except Exception:
                                pass

                        dropdown.bind(on_select=_on_ap_selected)
                        btn.bind(on_release=dropdown.open)
                        btn._selected_ap = None
                        spec_holder.add_widget(btn)
                        self._client_ap_select_btn = btn
                        self._client_ap_select_dropdown = dropdown
                        self._client_spec_input = None

                    else:
                        # default: spec input with browse button
                        spec_row, spec_input = _create_spec_row("", show_browse=True)
                        spec_holder.add_widget(spec_row)
                        self._client_spec_input = spec_input
                        self._client_ap_select_btn = None
                        self._client_ap_select_dropdown = None

                except Exception:
                    pass

            self._client_type_dropdown.bind(on_select=_on_type_selected)

            content.add_widget(self._client_type_btn)
            content.add_widget(spec_holder)

        btns = BoxLayout(size_hint_y=None, height=dp(40), spacing=8)
        btn_cancel = Button(text="CANCEL")
        btn_save = Button(text="SAVE")
        btn_cancel.bind(on_release=lambda *a: self._dismiss_client_dialog())
        btn_save.bind(on_release=lambda *a: self._on_client_dialog_save(slot, client_index))
        btns.add_widget(btn_cancel)
        btns.add_widget(btn_save)
        content.add_widget(btns)

        title = "Edit Client" if existing_ci else "Add Client"
        self.dialog_slot_client = Popup(title=title, content=content, size_hint=(None, None),
                                        size=(dp(420), dp(220)))
        self.dialog_slot_client.open()

        if not getattr(self, "_client_ap_select_btn", None):
            self._client_ap_select_btn = None
        if not getattr(self, "_client_spec_input", None):
            self._client_spec_input = getattr(self, "_client_spec_input", None)

    def _on_client_dialog_save(self, slot: Slot, client_index: Optional[int]):
        type_text = getattr(self, "_client_type_btn", None) and self._client_type_btn.text
        chosen_type = ClientType.Default
        if type_text and type_text in ClientType.__members__:
            chosen_type = ClientType[type_text]

        spec = None
        ap_choice = None
        if chosen_type == ClientType.AP:
            try:
                if getattr(self, "_client_ap_select_btn", None) and getattr(self._client_ap_select_btn, "_selected_ap", None):
                    ap_choice = getattr(self._client_ap_select_btn, "_selected_ap", None)
                elif getattr(self, "_ap_select_btn", None) and getattr(self._ap_select_btn, "_selected_ap", None):
                    ap_choice = getattr(self._ap_select_btn, "_selected_ap", None)
            except Exception:
                ap_choice = None
        else:
            try:
                spec = getattr(self, "_client_spec_input", None) and self._client_spec_input.text.strip()
            except Exception:
                spec = None

        try:
            ci = self._make_clientinfo_for_type(chosen_type, spec)
            if chosen_type == ClientType.AP and ap_choice:
                ci.ap_client_type = ap_choice
        except Exception:
            ci = None

        if ci:
            try:
                if client_index is None:
                    slot.Clients_to_open.append(ci)
                else:
                    clients = getattr(slot, "Clients_to_open", []) or []
                    if 0 <= client_index < len(clients):
                        clients[client_index] = ci
            except Exception:
                pass

        if getattr(self, "_slot_clients_list_builder", None):
            try:
                self._slot_clients_list_builder()
            except Exception:
                pass
        self.refresh_slots_view()
        self._dismiss_client_dialog()

    def _dismiss_client_dialog(self):
        if getattr(self, "dialog_slot_client", None):
            try:
                self.dialog_slot_client.dismiss()
            except Exception:
                pass
            self.dialog_slot_client = None
        self._client_type_dropdown = None
        self._ap_select_dropdown = None

    def _close_slot_editor(self):
        if getattr(self, "dialog_slot", None):
            try:
                self.dialog_slot.dismiss()
            except Exception:
                pass
            self.dialog_slot = None
        self._slot_clients_list_builder = None
        self._editor_slot = None

    def save_slot_edits(self, slot: Slot):
        name = getattr(self, "_slot_name_input", None) and self._slot_name_input.text.strip()
        if name:
            try:
                slot.name = name
            except Exception:
                pass
        self._close_slot_editor()
        self.refresh_slots_view()

    def select_steam_game_in_slot(self, slot: Slot, steam_id: str):
        if steam_id:
            try:
                for ci in getattr(slot, "Clients_to_open", []):
                    if ci.client_type == ClientType.Steam_Game:
                        ci.steam_app_id = steam_id
                        self.refresh_slots_view()
                        return
                self.add_client_to_slot(slot, ClientType.Steam_Game, steam=steam_id)
                self.refresh_slots_view()
                return
            except Exception:
                return

        try:
            selection = self.pick_file_via_dialog()
        except Exception:
            selection = None

        if not selection:
            return

        try:
            exe_path = selection
            self.add_client_to_slot(slot, ClientType.NonSteam_Game, exe=exe_path)
            self.refresh_slots_view()
        except Exception:
            return

    def debug_print_multiworlds(self, *args):
        import pprint
        def slot_to_dict(s):
            return {
                "id": hex(id(s)),
                "name": s.name,
                "Clients_to_open": [
                    {
                        "type": ci.client_type.name,
                        "ap": getattr(ci.ap_client_type, "name", None) if ci.ap_client_type else None,
                        "steam": ci.steam_app_id,
                        "exe": ci.executable_path,
                        "instr": ci.instructions
                    } for ci in s.Clients_to_open
                ]
            }

        def mw_to_dict(mw):
            return {
                "id": hex(id(mw)),
                "name": mw.name,
                "url": mw.url,
                "slots": [slot_to_dict(s) for s in mw.slots]
            }

        pprint.pprint([mw_to_dict(mw) for mw in getattr(self, "multiworlds", [])], width=120)

    def on_stop(self):
        """Serialize multiworlds into primitives before calling Utils.persistent_store to avoid YAML serialization errors."""
        try:
            serialized = self._serialize_multiworlds()
            Utils.persistent_store("multi_manager_data", "multiworlds", serialized, force_store=True)
        except Exception:
            logging.exception("Failed to save multiworlds")
        # call original cleanup
        try:
            super().on_stop()
        except Exception:
            # in case superclass doesn't implement it or other issues
            pass

    def _serialize_multiworlds(self):
        """Convert in-memory Multiworld/Slot/ClientInfo objects to plain dict/list/str so YAML can write them safely."""
        out = []
        for mw in getattr(self, "multiworlds", []) or []:
            mw_d = {
                "name": getattr(mw, "name", "") or "",
                "url": getattr(mw, "url", "") or "",
                "slots": [],
            }
            for s in getattr(mw, "slots", []) or []:
                s_d = {"name": getattr(s, "name", "") or "", "Clients_to_open": []}
                for ci in getattr(s, "Clients_to_open", []) or []:
                    s_d["Clients_to_open"].append({
                        "client_type": getattr(ci.client_type, "name", None) if ci and getattr(ci, "client_type",
                                                                                               None) is not None else None,
                        "ap_client_type": getattr(ci.ap_client_type, "name", None) if getattr(ci, "ap_client_type",
                                                                                              None) else None,
                        "launch_options": getattr(ci, "launch_options", "") or "",
                        "steam_app_id": getattr(ci, "steam_app_id", None),
                        "executable_path": getattr(ci, "executable_path", None),
                        "instructions": getattr(ci, "instructions", None),
                    })
                mw_d["slots"].append(s_d)
            out.append(mw_d)
        return out

    def _deserialize_multiworlds(self, raw_list):
        """Rebuild Multiworld/Slot/ClientInfo objects from the plain structures produced by _serialize_multiworlds."""
        result = []
        for item in raw_list or []:
            try:
                name = item.get("name", "") or ""
                url = item.get("url", "") or ""
                slots = []
                for s in item.get("slots", []) or []:
                    slot_name = s.get("name", "") or ""
                    slot = Slot(name=slot_name)
                    for ci in s.get("Clients_to_open", []) or []:
                        # client_type
                        ct_name = ci.get("client_type")
                        if ct_name and ct_name in ClientType.__members__:
                            ct = ClientType[ct_name]
                        else:
                            ct = ClientType.Default
                        # ap client
                        ap_name = ci.get("ap_client_type") or ci.get("ap")
                        ap = None
                        try:
                            if ap_name and hasattr(APClient, "__members__") and ap_name in APClient.__members__:
                                ap = APClient[ap_name]
                        except Exception:
                            ap = None
                        launch_options = ci.get("launch_options", "") or ""
                        steam_app_id = ci.get("steam_app_id")
                        executable_path = ci.get("executable_path")
                        instructions = ci.get("instructions")
                        slot.Clients_to_open.append(ClientInfo(
                            client_type=ct,
                            ap_client_type=ap,
                            launch_options=launch_options,
                            steam_app_id=steam_app_id,
                            executable_path=executable_path,
                            instructions=instructions
                        ))
                    slots.append(slot)
                result.append(Multiworld(name=name, url=url, slots=slots))
            except Exception:
                logging.exception("Failed to deserialize a multiworld entry; skipping it.")
                continue
        return result


def launch():
    Utils.init_logging("Multiworld_Manager", exception_logger="Client")
    MultiManagerApp().run()


if __name__ == "__main__":
    launch()