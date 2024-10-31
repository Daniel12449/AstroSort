from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QDateTime
from CustomWidgets import searchWidget

def add_horizontal_widgets(layout, widget1, widget2):
            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(widget1)
            hbox.addWidget(widget2)
            layout.addLayout(hbox)
            
def add_triple_widgets(layout, widget1, widget2, widget3, stretch):
            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(widget1)
            if stretch: hbox.addStretch()
            hbox.addWidget(widget2)
            hbox.addWidget(widget3)
            layout.addLayout(hbox)

class main_tab(QtWidgets.QWidget):
     def __init__(self, parent=None, *args, **kwargs):
        super(main_tab, self).__init__(parent, *args, **kwargs)
    
    ## Setup of Main tab
        self.tab1_main_layout = QtWidgets.QHBoxLayout()
        self.tab1_left_layout = QtWidgets.QVBoxLayout()
        self.tab1_right_layout = QtWidgets.QFrame()
        self.tab1_right_layout.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        self.tab1_right_layout.setLineWidth(2)
        
        ## Right Side
        # Object definition
        self.layout_right_box = QtWidgets.QVBoxLayout()
        self.label_logo = QtWidgets.QLabel("AstroSort", alignment=Qt.AlignmentFlag.AlignHCenter )
        self.label_logo.setStyleSheet("font-weight: bold; font-size: 45px")
        self.label_version = QtWidgets.QLabel("v1.0", alignment=Qt.AlignmentFlag.AlignHCenter )
        self.label_count_lights = QtWidgets.QLabel("0", alignment=Qt.AlignmentFlag.AlignRight)
        self.label_count_darks = QtWidgets.QLabel("0", alignment=Qt.AlignmentFlag.AlignRight)
        self.label_count_flats = QtWidgets.QLabel("0", alignment=Qt.AlignmentFlag.AlignRight)
        self.label_count_bias = QtWidgets.QLabel("0", alignment=Qt.AlignmentFlag.AlignRight)
    
        # Layout definition
        self.layout_right_box.addWidget(self.label_logo)
        self.layout_right_box.addWidget(self.label_version)
        self.layout_right_box.addStretch()
        vbox_count = QtWidgets.QVBoxLayout(alignment=Qt.AlignmentFlag.AlignHCenter )
        add_horizontal_widgets(vbox_count, QtWidgets.QLabel('Light Files:'), self.label_count_lights)
        add_horizontal_widgets(vbox_count, QtWidgets.QLabel('Dark Files:'), self.label_count_darks)
        add_horizontal_widgets(vbox_count, QtWidgets.QLabel('Flat Files:'), self.label_count_flats)
        add_horizontal_widgets(vbox_count, QtWidgets.QLabel('Bias Files:'), self.label_count_bias)
        self.layout_right_box.addLayout(vbox_count)
        self.layout_right_box.addStretch()
        self.tab1_right_layout.setLayout(self.layout_right_box)
        
        ## Left Side
        # Search box
        self.search_box = searchWidget()
        self.tab1_left_layout.addWidget(self.search_box)
        
        self.tab1_main_layout.addLayout(self.tab1_left_layout, 3)
        self.tab1_main_layout.addWidget(self.tab1_right_layout, 1)
        self.tab1_left_layout.addStretch()
        
        # Process 
        # Object definition
        self.checkbox_filename = QtWidgets.QCheckBox()
        self.line_output_path = QtWidgets.QLineEdit()
        self.button_output_path = QtWidgets.QPushButton("...")
        self.progress_bar = QtWidgets.QProgressBar()
        self.button_start = QtWidgets.QPushButton("Start")
        self.button_cancel = QtWidgets.QPushButton("Cancel")
        
        # Layout definition
        self.hbox_progress = QtWidgets.QHBoxLayout()
        self.hbox_progress.addWidget(self.progress_bar)
        self.hbox_progress.addWidget(self.button_start )
        self.hbox_progress.addWidget(self.button_cancel)
        
        add_horizontal_widgets(self.tab1_left_layout, QtWidgets.QLabel("Replace filenames with imgX: "), self.checkbox_filename) 
        self.tab1_left_layout.addWidget(QtWidgets.QLabel("Output path & start process"))
        add_horizontal_widgets(self.tab1_left_layout, self.line_output_path, self.button_output_path)
        self.tab1_left_layout.addLayout(self.hbox_progress)          
        self.setLayout(self.tab1_main_layout)

