#!/usr/bin/env python3
import json
import os
import sys

from PyQt6.QtCore import Qt, QSortFilterProxyModel, QSize
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QFont, QColor, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableView,
    QVBoxLayout,
    QWidget,
    QFrame,
    QSizePolicy,
)

if getattr(sys, "frozen", False):
    _BASE_DIR = os.path.dirname(sys.executable)
else:
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(_BASE_DIR, "address_book.json")

TRANSLATIONS = {
    "en": {
        "window_title": "Address Book",
        "search_group": "Search",
        "search_placeholder": "Search by name, email, company code or description…",
        "contacts_group": "Contacts",
        "form_group": "New / Edit contact",
        "col_name": "Name",
        "col_email": "Email",
        "col_company": "Company Code",
        "col_desc": "Description",
        "label_name": "Name:",
        "label_email": "Email:",
        "label_company": "Company Code:",
        "label_desc": "Description:",
        "btn_save": "💾  Add / Save",
        "btn_delete": "🗑  Delete",
        "btn_clear": "✖  Clear",
        "warn_title_missing": "Missing data",
        "warn_body_missing": "Please fill in Name and Email.",
        "warn_title_no_sel": "No selection",
        "warn_body_no_sel": "Please select a contact to delete.",
        "confirm_delete_title": "Delete",
        "confirm_delete_body": "Delete contact '{name}'?",
        "lang_label": "Language:",
    },
    "de": {
        "window_title": "Adressbuch",
        "search_group": "Suchen",
        "search_placeholder": "Suche nach Name, E-Mail, Firmencode oder Beschreibung…",
        "contacts_group": "Kontakte",
        "form_group": "Neuer / Kontakt bearbeiten",
        "col_name": "Name",
        "col_email": "E-Mail",
        "col_company": "Firmencode",
        "col_desc": "Beschreibung",
        "label_name": "Name:",
        "label_email": "E-Mail:",
        "label_company": "Firmencode:",
        "label_desc": "Beschreibung:",
        "btn_save": "💾  Speichern",
        "btn_delete": "🗑  Löschen",
        "btn_clear": "✖  Leeren",
        "warn_title_missing": "Fehlende Daten",
        "warn_body_missing": "Bitte Name und E-Mail ausfüllen.",
        "warn_title_no_sel": "Keine Auswahl",
        "warn_body_no_sel": "Bitte einen Kontakt zum Löschen auswählen.",
        "confirm_delete_title": "Löschen",
        "confirm_delete_body": "Kontakt '{name}' löschen?",
        "lang_label": "Sprache:",
    },
}

STYLESHEET = """
QWidget {
    background-color: #1a1f2e;
    color: #d4dbe8;
    font-size: 15px;
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
}

/* ── Top bar ── */
#topbar {
    background-color: #141820;
    border-bottom: 2px solid #2a3045;
    padding: 6px 12px;
}
#appTitle {
    font-size: 22px;
    font-weight: bold;
    color: #5cb8f0;
    letter-spacing: 1px;
}
#langLabel {
    color: #8896ae;
    font-size: 13px;
}

/* ── GroupBox ── */
QGroupBox {
    border: 2px solid #2a3045;
    border-radius: 10px;
    margin-top: 14px;
    padding: 12px 10px 10px 10px;
    font-size: 13px;
    color: #8896ae;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: #5cb8f0;
    font-weight: bold;
    font-size: 13px;
}

/* ── LineEdit ── */
QLineEdit {
    background-color: #222840;
    border: 2px solid #2a3045;
    border-radius: 8px;
    padding: 8px 12px;
    color: #d4dbe8;
    font-size: 15px;
    selection-background-color: #5cb8f0;
    selection-color: #141820;
}
QLineEdit:focus {
    border: 2px solid #5cb8f0;
    background-color: #263050;
}
QLineEdit::placeholder {
    color: #4a566e;
}

/* ── Labels in form ── */
QFormLayout QLabel {
    color: #a8b4c8;
    font-size: 14px;
    font-weight: bold;
    min-width: 130px;
}

/* ── Table ── */
QTableView {
    background-color: #141820;
    alternate-background-color: #1a1f2e;
    border: 2px solid #2a3045;
    border-radius: 10px;
    gridline-color: #2a3045;
    selection-background-color: #2e6da4;
    selection-color: #ffffff;
    font-size: 14px;
}
QTableView::item {
    padding: 6px 10px;
}
QTableView::item:selected {
    background-color: #2e6da4;
    color: #ffffff;
    font-weight: bold;
}
QHeaderView::section {
    background-color: #222840;
    color: #5cb8f0;
    font-weight: bold;
    font-size: 13px;
    padding: 8px 10px;
    border: none;
    border-right: 1px solid #2a3045;
    border-bottom: 2px solid #5cb8f0;
}
QHeaderView::section:hover {
    background-color: #2a3045;
}

/* ── Buttons ── */
QPushButton {
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: bold;
    border: none;
    min-width: 130px;
}
#btnSave {
    background-color: #3a9e6e;
    color: #ffffff;
}
#btnSave:hover  { background-color: #44b87e; }
#btnSave:pressed { background-color: #2e7d57; }

#btnDelete {
    background-color: #c0550a;
    color: #ffffff;
}
#btnDelete:hover  { background-color: #d9620c; }
#btnDelete:pressed { background-color: #9a4208; }

#btnClear {
    background-color: #2a3045;
    color: #a8b4c8;
}
#btnClear:hover  { background-color: #344060; }
#btnClear:pressed { background-color: #1e2535; }

/* ── ComboBox ── */
QComboBox {
    background-color: #222840;
    border: 2px solid #2a3045;
    border-radius: 8px;
    padding: 6px 12px;
    color: #d4dbe8;
    font-size: 14px;
    min-width: 110px;
}
QComboBox:hover { border-color: #5cb8f0; }
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox::down-arrow {
    width: 10px;
    height: 10px;
}
QComboBox QAbstractItemView {
    background-color: #222840;
    border: 2px solid #5cb8f0;
    border-radius: 8px;
    selection-background-color: #2e6da4;
    selection-color: #ffffff;
    padding: 4px;
}

/* ── Scrollbar ── */
QScrollBar:vertical {
    background: #1a1f2e;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: #2a3045;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover { background: #5cb8f0; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

/* ── Splitter ── */
QSplitter::handle {
    background-color: #2a3045;
    height: 6px;
    border-radius: 3px;
    margin: 2px 8px;
}
QSplitter::handle:hover {
    background-color: #5cb8f0;
}
"""


