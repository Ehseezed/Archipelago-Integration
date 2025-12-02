# python
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, List, Dict

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown

import Utils

if __name__ == "__main__":
    Utils.init_logging("Multiworld_Manager", exception_logger="Client")

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
                id: add_slot_btn
                text: "Add Slot"
                size_hint_x: None
                width: dp(100)
                disabled: True
                on_release: app.open_add_slot_dialog()

            Button:
                id: debug_btn
                text: "Debug"
                size_hint_x: None
                width: dp(80)
                on_release: app.debug_print_multiworlds()

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

    def get_app(self):
        return App.get_running_app()


def _make_apclient_enum():
    from worlds.LauncherComponents import components as _launcher_components, Type as _LauncherType
    members = {}
    comp_map = {}
    for comp in _launcher_components:
        if getattr(comp, "type", None) is _LauncherType.CLIENT:
            # sanitize display_name -> valid identifier
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
    EnumClass = Enum("APClient", members)
    # attach original Component object to enum members (or None)
    for member in EnumClass:
        setattr(member, "component", comp_map.get(member.name))
    return EnumClass

APClient = _make_apclient_enum()


class ClientType(Enum):
    AP = auto()
    Steam_Game = auto()
    NonSteam_Game = auto()
    Manual = auto()
    Default = -1



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
            print("Warning: No AP Client specified for AP client_type this has no actual function.")
        if self.client_type == ClientType.Steam_Game and not self.steam_app_id:
            print("Warning: No Steam Game specified this has no actual function.")
        if self.client_type == ClientType.NonSteam_Game and not self.executable_path:
            print("Warning: No Executable specified this has no actual function.")
        if self.client_type == ClientType.Default:
            print("Warning: ClientInfo created with Default client_type this has no actual function.")




@dataclass
class Slot:
    name: str
    Clients_to_open: List[ClientInfo] = field(default_factory=list)


@dataclass
class Multiworld:
    name: str
    url: Optional[str] = ""
    slots: List[Slot] = field(default_factory=list)


