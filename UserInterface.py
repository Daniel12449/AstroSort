from PySide6 import QtWidgets
from CustomWidgets import DropList
from PySide6.QtCore import QDateTime, QThreadPool

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AstroSort")
        
        # Function to add widget with label
        def add_horizontal_widgets(layout, widget1, widget2):
            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(widget1)
            hbox.addWidget(widget2)
            layout.addLayout(hbox)
           
        def add_triple_widgets(layout, widget1, widget2, widget3):
            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(widget1)
            hbox.addStretch()
            hbox.addWidget(widget2)
            hbox.addWidget(widget3)
            layout.addLayout(hbox)

        self.thread_manager = QThreadPool()
        
        self.mainWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.mainWidget)
        
        main_layout = QtWidgets.QHBoxLayout()
        layout_right = QtWidgets.QVBoxLayout()
        layout_left = QtWidgets.QVBoxLayout()
        
        self.mainWidget.setLayout(main_layout)
        
        # Left side Sublayouts
        main_layout.addLayout(layout_left)
        
        # Right side Sublayouts
        main_layout.addLayout(layout_right)
        
        # -- Begin left side layout --
        # Search Layout named Widgets
        self.combo_box_category = QtWidgets.QComboBox()
        self.combo_box_category.addItems(['Deep Sky Objects', 'Solar System', 'Comets', 'Constellations', 'Custom'])
        self.button_query = QtWidgets.QPushButton("Search")
        self.line_simbad_query = QtWidgets.QLineEdit(placeholderText="Enter Object")
        self.label_ra_coordinates = QtWidgets.QLabel()
        self.label_dec_coordinates = QtWidgets.QLabel()
        self.line_object_name1 = QtWidgets.QLineEdit()
        self.line_object_name2 = QtWidgets.QLineEdit()
        self.line_object_name3 = QtWidgets.QLineEdit()
        self.line_object_name4 = QtWidgets.QLineEdit()
        self.line_category = QtWidgets.QLineEdit()
        self.line_camera = QtWidgets.QLineEdit()
        self.line_focal_length = QtWidgets.QLineEdit()
        self.line_location = QtWidgets.QLineEdit()
        self.combo_box_query = QtWidgets.QComboBox()
        self.line_output_path = QtWidgets.QLineEdit()
        self.button_output_path = QtWidgets.QPushButton("...")
        self.button_start = QtWidgets.QPushButton("Copy and rename")
        self.date = QtWidgets.QDateEdit(calendarPopup=True)
        self.date.setDateTime(QDateTime.currentDateTime())
        self.progress_bar = QtWidgets.QProgressBar()
        self.button_cancel = QtWidgets.QPushButton("Cancel")
        
        # Left side Layout
        layout_left.addStretch()
        add_horizontal_widgets(layout_left, QtWidgets.QLabel("Choose category:"),  self.combo_box_category)
        
        # Stack definition
        self.stackedWidget = QtWidgets.QStackedWidget()
        
        # Search Widget
        self.searchLayout = QtWidgets.QWidget()
        hbox_astromeric_solution = QtWidgets.QVBoxLayout()
        hbox_astromeric_solution.addWidget(QtWidgets.QLabel("Search for Object"))
        add_horizontal_widgets(hbox_astromeric_solution, self.line_simbad_query, self.button_query)
        hbox_astromeric_solution.addWidget(self.combo_box_query)
        add_horizontal_widgets(hbox_astromeric_solution, QtWidgets.QLabel("RA: "),  self.label_ra_coordinates)
        add_horizontal_widgets(hbox_astromeric_solution, QtWidgets.QLabel("DEC: "), self.label_dec_coordinates)
        self.searchLayout.setLayout(hbox_astromeric_solution)
        
        # Manual entry widget 1
        self.manualEntryStack1 = QtWidgets.QWidget()
        hbox_manual_entry1 = QtWidgets.QHBoxLayout()
        add_horizontal_widgets(hbox_manual_entry1, QtWidgets.QLabel("Enter solar system object:"),  self.line_object_name1)
        self.manualEntryStack1.setLayout(hbox_manual_entry1)
        
        # Manual entry widget 2
        self.manualEntryStack2 = QtWidgets.QWidget()
        hbox_manual_entry2 = QtWidgets.QHBoxLayout()
        add_horizontal_widgets(hbox_manual_entry2, QtWidgets.QLabel("Enter comet name:"),  self.line_object_name2)
        self.manualEntryStack2.setLayout(hbox_manual_entry2)
        
        # Manual entry widget 3
        self.manualEntryStack3 = QtWidgets.QWidget()
        hbox_manual_entry3 = QtWidgets.QHBoxLayout()
        add_horizontal_widgets(hbox_manual_entry3, QtWidgets.QLabel("Enter constellation:"),  self.line_object_name3)
        self.manualEntryStack3.setLayout(hbox_manual_entry3)
        
        # Manual entry widget 4
        self.manualEntryStack4 = QtWidgets.QWidget()
        hbox_manual_entry4 = QtWidgets.QVBoxLayout()
        add_horizontal_widgets(hbox_manual_entry4, QtWidgets.QLabel("Enter category:"),  self.line_category)
        add_horizontal_widgets(hbox_manual_entry4, QtWidgets.QLabel("Enter object name:"),  self.line_object_name4)
        self.manualEntryStack4.setLayout(hbox_manual_entry4)
     
        # Adding Widgets to stack
        self.stackedWidget.addWidget(self.searchLayout)
        self.stackedWidget.addWidget(self.manualEntryStack1)
        self.stackedWidget.addWidget(self.manualEntryStack2) 
        self.stackedWidget.addWidget(self.manualEntryStack3) 
        self.stackedWidget.addWidget(self.manualEntryStack4)       
        layout_left.addWidget(self.stackedWidget)    

        # Spacer
        layout_left.addWidget(QtWidgets.QLabel(""))
        
        # Input fields
        add_horizontal_widgets(layout_left, QtWidgets.QLabel("Camera: "), self.line_camera)
        add_horizontal_widgets(layout_left, QtWidgets.QLabel("Focal Length: "), self.line_focal_length)
        add_horizontal_widgets(layout_left, QtWidgets.QLabel("Location: "), self.line_location)
        add_horizontal_widgets(layout_left, QtWidgets.QLabel("Date: "), self.date)
        layout_left.addStretch()
        layout_left.addWidget(QtWidgets.QLabel("Output Path"))
        add_horizontal_widgets(layout_left, self.line_output_path, self.button_output_path)
        layout_left.addWidget(self.button_start)
        layout_left.addStretch()
        add_horizontal_widgets(layout_left, self.progress_bar, self.button_cancel)
        
        # -- Begin right side layout --
        # Search Layout named Widgets
        self.list_lights = DropList(objectName='list_lights')
        self.list_darks = DropList(objectName='list_darks')
        self.list_flats = DropList(objectName='list_flats')
        self.list_bias = DropList(objectName='list_bias')
        
        self.button_add_lights = QtWidgets.QPushButton("+")
        self.button_del_lights = QtWidgets.QPushButton("-")
        
        self.button_add_darks = QtWidgets.QPushButton("+")
        self.button_del_darks = QtWidgets.QPushButton("-")
        
        self.button_add_flats = QtWidgets.QPushButton("+")
        self.button_del_flats = QtWidgets.QPushButton("-")
        
        self.button_add_bias = QtWidgets.QPushButton("+")
        self.button_del_bias = QtWidgets.QPushButton("-")
        
        # Right side layout
        add_triple_widgets(layout_right, QtWidgets.QLabel("Light files"), self.button_add_lights, self.button_del_lights)
        layout_right.addWidget(self.list_lights)
        
        add_triple_widgets(layout_right, QtWidgets.QLabel("Dark files"), self.button_add_darks, self.button_del_darks)
        layout_right.addWidget(self.list_darks)
        
        add_triple_widgets(layout_right, QtWidgets.QLabel("Flat files"), self.button_add_flats, self.button_del_flats)
        layout_right.addWidget(self.list_flats)
        
        add_triple_widgets(layout_right, QtWidgets.QLabel("Bias files"), self.button_add_bias, self.button_del_bias)
        layout_right.addWidget(self.list_bias)
        
        layout_right.addStretch()
        
        # Status Bar
        self.statusBar_line_status = QtWidgets.QLabel("Not all required fields are filled.")
        self.statusBar_line_filecount = QtWidgets.QLabel("Lights: 0 · Darks: 0 · Flats: 0 · Bias: 0")
        self.button_reset = QtWidgets.QPushButton("Reset")
        self.statusBar().size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.statusBar().addWidget(self.statusBar_line_status)
        self.statusBar().addWidget(QtWidgets.QLabel("  |  "))
        self.statusBar().addWidget(self.statusBar_line_filecount)
        self.statusBar().addPermanentWidget(self.button_reset)
        
        # Reset Dialog
        self.button_reset.clicked.connect(self.openResetDialog)
        
    def openResetDialog(self, s):
        self.resetDialog = ResetWindow()
        self.resetDialog.exec()

    def displayStack(self, i):
        from AstroSort import updateCategory
        self.stackedWidget.setCurrentIndex(i)
        updateCategory(i)
            
class ResetWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Reset")

        QBtn = (
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        self.checkbox_clear_lights = QtWidgets.QCheckBox("Clear light files")
        self.checkbox_clear_lights.setChecked(True)
        self.checkbox_clear_darks = QtWidgets.QCheckBox("Clear dark files")
        self.checkbox_clear_darks.setChecked(True)
        self.checkbox_clear_flats = QtWidgets.QCheckBox("Clear flat files")
        self.checkbox_clear_flats.setChecked(True)
        self.checkbox_clear_bias = QtWidgets.QCheckBox("Clear bias files")
        self.checkbox_clear_bias.setChecked(True)
        self.checkbox_clear_metadata = QtWidgets.QCheckBox("Clear metadata")

        layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Choose what to reset")
        layout.addWidget(message)
        layout.addStretch()
        layout.addWidget(self.checkbox_clear_lights)
        layout.addWidget(self.checkbox_clear_darks)
        layout.addWidget(self.checkbox_clear_flats)
        layout.addWidget(self.checkbox_clear_bias)
        layout.addStretch()
        layout.addWidget(self.checkbox_clear_metadata)
        layout.addStretch()
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)