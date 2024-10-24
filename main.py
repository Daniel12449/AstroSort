import sys, pathlib, logging, shutil
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QDateTime, QThreadPool, Slot
from astroquery.simbad import Simbad
from astroquery.jplsbdb import SBDB
from CustomWidgets import DropButton, searchWidget
from global_vars import *

# Subclass QMainWindow to customize your application's main window
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AstroSort")
        self.thread_manager = QThreadPool()
        
        # Layout functions
        def add_horizontal_widgets(layout, widget1, widget2):
            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(widget1)
            hbox.addWidget(widget2)
            layout.addLayout(hbox)
        
        # Main layout
        
        self.tabWidget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabWidget)
        
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        self.tab3 = QtWidgets.QWidget()

        self.tabWidget.addTab(self.tab1, "Main")
        self.tabWidget.addTab(self.tab2, "Files")
        self.tabWidget.addTab(self.tab3, "Process")
        
        ## Setup of Main tab
        self.tab1_main_layout = QtWidgets.QHBoxLayout()
        self.tab1_left_layout = QtWidgets.QVBoxLayout()
        self.tab1_right_layout = QtWidgets.QVBoxLayout()
        
        ## Left Side
        # Search box
        self.search_box = searchWidget()
        self.tab1_left_layout.addWidget(self.search_box)
        
        self.tab1_main_layout.addLayout(self.tab1_left_layout, 3)
        self.tab1_main_layout.addLayout(self.tab1_right_layout, 1)
        self.tab1.setLayout(self.tab1_main_layout)
        self.tab1_left_layout.addStretch()
        
        # Information Form
        # Object definitions
        self.formLayout = QtWidgets.QFormLayout()
        self.line_camera = QtWidgets.QLineEdit()
        self.line_focal_length = QtWidgets.QLineEdit()
        self.line_location = QtWidgets.QLineEdit()
        self.date = QtWidgets.QDateEdit(calendarPopup=True)
        self.date.setDateTime(QDateTime.currentDateTime())
        self.header_general = QtWidgets.QLabel('General information')
        self.header_general.setStyleSheet(''' font-size: 18px; ''')
        self.header_general.setAlignment(Qt.AlignCenter)
        
        self.formLayout.addRow(self.header_general)     
        self.formLayout.addRow('Date : ', self.date )  
        self.formLayout.addRow('Camera identifier: ', self.line_camera )
        self.formLayout.addRow('Focal length: ', self.line_focal_length )      
        self.formLayout.addRow('Location: ', self.line_location )      
                  
        
        self.tab1_left_layout.addLayout(self.formLayout)
        self.tab1_left_layout.addStretch()
        
        ## Setup of Files Tab
        self.tab2_layout = QtWidgets.QVBoxLayout()
        self.treeWidget = QtWidgets.QTreeWidget()
        self.label_selected_inputpath = QtWidgets.QLabel("No file selected.")
        self.label_selected_outputpath = QtWidgets.QLabel("No file selected. Prepare filepaths first.")
        self.button_remove_selected = QtWidgets.QPushButton("Remove selected")
        self.button_remove_all = QtWidgets.QPushButton("Clear")
        self.button_refresh = QtWidgets.QPushButton("Refresh")
        
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
        add_horizontal_widgets(self.tab2_layout, QtWidgets.QLabel("Input Path: "), self.label_selected_inputpath)
        add_horizontal_widgets(self.tab2_layout, QtWidgets.QLabel("Output Path: "), self.label_selected_outputpath)
        self.tab2.setLayout(self.tab2_layout)
        
        ## Setup of Process tab
        #Object definitions
        self.label_process_name = QtWidgets.QLabel()
        self.label_process_category = QtWidgets.QLabel()
        self.label_process_date = QtWidgets.QLabel()
        self.label_process_camera = QtWidgets.QLabel()
        self.label_process_focal_length = QtWidgets.QLabel()
        self.label_process_location = QtWidgets.QLabel()
        self.label_base_path = QtWidgets.QLabel()
        self.label_process_parameters = QtWidgets.QLabel("Process Parameters")
        self.label_process_parameters.setStyleSheet(''' font-size: 18px; ''')
        self.line_output_path = QtWidgets.QLineEdit()
        self.button_output_path = QtWidgets.QPushButton("...")
        self.progress_bar = QtWidgets.QProgressBar()
        self.button_start = QtWidgets.QPushButton("Start")
        self.button_cancel = QtWidgets.QPushButton("Cancel")
        
        #Layout definitions
        self.process_layout = QtWidgets.QVBoxLayout()
        self.process_layout.setAlignment(Qt.AlignHCenter)
        self.process_layout.addWidget(self.label_process_parameters )
        
        self.formLayout_process = QtWidgets.QFormLayout()
        self.formLayout_process.addRow('Object Name : ', self.label_process_name)
        self.formLayout_process.addRow('Object Category : ', self.label_process_category)
        self.formLayout_process.addRow('Date : ', self.label_process_date)  
        self.formLayout_process.addRow('Camera identifier: ', self.label_process_camera)
        self.formLayout_process.addRow('Focal length: ', self.label_process_focal_length)      
        self.formLayout_process.addRow('Location: ', self.label_process_location) 
        self.formLayout_process.addRow(QtWidgets.QLabel("")) 
        self.formLayout_process.addRow('Base path: ', self.label_base_path) 
        
        self.hbox_progress = QtWidgets.QHBoxLayout()
        self.hbox_progress.addWidget(self.progress_bar)
        self.hbox_progress.addWidget(self.button_start )
        self.hbox_progress.addWidget(self.button_cancel)
        
        self.process_layout.addLayout(self.formLayout_process)
        add_horizontal_widgets(self.process_layout, self.line_output_path, self.button_output_path)
        self.process_layout.addLayout(self.hbox_progress)
        self.tab3.setLayout(self.process_layout)
        
        ## Setup of Statusbar
        self.button_add_lights = DropButton("+ Lights", objectName='button_add_lights')
        self.button_add_darks = DropButton("+ Darks ", objectName='button_add_darks')
        self.button_add_flats = DropButton("+ Flats ", objectName='button_add_flats')
        self.button_add_bias = DropButton("+ Bias  ", objectName='button_add_bias')
        self.button_reset = QtWidgets.QPushButton("Reset")
        self.button_prepare = QtWidgets.QPushButton("Prepare")
        #self.statusBar().size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.statusBar().addWidget(self.button_add_lights)
        self.statusBar().addWidget(self.button_add_darks)
        self.statusBar().addWidget(self.button_add_flats)
        self.statusBar().addWidget(self.button_add_bias)
        self.statusBar().addPermanentWidget(self.button_prepare)
        self.statusBar().addPermanentWidget(self.button_reset)
        
