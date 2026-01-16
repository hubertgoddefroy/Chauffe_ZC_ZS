import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton,
    QFileDialog, QCheckBox, QLineEdit, QComboBox, QLabel)
from mesure_et_log import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calibration réflecto ZC")
        self.setGeometry(100, 100, 400, 300)

        # Appliquer un style moderne à toute la fenêtre
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
                margin-top: 10px;
                background-color: white;
            }
            QLabel {
                font-size: 12px;
                color: #333;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 12px;
                min-height: 24px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QLineEdit, QComboBox {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 6px;
                font-size: 12px;
            }
            QCheckBox {
                spacing: 8px;
                font-size: 12px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
        """)

        # Variables pour stocker les chemins
        self.install_dir = ""
        self.save_dir = ""

        # Variables pour stocker l'état des cases à cocher
        self.checkbox1_state = False
        self.checkbox2_state = False
        self.checkbox3_state = False
        self.checkbox4_state = False

        # Variable pour stocker les textes des champs
        self.text_field_machine = ""
        self.text_field_iteration = ""
        self.text_field_frequence = ""
        self.text_field_frequence_snap = ""

        # Variable pour stocker l'option sélectionnée
        self.combo_box_selection = ""

        # Widget central et layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Bouton pour sélectionner le dossier d'installation
        self.btn_install = QPushButton("Installation ZymoSoft")
        self.btn_install.clicked.connect(self.select_install_dir)
        layout.addWidget(self.btn_install)

        # Label pour afficher le dossier d'installation sélectionné
        self.label_install = QLabel("Aucun dossier sélectionné")
        layout.addWidget(self.label_install)

        # Bouton pour sélectionner le dossier d'enregistrement
        self.btn_save = QPushButton("Dossier d'enregistrement")
        self.btn_save.clicked.connect(self.select_save_dir)
        layout.addWidget(self.btn_save)

        # Label pour afficher le dossier d'enregistrement sélectionné
        self.label_save = QLabel("Aucun dossier sélectionné")
        layout.addWidget(self.label_save)

        # Champ texte
        self.text_field_machine = QLineEdit()
        self.text_field_machine.setPlaceholderText("Nom de la machine")
        self.text_field_machine.textChanged.connect(self.update_text_field_content_machine)
        layout.addWidget(self.text_field_machine)

        # Trois cases à cocher
        self.checkbox1 = QCheckBox("455")
        self.checkbox1.stateChanged.connect(self.update_checkbox1_state)
        self.checkbox2 = QCheckBox("730")
        self.checkbox2.stateChanged.connect(self.update_checkbox2_state)
        self.checkbox3 = QCheckBox("455 et 730")
        self.checkbox3.stateChanged.connect(self.update_checkbox3_state)
        layout.addWidget(self.checkbox1)
        layout.addWidget(self.checkbox2)
        layout.addWidget(self.checkbox3)

        # Champ texte
        self.text_field_iteration = QLineEdit()
        self.text_field_iteration.setPlaceholderText("Nombre d'itérations")
        self.text_field_iteration.textChanged.connect(self.update_text_field_content_iteration)
        layout.addWidget(self.text_field_iteration)

        # Champ texte
        self.text_field_frequence = QLineEdit()
        self.text_field_frequence.setPlaceholderText("Période d'enregistrement du .csv")
        self.text_field_frequence.textChanged.connect(self.update_text_field_content_periode)
        layout.addWidget(self.text_field_frequence)

        # Case à cocher si prise de focus à chaque snap
        self.checkbox4 = QCheckBox("Focus à chaque Snap")
        self.checkbox4.stateChanged.connect(self.update_checkbox4_state)
        layout.addWidget(self.checkbox4)

        # Champ texte
        self.text_field_frequence_snap = QLineEdit()
        self.text_field_frequence_snap.setPlaceholderText("Période d'enregistrement des snap")
        self.text_field_frequence_snap.textChanged.connect(self.update_text_field_content_periode_snap)
        layout.addWidget(self.text_field_frequence_snap)

        # Menu déroulant
        self.combo_box = QComboBox()
        self.combo_box.addItems(["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12",
                                 "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12",
                                 "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12",
                                 "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12",
                                 "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11", "E12",
                                 "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
                                 "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12",
                                 "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "H11", "H12"])
        self.combo_box.setCurrentText("A1")
        self.combo_box_selection = "A1"
        self.combo_box.currentTextChanged.connect(self.update_combo_box_selection)
        layout.addWidget(self.combo_box)

        # Bouton pour lancer l'acquisition de chauffe
        self.btn_process = QPushButton("Lancer la mesure")
        self.btn_process.clicked.connect(self.fonction_mesure_et_log)
        layout.addWidget(self.btn_process)

    def select_install_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Sélectionner le dossier d'installation du ZymoSoft")
        if dir_path:
            self.install_dir = dir_path  # Stocke le chemin dans la variable
            self.label_install.setText(dir_path)

    def select_save_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Sélectionner dossier d'enregistrement des snap du ZS")
        if dir_path:
            self.save_dir = dir_path  # Stocke le chemin dans la variable
            self.label_save.setText(dir_path)

    def update_checkbox1_state(self, state):
        self.checkbox1_state = state == 2  # 2 = coché, 0 = décoché

    def update_checkbox2_state(self, state):
        self.checkbox2_state = state == 2

    def update_checkbox3_state(self, state):
        self.checkbox3_state = state == 2

    def update_checkbox4_state(self, state):
        self.checkbox4_state = state == 2

    def update_text_field_content_machine(self, text):
        self.text_field_machine = text

    def update_text_field_content_iteration(self, text):
        self.text_field_iteration = text

    def update_text_field_content_periode(self, text):
        self.text_field_frequence = text

    def update_text_field_content_periode_snap(self, text):
        self.text_field_frequence_snap = text

    def update_combo_box_selection(self, text):
        self.combo_box_selection = text

    def fonction_mesure_et_log(self):
        log_de_mesure(self.install_dir,
                      self.save_dir,
                      self.checkbox1_state,
                      self.checkbox2_state,
                      self.checkbox3_state,
                      self.checkbox4_state,
                      self.text_field_machine,
                      self.text_field_iteration,
                      self.text_field_frequence,
                      self.combo_box_selection,
                      self.text_field_frequence_snap)

        mesure_chauffe_ZC_snap(self.install_dir,
                               self.save_dir,
                               self.text_field_machine,
                               self.combo_box_selection,
                               self.checkbox1_state,
                               self.checkbox2_state,
                               self.checkbox3_state,
                               self.checkbox4_state,
                               self.text_field_iteration,
                               self.text_field_frequence,
                               self.text_field_frequence_snap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())