def load_contacts() -> dict:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        migrated = {}
        for name, value in data.items():
            if isinstance(value, str):
                migrated[name] = {"email": value, "company_code": "", "opis": ""}
            else:
                entry = dict(value)
                entry.setdefault("company_code", "")
                entry.setdefault("opis", "")
                migrated[name] = entry
        return migrated
    return {}


def save_contacts(contacts: dict) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)


class AddressBook(QWidget):
    def __init__(self):
        super().__init__()
        self.contacts = load_contacts()
        self._lang = "en"
        self._build_ui()
        self._populate_model()

    def _t(self, key: str, **kwargs) -> str:
        text = TRANSLATIONS[self._lang][key]
        return text.format(**kwargs) if kwargs else text

    def _build_ui(self):
        self.setMinimumSize(760, 600)
        self.resize(860, 660)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Top bar ──
        topbar = QFrame()
        topbar.setObjectName("topbar")
        topbar.setFixedHeight(56)
        tb_layout = QHBoxLayout(topbar)
        tb_layout.setContentsMargins(16, 0, 16, 0)

        self.app_title = QLabel()
        self.app_title.setObjectName("appTitle")
        tb_layout.addWidget(self.app_title)
        tb_layout.addStretch()

        self.lang_label = QLabel()
        self.lang_label.setObjectName("langLabel")
        tb_layout.addWidget(self.lang_label)

        self.lang_combo = QComboBox()
        self.lang_combo.addItem("🇬🇧  English", "en")
        self.lang_combo.addItem("🇩🇪  Deutsch", "de")
        self.lang_combo.currentIndexChanged.connect(self._on_lang_changed)
        tb_layout.addWidget(self.lang_combo)
        root.addWidget(topbar)

        # ── Content ──
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(16, 12, 16, 12)
        content_layout.setSpacing(12)

        # Search
        self.search_group = QGroupBox()
        sg_layout = QHBoxLayout(self.search_group)
        self.search_edit = QLineEdit()
        self.search_edit.textChanged.connect(self._on_search)
        sg_layout.addWidget(self.search_edit)
        content_layout.addWidget(self.search_group)

        # Table
        self.model = QStandardItemModel(0, 4)
        self.proxy = QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.proxy.setFilterKeyColumn(-1)

        self.table = QTableView()
        self.table.setModel(self.proxy)
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)
        header.setMinimumSectionSize(80)
        self.table.setColumnWidth(0, 170)
        self.table.setColumnWidth(1, 210)
        self.table.setColumnWidth(2, 120)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(38)
        self.table.selectionModel().selectionChanged.connect(self._on_row_selected)

        # Form
        self.form_group = QGroupBox()
        form_layout = QHBoxLayout(self.form_group)
        form_layout.setSpacing(12)

        self.name_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.company_edit = QLineEdit()
        self.opis_edit = QLineEdit()
        self.label_name = QLabel()
        self.label_email = QLabel()
        self.label_company = QLabel()
        self.label_desc = QLabel()

        for label, field in [
            (self.label_name, self.name_edit),
            (self.label_email, self.email_edit),
            (self.label_company, self.company_edit),
            (self.label_desc, self.opis_edit),
        ]:
            col = QVBoxLayout()
            col.setSpacing(4)
            col.addWidget(label)
            col.addWidget(field)
            form_layout.addLayout(col)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        self.btn_save = QPushButton()
        self.btn_delete = QPushButton()
        self.btn_clear = QPushButton()
        self.btn_save.setObjectName("btnSave")
        self.btn_delete.setObjectName("btnDelete")
        self.btn_clear.setObjectName("btnClear")
        self.btn_save.setMinimumHeight(42)
        self.btn_delete.setMinimumHeight(42)
        self.btn_clear.setMinimumHeight(42)
        self.btn_save.clicked.connect(self._add_or_update)
        self.btn_delete.clicked.connect(self._delete)
        self.btn_clear.clicked.connect(self._clear_form)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addStretch()

        # Bottom panel (form + buttons)
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(10)
        bottom_layout.addWidget(self.form_group)
        bottom_layout.addLayout(btn_layout)

        # Splitter
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.table)
        splitter.addWidget(bottom_widget)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        splitter.setHandleWidth(8)
        content_layout.addWidget(splitter)

        root.addWidget(content)
        self._apply_translations()

    def _apply_translations(self):
        self.setWindowTitle(self._t("window_title"))
        self.app_title.setText("📒  " + self._t("window_title"))
        self.lang_label.setText(self._t("lang_label") + "  ")
        self.search_group.setTitle(self._t("search_group"))
        self.search_edit.setPlaceholderText(self._t("search_placeholder"))
        self.form_group.setTitle(self._t("form_group"))
        self.label_name.setText(self._t("label_name"))
        self.label_email.setText(self._t("label_email"))
        self.label_company.setText(self._t("label_company"))
        self.label_desc.setText(self._t("label_desc"))
        self.btn_save.setText(self._t("btn_save"))
        self.btn_delete.setText(self._t("btn_delete"))
        self.btn_clear.setText(self._t("btn_clear"))
        self.model.setHorizontalHeaderLabels([
            self._t("col_name"),
            self._t("col_email"),
            self._t("col_company"),
            self._t("col_desc"),
        ])

    def _populate_model(self):
        self.model.removeRows(0, self.model.rowCount())
        for name, d in self.contacts.items():
            row = [
                QStandardItem(name),
                QStandardItem(d["email"]),
                QStandardItem(d.get("company_code", "")),
                QStandardItem(d.get("opis", "")),
            ]
            for item in row:
                item.setEditable(False)
            self.model.appendRow(row)

    def _on_lang_changed(self):
        self._lang = self.lang_combo.currentData()
        self._apply_translations()

    def _on_search(self, text: str):
        self.proxy.setFilterFixedString(text)

    def _on_row_selected(self):
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return
        row = indexes[0].row()
        self.name_edit.setText(self.proxy.index(row, 0).data())
        self.email_edit.setText(self.proxy.index(row, 1).data())
        self.company_edit.setText(self.proxy.index(row, 2).data())
        self.opis_edit.setText(self.proxy.index(row, 3).data())

    def _add_or_update(self):
        name = self.name_edit.text().strip()
        email = self.email_edit.text().strip()
        company = self.company_edit.text().strip()
        opis = self.opis_edit.text().strip()
        if not name or not email:
            QMessageBox.warning(self, self._t("warn_title_missing"), self._t("warn_body_missing"))
            return
        self.contacts[name] = {"email": email, "company_code": company, "opis": opis}
        save_contacts(self.contacts)
        self._populate_model()
        self._clear_form()

    def _delete(self):
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            QMessageBox.warning(self, self._t("warn_title_no_sel"), self._t("warn_body_no_sel"))
            return
        name = self.proxy.index(indexes[0].row(), 0).data()
        reply = QMessageBox.question(
            self,
            self._t("confirm_delete_title"),
            self._t("confirm_delete_body", name=name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            del self.contacts[name]
            save_contacts(self.contacts)
            self._populate_model()
            self._clear_form()

    def _clear_form(self):
        self.name_edit.clear()
        self.email_edit.clear()
        self.company_edit.clear()
        self.opis_edit.clear()
        self.table.clearSelection()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    window = AddressBook()
    window.show()
    sys.exit(app.exec())