## -- Start of functions --

def openFiles(target):
    file_list = QtWidgets.QFileDialog.getOpenFileNames()[0]
    path_list = [pathlib.Path(p) for p in file_list]
    
    if target == 'lights':
        for path in path_list:
            output_files_list['light_input'].append(path)
            logging.info("Light file added: " + str(path))
    elif target == 'darks':
        for path in path_list:
            output_files_list['dark_input'].append(path)
            logging.info("Dark file added: " + str(path))
    elif target == 'flats':
        for path in path_list:
            output_files_list['flat_input'].append(path)
            logging.info("Flat file added: " + str(path))
    elif target == 'bias':
        for path in path_list:
            output_files_list['bias_input'].append(path)
            logging.info("Bias file added: " + str(path))
    populateTreeWidget()
            
def populateTreeWidget():
        window.treeWidget.clear()
        
        combined_file_list = {
            'Light files': output_files_list['light_input'],
            'Dark files': output_files_list['dark_input'],
            'Flat files': output_files_list['flat_input'],
            'Bias files': output_files_list['bias_input']
        }
        
        items = []
        for key, values in combined_file_list.items():
            item = QtWidgets.QTreeWidgetItem([key])
            for value in values:
                child = QtWidgets.QTreeWidgetItem([value.name])
                item.addChild(child)
            items.append(item)

        window.treeWidget.insertTopLevelItems(0, items)
        window.treeWidget.resizeColumnToContents(0)
    
def removeItems():
    items = window.treeWidget.selectedItems()
    
    for item in items:
        parent = item.parent().text(0)
        name = item.text(0)
        logging.info('Removing ' + name + ' from ' + parent)
        
        if parent == "Light files": parent = 'light_input'
        if parent == "Dark files": parent = 'dark_input'
        if parent == "Flat files": parent = 'flat_input'
        if parent == "Bias files": parent = 'bias_input'
        
        output_files_list[parent].remove(pathlib.Path(next((entry for entry in output_files_list[parent] if name in str(entry)), None)))
    populateTreeWidget()

def clearFileLists():
    output_files_list['light_input'].clear()
    output_files_list['dark_input'].clear()
    output_files_list['flat_input'].clear()
    output_files_list['bias_input'].clear()
    
    output_files_list['light_output'].clear()
    output_files_list['dark_output'].clear()
    output_files_list['flat_output'].clear()
    output_files_list['bias_output'].clear()
    populateTreeWidget()
    