class files_tab(QtWidgets.QWidget):
     def __init__(self, parent=None, *args, **kwargs):
        super(files_tab, self).__init__(parent, *args, **kwargs)
    
        ## Setup of Files Tab
        self.tab2_layout = QtWidgets.QVBoxLayout()
        self.treeWidget = QtWidgets.QTreeWidget()
        self.button_remove_selected = QtWidgets.QPushButton("Remove selected")
        self.button_remove_all = QtWidgets.QPushButton("Clear")
        self.button_refresh = QtWidgets.QPushButton("Refresh")
        self.checkbox_paths = QtWidgets.QCheckBox()
        
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabels(['File type'])
        self.treeWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.hbox_file_edit_bar = QtWidgets.QHBoxLayout()
        self.hbox_file_edit_bar.addWidget(QtWidgets.QLabel("Added Files"))
        self.hbox_file_edit_bar.addStretch()
        self.hbox_file_edit_bar.addWidget(self.button_refresh)
        self.hbox_file_edit_bar.addWidget(self.button_remove_selected)
        self.hbox_file_edit_bar.addWidget(self.button_remove_all)
        
        self.tab2_layout.addLayout(self.hbox_file_edit_bar)
        self.tab2_layout.addWidget(self.treeWidget)
        add_horizontal_widgets(self.tab2_layout, QtWidgets.QLabel("Show file paths in list"), self.checkbox_paths)
        self.setLayout(self.tab2_layout)

class structure_tab(QtWidgets.QWidget):
     def __init__(self, parent=None, *args, **kwargs):
        super(structure_tab, self).__init__(parent, *args, **kwargs)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(QtWidgets.QLabel("Still to do"))
        self.setLayout(self.main_layout)
        