class MultiManagerApp(App):
    # dialog references
    dialog_new: Optional[Popup] = None
    dialog_slot: Optional[Popup] = None
    dialog_edit: Optional[Popup] = None
    dialog_add: Optional[Popup] = None
    _new_slot_type_dropdown = None

    def pick_file_via_dialog(self):
        """
        Open a native file selection using Utils.open_filename.
        Returns selected file path or None.
        """
        import os

        # platform-aware default folders to suggest to the dialog
        if Utils.is_windows:
            default_paths = [
                os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Documents"),
                os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Downloads"),
            ]
            # include typical Windows executable extensions but allow a generic "*" so extensionless matches too
            filetypes = [
                ("Executable", ("*.exe", "*.bat", "*.com", "*")),
                ("All files", ("*",))
            ]
        else:
            # Linux / macOS: prefer user folders and allow selecting extensionless executables
            default_paths = [
                os.path.join(os.path.expanduser("~"), "Documents"),
                os.path.join(os.path.expanduser("~"), "Downloads"),
            ]
            # use "*" (not "*.*") so files without extensions are selectable
            filetypes = [
                ("Executable", ("*",)),
                ("All files", ("*",))
            ]

        default_path = next((p for p in default_paths if os.path.exists(p)), None) or ""
        # delegate to Utils.open_filename which picks the best available native dialog
        try:
            selection = Utils.open_filename("Select file", filetypes, suggest=default_path)
        except Exception:
            # if Utils.open_filename fails for any reason, fall back to no selection
            selection = None

        return selection

    def confirm_delete_slot(self, slot: Slot):
        """Open confirmation popup before deleting a slot."""
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
        """Perform the actual deletion and refresh UI."""
        try:
            if getattr(self, "selected_multiworld", None) and slot in self.selected_multiworld.slots:
                self.selected_multiworld.slots.remove(slot)
        except Exception:
            # keep this silent; UI will simply refresh
            pass

        # If the slot editor is open for this slot, close it
        if getattr(self, "_editor_slot", None) is slot:
            self._close_slot_editor()

        # Close confirmation and refresh UI
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

        # lazy init APClient here to avoid import-time collisions
        global APClient
        try:
            APClient = _make_apclient_enum()
        except Exception:
            APClient = None

        # ensure edit and add-slot buttons disabled initially (safe if ids not ready)
        try:
            self.root.ids.edit_mw_btn.disabled = True
        except Exception:
            pass

        try:
            self.root.ids.add_slot_btn.disabled = True
        except Exception:
            pass
        self.populate_multiworld_list()

    # multiworld create/edit
    def open_new_multiworld_dialog(self):
        if self.dialog_new:
            self.dialog_new.open()
            return

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self._new_name = TextInput(hint_text="Multiworld name", multiline=False,
                                   size_hint_y=None, height=dp(40), font_size=dp(16))
        self._new_url = TextInput(hint_text="Multiworld URL (optional)", multiline=False,
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
        self._edit_url = TextInput(text=(self.selected_multiworld.url or ""), hint_text="Multiworld URL (optional)", multiline=False,
                                   size_hint_y=None, height=dp(40), font_size=dp(16))
        content.add_widget(self._edit_name)
        content.add_widget(self._edit_url)
        btns = BoxLayout(size_hint_y=None, height=dp(40), spacing=8)
        btn_cancel = Button(text="CANCEL", on_release=lambda *a: self.dialog_edit.dismiss())
        btn_save = Button(text="SAVE", on_release=self.save_edited_multiworld)
        btns.add_widget(btn_cancel)
        btns.add_widget(btn_save)
        content.add_widget(btns)

        self.dialog_edit = Popup(title="Edit Multiworld", content=content, size_hint=(None, None), size=(dp(360), dp(220)))
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

    # list population & selection
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
            self.root.ids.toolbar.text = mw.name if mw else "No multiworld selected"
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

    # slots view & editing
    def refresh_slots_view(self):
        slots_box = self.root.ids.slots_box
        slots_box.clear_widgets()
        if not self.selected_multiworld:
            return
        for idx, slot in enumerate(self.selected_multiworld.slots):
            row = SlotRow()
            row.slot = slot
            row.text = f"{idx+1}: {slot.name}: {len(slot.Clients_to_open)} function(s)"
            slots_box.add_widget(row)

    def open_add_slot_details_dialog(self, slot_type: ClientType, name: str, mode: str = "SPEC"):
        # close the base add dialog but keep reference to inputs
        if self.dialog_add:
            self.dialog_add.dismiss()

        # create details dialog
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self._details_slot_type = slot_type
        self._details_slot_name = name

        if mode == "AP":
            # AP selection dropdown (unchanged)
            self._ap_select_btn = Button(text="Select AP client", size_hint_y=None, height=dp(40), font_size=dp(16))
            self._ap_select_dropdown = DropDown()
            ap_options = []
            try:
                if APClient:
                    ap_options = [m.name for m in APClient]
            except Exception:
                ap_options = []
            if not ap_options:
                ap_options = ["NONE"]
            for opt in ap_options:
                b = Button(text=opt, size_hint_y=None, height=dp(40))
                b.bind(on_release=lambda b, val=opt: self._ap_select_dropdown.select(val))
                self._ap_select_dropdown.add_widget(b)
            self._ap_select_btn.bind(on_release=self._ap_select_dropdown.open)
            self._ap_select_dropdown.bind(on_select=lambda inst, val: setattr(self._ap_select_btn, "text", val))
            content.add_widget(self._ap_select_btn)
        else:
            hint = "Primary spec (steam id / exe path / instructions)"
            row = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=None, height=dp(40))
            self._details_spec_input = TextInput(hint_text=hint, multiline=False,
                                                 size_hint_y=None, height=dp(40), font_size=dp(16))
            row.add_widget(self._details_spec_input)

            if slot_type == ClientType.Steam_Game:

                btn_browse = Button(text="Browse", size_hint_x=None, width=dp(100), size_hint_y=None, height=dp(40))
                btn_browse.bind(on_release= lambda *a: self._details_spec_input.setter('text')(self.pick_file_via_dialog() or ""))
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

    def open_add_slot_dialog(self):
        """
        Open the initial Add Slot dialog (name + client type).
        """
        if getattr(self, "dialog_add", None):
            try:
                self.dialog_add.open()
            except Exception:
                pass
            return

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self._new_slot_name = TextInput(hint_text="Slot name", multiline=False,
                                        size_hint_y=None, height=dp(40), font_size=dp(16))
        content.add_widget(self._new_slot_name)

        # client type selector (Button + DropDown)
        self._new_slot_type = Button(text="Default", size_hint_y=None, height=dp(40))
        self._new_slot_type_dropdown = DropDown()
        try:
            for name in ClientType.__members__:
                b = Button(text=name, size_hint_y=None, height=dp(40))
                b.bind(on_release=lambda btn, val=name: self._new_slot_type_dropdown.select(val))
                self._new_slot_type_dropdown.add_widget(b)
        except Exception:
            pass
        self._new_slot_type.bind(on_release=self._new_slot_type_dropdown.open)
        self._new_slot_type_dropdown.bind(on_select=lambda inst, val: setattr(self._new_slot_type, "text", val))
        content.add_widget(self._new_slot_type)

        btns = BoxLayout(size_hint_y=None, height=dp(40), spacing=8)
        btn_cancel = Button(text="CANCEL", on_release=lambda *a: self._dismiss_add_dialog())
        btn_create = Button(text="CREATE", on_release=self._on_add_slot_create)
        btns.add_widget(btn_cancel)
        btns.add_widget(btn_create)
        content.add_widget(btns)

        self.dialog_add = Popup(title="Add Slot", content=content, size_hint=(None, None), size=(dp(420), dp(220)))
        self.dialog_add.open()

    def _on_add_slot_create(self, *args):
        """
        Called when user clicks CREATE on the first Add Slot dialog.
        - Default: create immediately
        - AP: open AP details dialog
        - Manual: open SPEC details dialog
        - Steam_Game / NonSteam_Game: launch file picker (background thread) and finalize with chosen path
        """
        from kivy.clock import Clock
        import threading

        name = getattr(self, "_new_slot_name", None) and self._new_slot_name.text.strip()
        if not name:
            # nothing to do, close the add dialog if still open
            self._dismiss_add_dialog()
            return

        type_text = getattr(self, "_new_slot_type", None) and self._new_slot_type.text.strip()
        slot_type = ClientType.Default
        if type_text and type_text in ClientType.__members__:
            slot_type = ClientType[type_text]

        # Close the base add dialog so we don't stack dialogs / keep UI consistent
        self._dismiss_add_dialog()

        if slot_type == ClientType.AP:
            # AP needs the AP-specific details dialog
            self.open_add_slot_details_dialog(slot_type, name, mode="AP")
            return

        if slot_type == ClientType.Manual:
            # Manual uses the SPEC details dialog (user types instructions)
            self.open_add_slot_details_dialog(slot_type, name, mode="SPEC")
            return

        if slot_type in (ClientType.Steam_Game, ClientType.NonSteam_Game):
            # Launch the shared file picker in a background thread to avoid blocking UI / importing tkinter on Kivy main loop.
            def worker():
                try:
                    spec_path = self.pick_file_via_dialog()
                except Exception:
                    spec_path = None

                def finalize_if_selected(dt):
                    if spec_path:
                        # pass the chosen path as the spec
                        self._finalize_create_slot(slot_type, name, spec=spec_path)
                    # If user cancelled the picker (spec_path is None), do nothing (add dialog already dismissed).

                Clock.schedule_once(finalize_if_selected, 0)

            threading.Thread(target=worker, daemon=True).start()
            return

        # Default / no extra info required: create slot immediately
        self._finalize_create_slot(slot_type, name, spec=None)

    def _on_details_create(self, *args):
        # read details from the details dialog and finalize slot creation
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

        # finalize create
        self._finalize_create_slot(slot_type, name, spec=spec, ap_choice_name=ap_choice_name)
        self._dismiss_add_dialog()

    def _finalize_create_slot(self, slot_type: ClientType, name: str, spec: Optional[str] = None,
                              ap_choice_name: Optional[str] = None):
        # safe creation following existing non-invasive pattern
        try:
            new_slot = Slot(name=name)
            if not hasattr(new_slot, "Clients_to_open") or new_slot.Clients_to_open is None:
                new_slot.Clients_to_open = []
        except Exception:
            return

        # append slot to multiworld
        try:
            if getattr(self, "selected_multiworld", None) is None:
                return
            self.selected_multiworld.slots.append(new_slot)
        except Exception:
            return

        # build ClientInfo and add one entry
        try:
            if slot_type == ClientType.AP:
                ap_enum_member = None
                try:
                    if APClient and ap_choice_name:
                        # prefer exact name match
                        ap_enum_member = APClient[ap_choice_name] if ap_choice_name in APClient.__members__ else None
                except Exception:
                    ap_enum_member = None
                ci = self._make_clientinfo_for_type(ClientType.AP, None)
                # replace ap_client_type if we could resolve selection
                if ap_enum_member:
                    ci.ap_client_type = ap_enum_member
            else:
                ci = self._make_clientinfo_for_type(slot_type, spec)
            if ci and ci.client_type != ClientType.Default:
                # use the existing helper so UI/state updates remain consistent
                self.add_client_to_slot(new_slot, ci.client_type, ap=ci.ap_client_type,
                                        launch=ci.launch_options, steam=ci.steam_app_id,
                                        exe=ci.executable_path, instr=ci.instructions)
                # If Steam_Game and we have a spec (from the file chooser), use the helper to apply it
                try:
                    if slot_type == ClientType.Steam_Game and spec:
                        # call the new method to handle steam selection for this slot
                        self.select_steam_game_in_slot(new_slot, spec)
                except Exception:
                    pass
            else:
                # still create an empty/default ClientInfo entry to reflect user's intent
                try:
                    new_slot.Clients_to_open.append(ClientInfo(client_type=ClientType.Default))
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
        # build a ClientInfo that satisfies __post_init__ checks
        if ct == ClientType.AP:
            ap_choice = None
            try:
                if APClient:
                    # try to match by name or use first member as fallback
                    for m in APClient:
                        if spec and (spec == m.name or spec == m.value):
                            ap_choice = m
                            break
                    if not ap_choice:
                        ap_choice = next(iter(APClient))
            except Exception:
                ap_choice = None
            return ClientInfo(client_type=ClientType.AP, ap_client_type=ap_choice)
        if ct == ClientType.Steam_Game:
            return ClientInfo(client_type=ClientType.Steam_Game, steam_app_id=(spec or ""))
        if ct == ClientType.NonSteam_Game:
            return ClientInfo(client_type=ClientType.NonSteam_Game, executable_path=(spec or ""))
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
        # map text to ClientType safely
        slot_type = ClientType.Default
        if type_text and type_text in ClientType.__members__:
            slot_type = ClientType[type_text]

        # create Slot and ensure Clients_to_open list exists
        try:
            new_slot = Slot(name=name)
            if not hasattr(new_slot, "Clients_to_open") or new_slot.Clients_to_open is None:
                new_slot.Clients_to_open = []
        except Exception:
            self._dismiss_add_dialog()
            return

        # attach slot to selected multiworld
        try:
            self.selected_multiworld.slots.append(new_slot)
        except Exception:
            self._dismiss_add_dialog()
            return

        # create an initial ClientInfo using the helper and add via the helper
        try:
            ci = self._make_clientinfo_for_type(slot_type, None)
            if ci and ci.client_type != ClientType.Default:
                self.add_client_to_slot(new_slot, ci.client_type, ap=ci.ap_client_type,
                                        launch=ci.launch_options, steam=ci.steam_app_id,
                                        exe=ci.executable_path, instr=ci.instructions)
        except Exception:
            # non-fatal — slot created even if initial client creation fails
            pass

        self._dismiss_add_dialog()
        self.refresh_slots_view()

    def add_client_to_slot(self, slot: Slot, type: ClientType, ap: Optional[APClient] = None, launch: str = "", steam: str = "", exe: str = "", instr: str = ""):
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
        # open a dialog that allows editing the slot name and managing clients
        if self.dialog_slot:
            self.dialog_slot.open()
            return

        self._editor_slot = slot

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # slot name
        self._slot_name_input = TextInput(text=getattr(slot, "name", ""), multiline=False,
                                          size_hint_y=None, height=dp(40), font_size=dp(16))
        content.add_widget(self._slot_name_input)

        # client list area
        self._slot_clients_list = BoxLayout(orientation='vertical', spacing=6, size_hint_y=None)
        self._slot_clients_list.bind(minimum_height=self._slot_clients_list.setter('height'))

        def _build_clients_list():
            self._slot_clients_list.clear_widgets()
            clients = getattr(slot, "Clients_to_open", []) or []
            for i, ci in enumerate(clients):
                row = BoxLayout(size_hint_y=None, height=dp(40), spacing=6)
                # display: type and short spec
                ct = getattr(ci, "client_type", None)
                ct_text = ct.name if ct else "Unknown"
                extra = ""
                if getattr(ci, "steam_app_id", None):
                    extra = ci.steam_app_id
                elif getattr(ci, "executable_path", None):
                    extra = ci.executable_path
                elif getattr(ci, "instructions", None):
                    extra = ci.instructions
                elif getattr(ci, "ap_client_type", None):
                    extra = getattr(ci.ap_client_type, "name", "")
                lbl = Label(text=f"{ct_text}{(': ' + extra) if extra else ''}", halign="left", valign="middle",
                            text_size=(None, dp(40)))
                row.add_widget(lbl)
                btn_edit = Button(text="Edit", size_hint_x=None, width=dp(64))
                btn_remove = Button(text="Remove", size_hint_x=None, width=dp(80))
                # capture index
                btn_edit.bind(on_release=lambda inst, idx=i: self._open_client_edit_dialog(slot, idx))

                def _remove(inst, idx=i):
                    try:
                        slot.Clients_to_open.pop(idx)
                    except Exception:
                        pass
                    _build_clients_list()
                    self.refresh_slots_view()

                btn_remove.bind(on_release=_remove)
                row.add_widget(btn_edit)
                row.add_widget(btn_remove)
                self._slot_clients_list.add_widget(row)

        # populate initial list
        _build_clients_list()

        # wrap in ScrollView-like area
        content.add_widget(self._slot_clients_list)

        # add / save / cancel buttons
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

        # store builder to refresh after client edits
        self._slot_clients_list_builder = _build_clients_list

    def _open_client_edit_dialog(self, slot: Slot, client_index: Optional[int]):
        """
        Edit an existing client (client_index >= 0) or create a new one (client_index is None).
        - Existing client: client type is fixed. UI only allows changing AP client (if AP) or the spec/exe path (for games/manual).
        - New client: allow selecting a client type and providing the appropriate spec/AP selection.
        """
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

        def _create_spec_row(initial_text: str = ""):
            """Return (row_widget, text_input) where row contains a TextInput and a Browse button
            that calls self.pick_file_via_dialog() in a background thread and updates the TextInput."""
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=8)
            ti = TextInput(text=initial_text, multiline=False)
            row.add_widget(ti)
            btn_browse = Button(text="Browse...", size_hint_x=None, width=dp(100))

            def _on_browse(_inst):
                def worker():
                    try:
                        # call the existing pick implementation (may use Utils.open_filename)
                        path = None
                        try:
                            path = self.pick_file_via_dialog()
                        except Exception:
                            # fallback to Utils.open_filename if pick_file_via_dialog is not implemented
                            try:
                                path = Utils.open_filename("Select file", (("All files", ("*.*",)),))
                            except Exception:
                                path = None
                    except Exception:
                        path = None

                    # schedule UI update
                    def _set_path(dt):
                        if path:
                            ti.text = path

                    Clock.schedule_once(_set_path, 0)

                threading.Thread(target=worker, daemon=True).start()

            btn_browse.bind(on_release=_on_browse)
            row.add_widget(btn_browse)
            return row, ti

        # build dialog content
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # If editing an existing client, do not allow changing client type.
        if existing_ci:
            # show fixed client type label
            lbl = Label(text=f"Client Type: {existing_ci.client_type.name}", size_hint_y=None, height=dp(30))
            content.add_widget(lbl)

            # AP selection
            if existing_ci.client_type == ClientType.AP:
                # build AP dropdown from APClient enum
                self._client_ap_select_btn = Button(
                    text=(existing_ci.ap_client_type.name if getattr(existing_ci, "ap_client_type",
                                                                     None) else "Select AP Client"),
                    size_hint_y=None, height=dp(40))
                self._client_ap_select_dropdown = DropDown()
                for member in APClient:
                    b = Button(text=member.name, size_hint_y=None, height=dp(40))
                    b.bind(on_release=lambda btn, m=member: self._client_ap_select_dropdown.select(m))
                    self._client_ap_select_dropdown.add_widget(b)
                # When an AP is selected, set the button text and store selection
                self._client_ap_select_dropdown.bind(
                    on_select=lambda inst, val: setattr(self._client_ap_select_btn, "text", val.name))
                self._client_ap_select_btn.bind(on_release=self._client_ap_select_dropdown.open)
                # store current selection on the instance for later save
                self._client_ap_select_btn._selected_ap = getattr(existing_ci, "ap_client_type", None)
                # set text properly if an AP is present
                if getattr(existing_ci, "ap_client_type", None):
                    self._client_ap_select_btn.text = existing_ci.ap_client_type.name
                content.add_widget(self._client_ap_select_btn)
                # map selected ap value retrieval in save to reading button text / stored selection
            else:
                # For Steam_Game / NonSteam_Game / Manual show spec row with Browse
                initial = getattr(existing_ci, "executable_path", "") or getattr(existing_ci, "steam_app_id",
                                                                                 "") or getattr(existing_ci,
                                                                                                "instructions",
                                                                                                "") or ""
                spec_row, spec_input = _create_spec_row(initial)
                content.add_widget(spec_row)
                self._client_spec_input = spec_input

        else:
            # Creating a new client: allow selecting a type (keeps previous UX)
            # type selector
            self._client_type_btn = Button(text="Client Type", size_hint_y=None, height=dp(40))
            self._client_type_dropdown = DropDown()
            for opt in ("AP", "Steam_Game", "NonSteam_Game", "Manual", "Default"):
                b = Button(text=opt, size_hint_y=None, height=dp(40))
                b.bind(on_release=lambda btn, val=opt: self._client_type_dropdown.select(val))
                self._client_type_dropdown.add_widget(b)
            self._client_type_btn.bind(on_release=self._client_type_dropdown.open)
            self._client_type_dropdown.bind(
                on_select=lambda instance, value: setattr(self._client_type_btn, "text", value))
            content.add_widget(self._client_type_btn)

            # placeholder area for either AP selector or spec row; start with a plain spec row
            spec_row, spec_input = _create_spec_row("")
            content.add_widget(spec_row)
            self._client_spec_input = spec_input

            # when type changes, swap the widget
            def _on_type_selected(instance, value):
                # remove current widget if present
                try:
                    if getattr(self, "_client_ap_select_btn", None) and self._client_ap_select_btn.parent:
                        content.remove_widget(self._client_ap_select_btn)
                except Exception:
                    pass
                try:
                    if getattr(self, "_client_spec_input", None) and self._client_spec_input.parent:
                        content.remove_widget(self._client_spec_input.parent if hasattr(self._client_spec_input,
                                                                                        "parent") else self._client_spec_input)
                except Exception:
                    pass

                if value == "AP":
                    # add AP selector
                    self._client_ap_select_btn = Button(text="Select AP Client", size_hint_y=None, height=dp(40))
                    self._client_ap_select_dropdown = DropDown()
                    for member in APClient:
                        b = Button(text=member.name, size_hint_y=None, height=dp(40))
                        b.bind(on_release=lambda btn, m=member: self._client_ap_select_dropdown.select(m))
                        self._client_ap_select_dropdown.add_widget(b)
                    self._client_ap_select_dropdown.bind(
                        on_select=lambda inst, val: setattr(self._client_ap_select_btn, "text", val.name))
                    self._client_ap_select_btn.bind(on_release=self._client_ap_select_dropdown.open)
                    content.add_widget(self._client_ap_select_btn, index=len(content.children))
                    self._client_spec_input = None
                else:
                    # add spec row for games/manual/default
                    spec_row, spec_input = _create_spec_row("")
                    content.add_widget(spec_row, index=len(content.children))
                    self._client_spec_input = spec_input
                    self._client_ap_select_btn = None
                    self._client_ap_select_dropdown = None

            self._client_type_dropdown.bind(on_select=_on_type_selected)

        # buttons
        btns = BoxLayout(size_hint_y=None, height=dp(40), spacing=8)
        btn_cancel = Button(text="CANCEL")
        btn_save = Button(text="SAVE")
        btn_cancel.bind(on_release=lambda *a: self._dismiss_client_dialog())
        btn_save.bind(on_release=lambda *a: self._on_client_dialog_save(slot, client_index))
        btns.add_widget(btn_cancel)
        btns.add_widget(btn_save)
        content.add_widget(btns)

        self.dialog_slot_client = Popup(title="Edit Client", content=content, size_hint=(None, None),
                                        size=(dp(420), dp(220)))
        self.dialog_slot_client.open()

        # ensure helper references exist for save handler
        if not getattr(self, "_client_ap_select_btn", None):
            self._client_ap_select_btn = None
        if not getattr(self, "_client_spec_input", None):
            self._client_spec_input = getattr(self, "_client_spec_input", None)

    def _on_client_dialog_save(self, slot: Slot, client_index: Optional[int]):
        # read type & spec/ap choice and create/update ClientInfo
        type_text = getattr(self, "_client_type_btn", None) and self._client_type_btn.text
        chosen_type = ClientType.Default
        if type_text and type_text in ClientType.__members__:
            chosen_type = ClientType[type_text]

        spec = None
        ap_choice = None
        if chosen_type == ClientType.AP:
            ap_choice_name = getattr(self, "_ap_select_btn", None) and self._ap_select_btn.text
            if ap_choice_name and APClient and ap_choice_name in APClient.__members__:
                ap_choice = APClient[ap_choice_name]
        else:
            spec = getattr(self, "_client_spec_input", None) and self._client_spec_input.text.strip()

        # build ClientInfo
        try:
            ci = self._make_clientinfo_for_type(chosen_type, spec)
            if chosen_type == ClientType.AP and ap_choice:
                ci.ap_client_type = ap_choice
        except Exception:
            ci = None

        if ci:
            # apply edit or append
            try:
                if client_index is None:
                    # add
                    self.add_client_to_slot(slot, ci.client_type, ap=ci.ap_client_type, launch=ci.launch_options,
                                            steam=ci.steam_app_id, exe=ci.executable_path, instr=ci.instructions)
                else:
                    # replace existing
                    clients = getattr(slot, "Clients_to_open", []) or []
                    if 0 <= client_index < len(clients):
                        clients[client_index] = ci
            except Exception:
                pass

        # refresh client list in slot editor and main view
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
        # clear temp fields
        self._client_type_dropdown = None
        self._ap_select_dropdown = None

    def _close_slot_editor(self):
        if getattr(self, "dialog_slot", None):
            try:
                self.dialog_slot.dismiss()
            except Exception:
                pass
            self.dialog_slot = None
        # clear builder reference
        self._slot_clients_list_builder = None
        self._editor_slot = None

    def save_slot_edits(self, slot: Slot):
        # update slot name and close editor
        name = getattr(self, "_slot_name_input", None) and self._slot_name_input.text.strip()
        if name:
            try:
                slot.name = name
            except Exception:
                pass
        # dismiss editor
        self._close_slot_editor()
        self.refresh_slots_view()

    def select_steam_game_in_slot(self, slot: Slot, steam_id: str):
        # If steam_id provided, apply it to an existing Steam_Game client or add one
        if steam_id:
            try:
                # try to find existing Steam_Game client and set steam_app_id
                for ci in getattr(slot, "Clients_to_open", []):
                    if ci.client_type == ClientType.Steam_Game:
                        ci.steam_app_id = steam_id
                        self.refresh_slots_view()
                        return
                # otherwise add a new Steam_Game client entry
                self.add_client_to_slot(slot, ClientType.Steam_Game, steam=steam_id)
                self.refresh_slots_view()
                return
            except Exception:
                # keep silent as UI already tolerates failures
                return

        # No steam_id passed -> open native file chooser via pick_file_via_dialog()
        try:
            selection = self.pick_file_via_dialog()
        except Exception:
            selection = None

        if not selection:
            # user cancelled or dialog unavailable
            return

        # Treat chosen file as an executable path and add as a NonSteam_Game client
        try:
            # normalize path if needed (keep raw selection otherwise)
            exe_path = selection
            self.add_client_to_slot(slot, ClientType.NonSteam_Game, exe=exe_path)
            self.refresh_slots_view()
        except Exception:
            # ignore errors to avoid crashing the UI
            return

    def debug_print_multiworlds(self, *args):
        import pprint
        def slot_to_dict(s):
            return {
                "id": hex(id(s)),
                "name": s.name,
                "Clients_to_open": [
                    {
                        "client_type": c.client_type.name if c.client_type else "Unknown",
                        "ap_client_type": c.ap_client_type.name if c.ap_client_type else None,
                        "launch_options": c.launch_options,
                        "steam_app_id": c.steam_app_id,
                        "executable_path": c.executable_path,
                        "instructions": c.instructions
                    } for c in (s.Clients_to_open or [])
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


if __name__ == "__main__":
    MultiManagerApp().run()