def updateFilePathLabels():
    item = window.treeWidget.currentItem()
    try:
        parent = item.parent().text(0)
    except:
        logging.info('Selected Entry has no file paths.')
        return
    
    if parent == "Light files": 
        input_key = 'light_input'
        output_key = 'light_output'
    if parent == "Dark files": 
        input_key = 'dark_input'
        output_key = 'dark_output'
    if parent == "Flat files": 
        input_key = 'flat_input'
        output_key = 'flat_output'
    if parent == "Bias files": 
        input_key = 'bias_input'
        output_key = 'bias_output'
    
    input_path = next((entry for entry in output_files_list[input_key] if item.text(0) in str(entry)), 'No file selected.')
    output_path = next((entry for entry in output_files_list[output_key] if item.text(0) in str(entry)), 'No file selected. Prepare filepaths first.')
    
    window.label_selected_inputpath.setText(str(input_path))
    window.label_selected_outputpath.setText(str(output_path))

def querySimbad():
    window.search_box.combo_box_query_simbad.clear()
    queryString = window.search_box.line_simbad_query.text()
    
    simbad = Simbad()
    simbad.ROW_LIMIT = 10
    
    if queryString != "":
        try:
            simbad_results = simbad.query_region(queryString)
            for i in range(len(simbad_results)):
                name = simbad_results[i]["MAIN_ID"]
                if "NAME" in name: 
                    name = name.strip("NAME ")
                coordinates = [simbad_results[i]["RA"], simbad_results[i]["DEC"], name]
                window.search_box.combo_box_query_simbad.addItem(name, coordinates)
        except: 
            QtWidgets.QMessageBox.about(None, "Simbad Search", "Simbad was unable to find an object")
            logging.warning("Simbad was unable to find a matching object.")

def updateSimbadCoordinates():
    window.search_box.label_ra_coordinates_simbad.clear()
    window.search_box.label_dec_coordinates_simbad.clear()
    
    current_combobox_data = window.search_box.combo_box_query_simbad.currentData()

    if isinstance(current_combobox_data, list):
        window.search_box.label_ra_coordinates_simbad.setText(current_combobox_data[0])
        window.search_box.label_dec_coordinates_simbad.setText(current_combobox_data[1])
    
    logging.info('Simbad coordinates set to: ' + str(current_combobox_data))
    

def querySBDB():
    queryString = window.search_box.line_sbdb_query.text()

    if queryString != "":
        sbdb = SBDB.query(queryString)
        
        if 'message' in sbdb.keys():
            QtWidgets.QMessageBox.about(None, "SBDB Search", "SBDB was unable to find an object")        
        
        elif 'object' in sbdb.keys():
            window.search_box.label_full_name.setText(sbdb['object']['fullname'])
            window.search_box.label_type.setText(sbdb['object']['orbit_class']['name'])
            
            if 'shortname' in sbdb['object'].keys():
                window.search_box.label_short_name.setText(sbdb['object']['shortname'])
            else:
                window.search_box.label_short_name.setText('-/-')