class metadata_tab(QtWidgets.QWidget):
     def __init__(self, parent=None, *args, **kwargs):
        super(metadata_tab, self).__init__(parent, *args, **kwargs)
        
        self.main_layout = QtWidgets.QVBoxLayout()
        self.metadata_box_layout = QtWidgets.QHBoxLayout()
        
        # General object definition
        self.header = QtWidgets.QLabel('Image Metadata')
        self.header.setStyleSheet(''' font-size: 18px; ''')
        self.separator = QtWidgets.QFrame()
        self.separator.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Expanding)
        self.button_scan_metadata = QtWidgets.QPushButton('Scan Files') 
        
        # Header Layout
        self.header_layout = QtWidgets.QHBoxLayout()
        self.header_layout.addWidget(self.header)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.button_scan_metadata)
        self.main_layout.addLayout(self.header_layout)
        
        # Left object definition
        self.exif_camera = QtWidgets.QLineEdit()
        self.exif_exposure = QtWidgets.QLineEdit()
        self.exif_date = QtWidgets.QDateEdit(calendarPopup=True)
        self.exif_date.setDateTime(QDateTime.currentDateTime())
        self.exif_iso = QtWidgets.QLineEdit()
        self.exif_focal_length = QtWidgets.QLineEdit()
        self.line_location = QtWidgets.QLineEdit()
        self.label_exif = QtWidgets.QLabel('Exif image metadata')
        self.label_exif.setStyleSheet("font-weight: bold")
        self.label_fits = QtWidgets.QLabel('FITS image metadata')
        self.label_fits.setStyleSheet("font-weight: bold")
        self.label_general = QtWidgets.QLabel("General Metadata")
        self.label_general.setStyleSheet("font-weight: bold")
                
        # Left column
        self.left_column = QtWidgets.QFormLayout()
        self.left_column.addRow(self.label_exif)
        self.left_column.addRow('Camera model: ', self.exif_camera)             #"EXIF:Model"
        self.left_column.addRow('Exposure time: ', self.exif_exposure)          #"EXIF:ExposureTime"
        self.left_column.addRow('Date taken: ', self.exif_date )                #"EXIF:DateTimeOriginal"
        self.left_column.addRow('ISO: ', self.exif_iso)                         #"EXIF:ISO"
        self.left_column.addRow('Focal length: ', self.exif_focal_length )      #"EXIF:FocalLength"
        
        self.left_column.addRow(QtWidgets.QLabel(""));
        self.left_column.addRow(self.label_general);
        self.left_column.addRow("Location: ", self.line_location )
        
        # Right object definition
        self.fits_camera = QtWidgets.QLineEdit()
        self.fits_exposure = QtWidgets.QLineEdit()
        self.fits_date = QtWidgets.QDateEdit(calendarPopup=True)
        self.fits_date.setDateTime(QDateTime.currentDateTime())
        self.fits_gain = QtWidgets.QLineEdit()
        self.fits_focal_length = QtWidgets.QLineEdit()
        self.fits_telescope = QtWidgets.QLineEdit()
        self.fits_object = QtWidgets.QLineEdit()
        self.fits_temperature = QtWidgets.QLineEdit()
        
        # Right column
        self.right_column = QtWidgets.QFormLayout()
        self.right_column.addRow(self.label_fits)
        self.right_column.addRow('Camera model: ', self.fits_camera)            #"FITS:Instrument"
        self.right_column.addRow('Exposure time', self.fits_exposure)           #"FITS:Exposure"
        self.right_column.addRow('Date taken: ', self.fits_date)                #"FITS:ObservationDate"
        self.right_column.addRow('Gain: ', self.fits_gain)                      #"FITS:Gain"
        self.right_column.addRow('Focal length', self.fits_focal_length )       #"FITS:Focallen"
        self.right_column.addRow('Telescope: ', self.fits_telescope)            #"FITS:Telescope"
        self.right_column.addRow('Object: ', self.fits_object)                  #"FITS:Object"
        self.right_column.addRow('Sensor temperature: ', self.fits_temperature) #"FITS:Set-temp"        

        self.metadata_box_layout.addLayout(self.left_column)
        self.metadata_box_layout.addLayout(self.right_column)
        
        # Bottom Layout
        # Object definition
        self.bottom_layout = QtWidgets.QVBoxLayout()
        self.header_additional = QtWidgets.QLabel("General Metadata")
        self.header_additional.setStyleSheet("font-weight: bold")
        self.line_exposure_dark = QtWidgets.QLineEdit()
        self.line_exposure_flat = QtWidgets.QLineEdit()
        self.line_exposure_bias = QtWidgets.QLineEdit()
        self.line_iso_dark = QtWidgets.QLineEdit()
        self.line_iso_flat = QtWidgets.QLineEdit()
        self.line_iso_bias = QtWidgets.QLineEdit()
        self.label_exposure = QtWidgets.QLabel("Exposure")
        self.label_exposure.setAlignment(Qt.AlignHCenter)
        self.label_iso = QtWidgets.QLabel("ISO / Gain")
        self.label_iso.setAlignment(Qt.AlignHCenter)
        
        # Layout
        self.bottom_layout.addWidget(self.header_additional)
        add_triple_widgets(self.bottom_layout, QtWidgets.QLabel("File type"), self.label_exposure, self.label_iso, False)
        add_triple_widgets(self.bottom_layout, QtWidgets.QLabel("Dark files"), self.line_exposure_dark, self.line_iso_dark, True)  
        add_triple_widgets(self.bottom_layout, QtWidgets.QLabel("Flat files  "), self.line_exposure_flat, self.line_iso_flat, True)
        add_triple_widgets(self.bottom_layout, QtWidgets.QLabel("Bias files "), self.line_exposure_bias, self.line_iso_bias, True)
        
        self.main_layout.addLayout(self.metadata_box_layout)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.bottom_layout)
        self.setLayout(self.main_layout)