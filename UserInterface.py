from PySide6 import QtWidgets
from CustomWidgets import DropList
from PySide6.QtCore import QDateTime, QThreadPool

class MainWindow(QtWidgets.QWidget):
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
        
        main_layout = QtWidgets.QHBoxLayout()
        layout_right = QtWidgets.QVBoxLayout()
        layout_left = QtWidgets.QVBoxLayout()
        
        self.setLayout(main_layout)
        
        # Left side Sublayouts
        main_layout.addLayout(layout_left)
        
        # Right side Sublayouts
        main_layout.addLayout(layout_right)
        
        # -- Begin left side layout --
        # Search Layout named Widgets
        self.combo_box_category = QtWidgets.QComboBox()
        self.combo_box_category.addItems(['Deep Sky Objects', 'Solar System', 'Comets', 'Constellations'])
        self.button_query = QtWidgets.QPushButton("Search")
        self.line_simbad_query = QtWidgets.QLineEdit(placeholderText="Enter Object")
        self.label_ra_coordinates = QtWidgets.QLabel()
        self.label_dec_coordinates = QtWidgets.QLabel()
        self.line_object_name1 = QtWidgets.QLineEdit()
        self.line_object_name2 = QtWidgets.QLineEdit()
        self.line_object_name3 = QtWidgets.QLineEdit()
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
     
        
        # Adding Widgets to stack
        self.stackedWidget.addWidget(self.searchLayout)
        self.stackedWidget.addWidget(self.manualEntryStack1)
        self.stackedWidget.addWidget(self.manualEntryStack2) 
        self.stackedWidget.addWidget(self.manualEntryStack3)     
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
            
    def displayStack(self, i):
        global category

        self.stackedWidget.setCurrentIndex(i)
        
        if i == 1:
            category = "Deep Sky Objects"
        elif i == 2:
            category = "Solar System"
        elif i == 3:
            category = "Comets"
        elif i == 4:
            category = "Constellations"

            