def gatherProcessParameters():
    global output_final_dir 
    current_category = window.search_box.currentIndex()
    date = str(window.date.date().year()) + "-" + str(window.date.date().month()) + "-" + str(window.date.date().day())
    location = window.line_location.text()
    camera = window.line_camera.text()
    focal_length = window.line_focal_length.text()
    
    if location == "" or camera == "" or focal_length == "":
        QtWidgets.QMessageBox.about(None, "General Parameters", "Please fill location, camera and focal length fields.")
        raise ValueError('Please fill location, camera and focal length fields.')
    
    if current_category == 0:
        object_category = "DeepSky"
        object_name_temp = window.search_box.combo_box_query_simbad.currentData()
        if isinstance(object_name_temp, list):
            object_name = object_name_temp[2].replace(" ", "")
        else:
            QtWidgets.QMessageBox.about(None, "Deep Sky Object", "Please select an object.")
            raise ValueError
    
    elif current_category == 1:
        object_name_temp = window.search_box.combo_box_planets.currentText()
        custom_object_name_tmep = window.search_box.line_largeBodies_custom.text()
        object_category = "LargeSolarSystemBodies"        
        
        if object_name_temp == 'Custom' and custom_object_name_tmep != '':
            object_name = custom_object_name_tmep
        elif object_name_temp == 'Custom' and custom_object_name_tmep == '':
            QtWidgets.QMessageBox.about(None, "Large Solar System Bodies", "Please enter custom object or select different entry.")
            raise ValueError
        elif object_name_temp != 'Custom':
            object_name = object_name_temp
            
    elif current_category == 2:
        object_category = "SmallSolarSystemBodies"
        object_name_long = window.search_box.label_full_name.text()
        object_name_short = window.search_box.label_short_name.text()
        
        if object_name_long == "":
            QtWidgets.QMessageBox.about(None, "Small Solar System Bodies", "Please select an object.")
            raise ValueError
        
        if object_name_short != '-/-':
            object_name = object_name_short.replace(" ", "-").replace("/", "")
        else: 
            object_name = object_name_long.replace(" ", "-").replace("/", "")
    
    elif current_category == 3:
        object_category = "Constellations"
        object_name_tmp = window.search_box.line_constellation.text()
        
        if object_name_tmp != "":
            object_name = object_name_tmp
        else: 
            QtWidgets.QMessageBox.about(None, "Constellations", "Please enter constellation or select different category.")
            raise ValueError
    
    elif current_category == 4:
        object_category_temp = window.search_box.line_custom_category.text()
        object_name_tmp = window.search_box.line_custom_name.text()
        
        if object_name_tmp != "" and object_category_temp != "":
            object_name = object_name_tmp
            object_category = object_category_temp
        else:
            QtWidgets.QMessageBox.about(None, "Custom Category", "Please enter a custom name and category.")
            raise ValueError

    window.label_process_name.setText(str(object_name))
    window.label_process_category.setText(str(object_category))
    window.label_process_date.setText(str(date))
    window.label_process_camera.setText(str(camera))
    window.label_process_focal_length.setText(str(location))
    window.label_process_location.setText(str(focal_length))
    
    output_path_tmp = window.line_output_path.text()
    
    if output_path_tmp != "":
        output_path = pathlib.Path(output_path_tmp)
    else:
        QtWidgets.QMessageBox.about(None, "Processing", "Please enter an output path.")
        raise ValueError
    
    output_final_dir = output_path / pathlib.Path(object_category) / pathlib.Path(object_name) / pathlib.Path(date + "_" + location) / pathlib.Path(camera + "_" + focal_length)
    window.label_base_path.setText(str(output_final_dir))

def setBaseDirectory():
    outputPath = QtWidgets.QFileDialog.getExistingDirectory()
    window.line_output_path.setText(outputPath)
    logging.info("Output path set to: " + str(outputPath))
    
def setCancel():
    global canceled
    if canceled == False:
        canceled = True
        logging.warning("Process canceled!")
    elif canceled == True:
        canceled = False
        logging.info("Process reset.") 
        
def preparePaths():
    global output_final_dir, output_files_list
    try:
        gatherProcessParameters()   
        camera = window.label_process_camera.text()
        focal_length = window.label_process_focal_length.text()
    except:
        QtWidgets.QMessageBox.about(None, "Starting Process", "Please correct any errors and try again.")
        return
    
    # Clear output paths
    output_files_list['light_output'].clear()
    output_files_list['dark_output'].clear()
    output_files_list['flat_output'].clear()
    output_files_list['bias_output'].clear()
          
    for file in output_files_list['light_input']:
        output_dir = output_final_dir / pathlib.Path('LIGHTS') 
        filename = "L_" + camera + "_" + focal_length + "_" + file.name
        output_files_list['light_output'].append(output_dir / pathlib.Path(filename))
        
    for file in output_files_list['dark_input']:
        output_dir = output_final_dir / pathlib.Path('DARKS') 
        filename = "D_" + camera + "_" + focal_length + "_" + file.name
        output_files_list['dark_output'].append(output_dir / pathlib.Path(filename))
        
    for file in output_files_list['flat_input']:
        output_dir = output_final_dir / pathlib.Path('FLATS') 
        filename = "F_" + camera + "_" + focal_length + "_" + file.name
        output_files_list['flat_output'].append(output_dir / pathlib.Path(filename))
        
    for file in output_files_list['bias_input']:
        output_dir = output_final_dir / pathlib.Path('BIAS') 
        filename = "B_" + camera + "_" + focal_length + "_" + file.name
        output_files_list['bias_output'].append(output_dir / pathlib.Path(filename))
   
@Slot()      
def copyProcess():
    #Setup of Progress bar
    total_files = len(output_files_list['light_output']) + len(output_files_list['dark_output']) + len(output_files_list['flat_output']) + len(output_files_list['bias_output'])
    window.progress_bar.setMinimum(0)
    window.progress_bar.setMaximum(total_files)
    logging.info('Number of files to process: ' + str(total_files))
    current_file = 0
    
    # Create file paths
    if len(output_files_list['light_output']) != 0:
        logging.info('Created LIGHTS subdirectory')
        light_subfolder = output_final_dir / pathlib.Path('LIGHTS') 
        light_subfolder.mkdir(parents=True, exist_ok=True)
        
    if len(output_files_list['dark_output']) != 0:
        logging.info('Created DARKS subdirectory')
        dark_subfolder = output_final_dir / pathlib.Path('DARKS') 
        dark_subfolder.mkdir(parents=True, exist_ok=True)
        
    if len(output_files_list['flat_output']) != 0:
        logging.info('Created FLATS subdirectory')
        flat_subfolder = output_final_dir / pathlib.Path('FLATS') 
        flat_subfolder.mkdir(parents=True, exist_ok=True)
        
    if len(output_files_list['bias_output']) != 0:
        logging.info('Created BIAS subdirectory')
        bias_subfolder = output_final_dir / pathlib.Path('BIAS') 
        bias_subfolder.mkdir(parents=True, exist_ok=True)
    
    
    for index in range(len(output_files_list['light_input'])):
        if canceled: return None
        current_file += 1
        window.progress_bar.setValue(current_file)
        input = output_files_list['light_input'][index]
        output = output_files_list['light_output'][index]
        
        logging.info('COPY: ' + str(input) + '  -->  ' + str(output))
        shutil.copy(input, output)
        
    for index in range(len(output_files_list['dark_input'])):
        if canceled: return None
        current_file += 1
        window.progress_bar.setValue(current_file)
        input = output_files_list['dark_input'][index]
        output = output_files_list['dark_output'][index]
        
        logging.info('COPY: ' + str(input) + '  -->  ' + str(output))
        shutil.copy(input, output)
        
    for index in range(len(output_files_list['flat_input'])):
        if canceled: return None
        current_file += 1
        window.progress_bar.setValue(current_file)
        input = output_files_list['flat_input'][index]
        output = output_files_list['flat_output'][index]
        
        logging.info('COPY: ' + str(input) + '  -->  ' + str(output))
        shutil.copy(input, output)
        
    for index in range(len(output_files_list['bias_input'])):
        if canceled: return None
        current_file += 1
        window.progress_bar.setValue(current_file)
        input = output_files_list['bias_input'][index]
        output = output_files_list['bias_output'][index]
        
        logging.info('COPY: ' + str(input) + '  -->  ' + str(output))
        shutil.copy(input, output)
    
@Slot()      
def startProcess(self):
    preparePaths()
    window.thread_manager.start(copyProcess)
    logging.info("Starting rename and copy process.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(1200, 600)
    populateTreeWidget()
    
    # Status bar
    window.button_add_lights.clicked.connect(lambda: openFiles('lights'))
    window.button_add_darks.clicked.connect(lambda: openFiles('darks'))
    window.button_add_flats.clicked.connect(lambda: openFiles('flats'))
    window.button_add_bias.clicked.connect(lambda: openFiles('bias'))
    window.button_prepare.clicked.connect(preparePaths)
    
    # Main Tab
    window.search_box.button_simbad_query.clicked.connect(querySimbad)
    window.search_box.line_simbad_query.returnPressed.connect(querySimbad)
    window.search_box.combo_box_query_simbad.currentIndexChanged.connect(updateSimbadCoordinates)
    window.search_box.button_sbdb_query.clicked.connect(querySBDB)
    window.search_box.line_sbdb_query.returnPressed.connect(querySBDB)
    
    # Files Tab
    window.button_refresh.clicked.connect(populateTreeWidget)
    window.button_remove_all.clicked.connect(clearFileLists)
    window.button_remove_selected.clicked.connect(removeItems)
    window.button_add_lights.dropSignal.connect(populateTreeWidget)
    window.button_add_darks.dropSignal.connect(populateTreeWidget)
    window.button_add_flats.dropSignal.connect(populateTreeWidget)
    window.button_add_bias.dropSignal.connect(populateTreeWidget)
    window.treeWidget.currentItemChanged.connect(updateFilePathLabels)
    
    # Process Tab
    window.button_output_path.clicked.connect(setBaseDirectory)
    window.button_start.clicked.connect(startProcess)
    window.button_cancel.clicked.connect(setCancel)

    window.show()
    app.exec()