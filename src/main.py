from datetime import datetime
from PySide6 import QtWidgets
from PySide6.QtCore import QThreadPool, Slot, QStandardPaths
from astroquery.simbad import Simbad
from astroquery.jplsbdb import SBDB
from dateutil.parser import parse
from CustomWidgets import DropButton
from ui_classes import *
from config import *

import sys, pathlib, logging, shutil, exiftool, pandas
import vars


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
        
        self.tabWidget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabWidget)
        
        self.tab1 = main_tab()
        self.tab2 = files_tab()
        #self.tab3 = structure_tab()
        self.tab4 = metadata_tab()

        self.tabWidget.addTab(self.tab1, "Main")
        self.tabWidget.addTab(self.tab2, "Files")
        #self.tabWidget.addTab(self.tab3, "Folder Structure")
        self.tabWidget.addTab(self.tab4, "Image Metadata")
        
        ## Setup of Statusbar
        self.button_add_lights = DropButton("+ Lights", objectName='button_add_lights')
        self.button_add_darks = DropButton("+ Darks ", objectName='button_add_darks')
        self.button_add_flats = DropButton("+ Flats ", objectName='button_add_flats')
        self.button_add_bias = DropButton("+ Bias  ", objectName='button_add_bias')
        self.button_reset = QtWidgets.QPushButton("Reset")
        self.button_prepare = QtWidgets.QPushButton("Prepare")
        self.statusBar().addWidget(self.button_add_lights)
        self.statusBar().addWidget(self.button_add_darks)
        self.statusBar().addWidget(self.button_add_flats)
        self.statusBar().addWidget(self.button_add_bias)
        self.statusBar().addPermanentWidget(self.button_prepare)
        self.statusBar().addPermanentWidget(self.button_reset)

## -- Start of functions --

def resetBox():
    result  = QtWidgets.QMessageBox.question(None, 'Reset', "Do you really want to reset all files and settings?",
            QtWidgets.QMessageBox.Reset | QtWidgets.QMessageBox.Cancel)
            
    if result == QtWidgets.QMessageBox.Reset:
        resetAll()

def openFiles(target):
    file_list = QtWidgets.QFileDialog.getOpenFileNames()[0]
    
    path_list = [pathlib.Path(p) for p in file_list]
    name_list = [p.name for p in path_list]
    
    
    files = pandas.DataFrame({
        'name': name_list,
        'input_path': path_list
    })
    
    if target == 'lights':    
        vars.df_lights = pandas.concat([vars.df_lights, files], ignore_index=True)
        logging.info('''Light files added: \n''' + str(vars.df_lights))
    elif target == 'darks':
        vars.df_darks = pandas.concat([vars.df_darks, files], ignore_index=True)
        logging.info('''Dark files added: \n''' + str(vars.df_darks))
    elif target == 'flats':
        vars.df_flats = pandas.concat([vars.df_flats, files], ignore_index=True)
        logging.info('''Flat files added: \n''' + str(vars.df_flats))
    elif target == 'bias':
        vars.df_bias = pandas.concat([vars.df_bias, files], ignore_index=True)
        logging.info('''Bias files added: \n''' + str(vars.df_bias))
    
    populateTreeWidget()
            
def populateTreeWidget():
    window.tab2.treeWidget.clear()

    if len(vars.df_lights.index) != 0:
        columns = vars.df_lights.columns.values.tolist()
    elif len(vars.df_darks.index) != 0:
        columns = vars.df_darks.columns.values.tolist()
    elif len(vars.df_flats.index) != 0:
        columns = vars.df_flats.columns.values.tolist()
    elif len(vars.df_bias.index) != 0:
        columns = vars.df_bias.columns.values.tolist()
    else:
        columns = []

    window.tab2.treeWidget.setColumnCount(len(columns))
    window.tab2.treeWidget.setHeaderLabels(columns)
        
    if window.tab2.checkbox_paths.checkState() == Qt.CheckState.Unchecked: 
        state = True
    else: 
        state = False
        
    if 'input_path' in columns:
       window.tab2.treeWidget.setColumnHidden(columns.index('input_path'), state)
    if 'new_file_structure' in columns:
        window.tab2.treeWidget.setColumnHidden(columns.index('new_file_structure'), state)
        
    for i, df in enumerate([vars.df_lights, vars.df_darks, vars.df_flats, vars.df_bias]):
        if i == 0: parent_item = QtWidgets.QTreeWidgetItem(["Light files"])
        if i == 1: parent_item = QtWidgets.QTreeWidgetItem(["Dark files"])
        if i == 2: parent_item = QtWidgets.QTreeWidgetItem(["Flat files"])
        if i == 3: parent_item = QtWidgets.QTreeWidgetItem(["Bias files"])

        for index, row in df.iterrows():
            child = QtWidgets.QTreeWidgetItem(row["name"])
            for index, value in enumerate(columns):
                child.setText(index, str(row[value]))
            parent_item.addChild(child)
        window.tab2.treeWidget.insertTopLevelItem(0, parent_item)

    for column in range(len(columns)):
        window.tab2.treeWidget.resizeColumnToContents(column)   
    window.tab2.treeWidget.resizeColumnToContents(0)   

    window.tab2.treeWidget.expandAll()

    # Send counts to mainpage
    window.tab1.label_count_lights.setText(str(len(vars.df_lights)))
    window.tab1.label_count_darks.setText(str(len(vars.df_darks)))
    window.tab1.label_count_flats.setText(str(len(vars.df_flats)))
    window.tab1.label_count_bias.setText(str(len(vars.df_bias))) 
    
def removeItems():
    items = window.tab2.treeWidget.selectedItems()
    
    for item in items:
        parent = item.parent().text(0)
        name = item.text(0)
        logging.info('Removing ' + name + ' from ' + parent)
        
        if parent == "Light files": 
            vars.df_lights.drop(vars.df_lights[vars.df_lights['name'] == name].index, inplace=True)
        if parent == "Dark files": 
            vars.df_darks.drop(vars.df_darks[vars.df_darks['name'] == name].index, inplace=True)
        if parent == "Flat files": 
            vars.df_flats.drop(vars.df_flats[vars.df_flats['name'] == name].index, inplace=True)
        if parent == "Bias files": 
            vars.df_bias.drop(vars.df_bias[vars.df_bias['name'] == name].index, inplace=True)
        
    populateTreeWidget()

def clearFileLists():
    vars.df_lights = vars.df_lights.iloc[0:0]
    vars.df_darks  = vars.df_darks.iloc[0:0]
    vars.df_flats  = vars.df_flats.iloc[0:0]
    vars.df_bias   = vars.df_bias.iloc[0:0]
    populateTreeWidget()
    
def querySimbad():
    window.tab1.search_box.combo_box_query_simbad.clear()
    queryString = window.tab1.search_box.line_simbad_query.text()
    simbad = Simbad()
    
    if queryString != "":
        
        def sort_catalogue(name):
            if name.startswith("M "):
                return (0, name) 
            elif name.startswith("IC "):
                return (1, name)
            elif name.startswith("NGC "):
                return (2, name)
            else:
                return (3, name) 
        
        try:
            simbad_result = simbad.query_objectids(queryString)
            names = []
            
            for index, entry in enumerate(reversed(simbad_result)):
                name = entry["id"]
                if "NAME" in name: name = name.strip("NAME").replace(" ", "")
                names.append(name)
                
            window.tab1.search_box.combo_box_query_simbad.addItems(sorted(names, key=sort_catalogue))
        except: 
            QtWidgets.QMessageBox.about(None, "Simbad Search", "Simbad was unable to find an object")
            logging.warning("Simbad was unable to find a matching object.") 

def querySBDB():
    queryString = window.tab1.search_box.line_sbdb_query.text()

    if queryString != "":
        sbdb = SBDB.query(queryString)
        
        if 'message' in sbdb.keys():
            QtWidgets.QMessageBox.about(None, "SBDB Search", "SBDB was unable to find an object")        
        
        elif 'object' in sbdb.keys():
            window.tab1.search_box.label_full_name.setText(sbdb['object']['fullname'])
            window.tab1.search_box.label_type.setText(sbdb['object']['orbit_class']['name'])
            
            if 'shortname' in sbdb['object'].keys():
                window.tab1.search_box.label_short_name.setText(sbdb['object']['shortname'])
            else:
                window.tab1.search_box.label_short_name.setText('-/-')

def gatherProcessParameters():
    current_category = window.tab1.search_box.currentIndex()
    location = window.tab4.line_location.text()
    
    if window.tab4.exif_camera.isEnabled():
        date = str(window.tab4.exif_date.date().year()) + "-" + str(window.tab4.exif_date.date().month()) + "-" + str(window.tab4.exif_date.date().day())
        camera = str(window.tab4.exif_camera.text())
        focal_length = str(window.tab4.exif_focal_length.text())
    elif window.tab4.fits_camera.isEnabled():
        date = str(window.tab4.fits_date.date().year()) + "-" + str(window.tab4.fits_date.date().month()) + "-" + str(window.tab4.fits_date.date().day())
        camera = str(window.tab4.fits_camera.text())
        focal_length = str(window.tab4.fits_focal_length.text())
    
    if location == "" or camera == "" or focal_length == "":
        QtWidgets.QMessageBox.about(None, "General Parameters", "Please fill location, camera and focal length fields.")
        raise ValueError('Please fill location, camera and focal length fields.')
    
    if current_category == 0:
        object_category = "DeepSky"
        object_name = window.tab1.search_box.combo_box_query_simbad.currentText()
        if not object_name:
            QtWidgets.QMessageBox.about(None, "Deep Sky Object", "Please select an object.")
            raise ValueError
    
    elif current_category == 1:
        object_name_temp = window.tab1.search_box.combo_box_planets.currentText()
        custom_object_name_tmep = window.tab1.search_box.line_largeBodies_custom.text()
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
        object_name_long = window.tab1.search_box.label_full_name.text()
        object_name_short = window.tab1.search_box.label_short_name.text()
        
        if object_name_long == "":
            QtWidgets.QMessageBox.about(None, "Small Solar System Bodies", "Please select an object.")
            raise ValueError
        
        if object_name_short != '-/-':
            object_name = object_name_short.replace(" ", "-").replace("/", "")
        else: 
            object_name = object_name_long.replace(" ", "-").replace("/", "")
    
    elif current_category == 3:
        object_category = "Constellations"
        object_name_tmp = window.tab1.search_box.line_constellation.text()
        
        if object_name_tmp != "":
            object_name = object_name_tmp
        else: 
            QtWidgets.QMessageBox.about(None, "Constellations", "Please enter constellation or select different category.")
            raise ValueError
    
    elif current_category == 4:
        object_category_temp = window.tab1.search_box.line_custom_category.text()
        object_name_tmp = window.tab1.search_box.line_custom_name.text()
        
        if object_name_tmp != "" and object_category_temp != "":
            object_name = object_name_tmp
            object_category = object_category_temp
        else:
            QtWidgets.QMessageBox.about(None, "Custom Category", "Please enter a custom name and category.")
            raise ValueError
    
    output_path_tmp = window.tab1.line_output_path.text()
    
    if output_path_tmp != "":
        output_path = pathlib.Path(output_path_tmp)
    else:
        QtWidgets.QMessageBox.about(None, "Processing", "Please enter an output path.")
        raise ValueError
    
    vars.output_dir_local = output_path / pathlib.Path(object_category) / pathlib.Path(object_name) / pathlib.Path(date + "_" + location) / pathlib.Path(camera + "_" + focal_length)
    
def setBaseDirectory():
    outputPath = QtWidgets.QFileDialog.getExistingDirectory()
    window.tab1.line_output_path.setText(outputPath)
    logging.info("Output path set to: " + str(outputPath))
    
def setCancel():
    if vars.canceled == False:
        vars.canceled = True
        logging.warning("Process vars.canceled!")
    elif vars.canceled == True:
        vars.canceled = False
        logging.info("Process reset.") 
        
def prepareLocalPaths():
    try:
        gatherProcessParameters()
        if window.tab4.exif_camera.isEnabled():
            exposure = str(window.tab4.exif_exposure.text())
            iso = str(window.tab4.exif_iso.text())
        elif window.tab4.fits_camera.isEnabled():
            exposure = str(window.tab4.fits_exposure.text())
            iso = str(window.tab4.fits_gain.text())  
        
        if window.tab4.line_exposure_dark.text() != "":
            exposure_dark = str(window.tab4.line_exposure_dark.text())
        if window.tab4.line_iso_dark.text() != "":
            iso_dark = str(window.tab4.line_iso_dark.text())
          
        if window.tab4.line_exposure_flat.text() != "":
            exposure_flat = str(window.tab4.line_exposure_flat.text())
        if window.tab4.line_iso_flat.text() != "":
            iso_flat = str(window.tab4.line_iso_flat.text())
    
        if window.tab4.line_exposure_bias.text() != "":
            exposure_bias = str(window.tab4.line_exposure_bias.text())
        if window.tab4.line_iso_bias.text() != "":
            iso_bias = str(window.tab4.line_iso_bias.text())

    except:
        QtWidgets.QMessageBox.about(None, "Starting Process", "Please correct any errors and try again. Make sure all metadata fields are filled.")
        return    
          
    for index, row in vars.df_lights.iterrows():
        if window.tab1.checkbox_filename.isChecked():
            extension = row['input_path'].suffix
            filename = "L_" + exposure + "_" + iso + "_img" + str(index) + extension
        else:
            filename = "L_" + exposure + "_" + iso + "_" + row['name']            

        vars.df_lights.loc[index, 'new_file_structure'] = pathlib.Path('LIGHTS') / pathlib.Path(filename)
        
    for index, row in vars.df_darks.iterrows():
        if window.tab1.checkbox_filename.isChecked():
            extension = row['input_path'].suffix
            filename = "D_" + exposure_dark + "_" + iso_dark  + "_img" + str(index) + extension
        else:
            filename = "D_" + exposure_dark + "_" + iso_dark + "_" + row['name']
        vars.df_darks.loc[index, 'new_file_structure'] = pathlib.Path('DARKS') / pathlib.Path(filename)
        
    for index, row in vars.df_flats.iterrows():
        if window.tab1.checkbox_filename.isChecked():
            extension = row['input_path'].suffix
            filename = "F_" + exposure_flat + "_" + iso_flat  + "_img" + str(index) + extension
        else:
            filename = "F_" + exposure_flat + "_" + iso_flat + "_" + row['name'] 
        vars.df_flats.loc[index, 'new_file_structure'] = pathlib.Path('FLATS') / pathlib.Path(filename)
        
    for index, row in vars.df_bias.iterrows():
        if window.tab1.checkbox_filename.isChecked():
            extension = row['input_path'].suffix
            filename = "B_" + exposure_bias + "_" + iso_bias  + "_img" + str(index) + extension
        else:
            filename = "B_" + exposure_bias + "_" + iso_bias + "_" + row['name'] 
        vars.df_bias.loc[index, 'new_file_structure'] = pathlib.Path('BIAS') / pathlib.Path(filename)
        
    print(vars.df_lights)
        
def resetAll():
    clearFileLists()
    
    window.tab1.search_box.line_constellation.clear()
    window.tab1.search_box.line_custom_category.clear()
    window.tab1.search_box.line_custom_name.clear()
    window.tab1.search_box.line_largeBodies_custom.clear()
    window.tab1.search_box.line_sbdb_query.clear()
    window.tab1.search_box.line_simbad_query.clear()
    window.tab1.search_box.combo_box_query_simbad.clear()
    window.tab1.search_box.label_full_name.clear()
    window.tab1.search_box.label_short_name.clear()
    window.tab1.search_box.label_type.clear()
    window.tab1.line_output_path.clear()
    
    list_exif = [window.tab4.exif_camera, window.tab4.exif_exposure, window.tab4.exif_date, window.tab4.exif_iso, window.tab4.exif_focal_length,
                 window.tab4.fits_camera, window.tab4.fits_exposure, window.tab4.fits_date, window.tab4.fits_gain, window.tab4.fits_focal_length,
                 window.tab4.fits_telescope, window.tab4.fits_object, window.tab4.fits_temperature, window.tab4.line_exposure_dark, 
                 window.tab4.line_exposure_flat, window.tab4.line_exposure_bias, window.tab4.line_iso_dark, window.tab4.line_iso_flat,
                 window.tab4.line_iso_bias, window.tab4.line_location]
    
    for line in list_exif:
            line.clear()
            
    populateTreeWidget()
    
def readExif():
    readExifLights()
    readExifDarks()
    readExifFlats()
    readExifBias()    
    
def readExifLights():
    ## Lights exif / fits
    try:
        files = vars.df_lights['input_path'].iloc[0]
    except:
        logging.info("No light file found") 
        return
    
    # reset line edits
    list_exif = [window.tab4.exif_camera, window.tab4.exif_exposure, window.tab4.exif_date, window.tab4.exif_iso, window.tab4.exif_focal_length]
    list_fits = [window.tab4.fits_camera, window.tab4.fits_exposure, window.tab4.fits_date, window.tab4.fits_gain, window.tab4.fits_focal_length,
                 window.tab4.fits_telescope, window.tab4.fits_object, window.tab4.fits_temperature]
    
    eth = exiftool.ExifToolHelper()
    metadata = eth.get_metadata(files, params=["-d", "%Y-%m-%d %H:%M:%S"])[0]

    if "EXIF:ExposureTime" in metadata.keys():
        for line in list_fits:
            line.clear()
            line.setEnabled(False)
            
        for line in list_exif:
            line.clear()
            line.setEnabled(True)
        
        window.tab4.exif_camera.setText(str(metadata["EXIF:Model"]))
        window.tab4.exif_exposure.setText(str(metadata["EXIF:ExposureTime"]) + "s")
        window.tab4.exif_iso.setText(str(metadata["EXIF:ISO"]))
        window.tab4.exif_focal_length.setText(str(metadata["EXIF:FocalLength"]) + "mm")
     
        date = datetime.strptime(str(metadata["EXIF:DateTimeOriginal"]), "%Y:%m:%d %H:%M:%S")
        window.tab4.exif_date.setDate(date.date())
         
    if "FITS:Exposure" in metadata.keys():
        for line in list_fits:
            line.clear()
            line.setEnabled(True)
            
        for line in list_exif:
            line.clear()
            line.setEnabled(False)
        
        window.tab4.fits_camera.setText(str(metadata["FITS:Instrument"]))
        window.tab4.fits_exposure.setText(str(metadata["FITS:Exposure"]) + "s")
        window.tab4.fits_gain.setText(str(metadata["FITS:Gain"]))
        window.tab4.fits_focal_length.setText(str(round(metadata["FITS:Focallen"])) + "mm")
        window.tab4.fits_telescope.setText(str(metadata["FITS:Telescope"]))
        window.tab4.fits_object.setText(str(metadata["FITS:Object"]))
        window.tab4.fits_temperature.setText(str(round(metadata["FITS:Set-temp" ])))
        
        date = parse(str(metadata["FITS:ObservationDate"]))
        window.tab4.fits_date.setDate(date.date())
        
def readExifDarks():
        ## Dark exif / fits
        try:
            files = vars.df_darks['input_path'].iloc[0]
        except:
            logging.info("No dark file found") 
            return

        # reset LineEdits
        window.tab4.line_exposure_dark.clear()
        window.tab4.line_iso_dark.clear()
        
        # read exif
        eth = exiftool.ExifToolHelper()
        metadata = eth.get_metadata(files)[0]
        
        if "EXIF:ExposureTime" in metadata.keys(): window.tab4.line_exposure_dark.setText(str(metadata["EXIF:ExposureTime"]) + "s")
        if "EXIF:ISO" in metadata.keys(): window.tab4.line_iso_dark.setText(str(metadata["EXIF:ISO"]))
        
        if "FITS:Exposure" in metadata.keys(): window.tab4.line_exposure_dark.setText(str(metadata["FITS:Exposure"]) + "s")
        if "FITS:Gain" in metadata.keys(): window.tab4.line_iso_dark.setText(str(metadata["FITS:Gain"]))
        
def readExifFlats():
        ## Flat exif / fits
        try:
            files = vars.df_flats['input_path'].iloc[0]
        except:
            logging.info("No flat file found") 
            return

        # reset LineEdits
        window.tab4.line_exposure_flat.clear()
        window.tab4.line_iso_flat.clear()
        
        # read exif
        eth = exiftool.ExifToolHelper()
        metadata = eth.get_metadata(files)[0]
        
        if "EXIF:ExposureTime" in metadata.keys(): window.tab4.line_exposure_flat.setText(str(metadata["EXIF:ExposureTime"]) + "s")
        if "EXIF:ISO" in metadata.keys(): window.tab4.line_iso_flat.setText(str(metadata["EXIF:ISO"]) )
        
        if "FITS:Exposure" in metadata.keys(): window.tab4.line_exposure_flat.setText(str(metadata["FITS:Exposure"]) + "s")
        if "FITS:Gain" in metadata.keys(): window.tab4.line_iso_flat.setText(str(metadata["FITS:Gain"]))
        
def readExifBias():
        ## Bias exif / fits
        try:
            files = vars.df_bias['input_path'].iloc[0]
        except:
            logging.info("No bias file found") 
            return

        # reset LineEdits
        window.tab4.line_exposure_bias.clear()
        window.tab4.line_iso_bias.clear()
        
        # read exif
        eth = exiftool.ExifToolHelper()
        metadata = eth.get_metadata(files)[0]
        
        if "EXIF:ExposureTime" in metadata.keys(): window.tab4.line_exposure_bias.setText(str(metadata["EXIF:ExposureTime"]) + "s")
        if "EXIF:ISO" in metadata.keys(): window.tab4.line_iso_bias.setText(str(metadata["EXIF:ISO"]))
        
        if "FITS:Exposure" in metadata.keys(): window.tab4.line_exposure_bias.setText(str(metadata["FITS:Exposure"]) + "s")
        if "FITS:Gain" in metadata.keys(): window.tab4.line_iso_bias.setText(str(metadata["FITS:Gain"]))
            
@Slot()      
def copyProcess():
    # Create file paths
    if len(vars.df_lights) != 0:
        logging.info('Created LIGHTS subdirectory')
        light_subfolder = vars.output_dir_local / pathlib.Path('LIGHTS') 
        light_subfolder.mkdir(parents=True, exist_ok=True)
        
    if len(vars.df_darks) != 0:
        logging.info('Created DARKS subdirectory')
        dark_subfolder = vars.output_dir_local / pathlib.Path('DARKS') 
        dark_subfolder.mkdir(parents=True, exist_ok=True)
        
    if len(vars.df_flats) != 0:
        logging.info('Created FLATS subdirectory')
        flat_subfolder = vars.output_dir_local / pathlib.Path('FLATS') 
        flat_subfolder.mkdir(parents=True, exist_ok=True)
        
    if len(vars.df_bias) != 0:
        logging.info('Created BIAS subdirectory')
        bias_subfolder = vars.output_dir_local / pathlib.Path('BIAS') 
        bias_subfolder.mkdir(parents=True, exist_ok=True)
    
    for index, element in vars.df_lights.iterrows():
        if vars.canceled: return None
        vars.current_file += 1
        window.tab1.progress_bar.setValue(vars.current_file)
        input = vars.df_lights.loc[index, 'input_path']
        output = vars.output_dir_local / vars.df_lights.loc[index, 'new_file_structure']
        
        logging.info('COPY: ' + str(input) + '  -->  ' + str(output))
        shutil.copy(input, output)
        
    for index, element in vars.df_darks.iterrows():
        if vars.canceled: return None
        vars.current_file += 1
        window.tab1.progress_bar.setValue(vars.current_file)
        input = vars.df_darks.loc[index, 'input_path']
        output = vars.output_dir_local / vars.df_darks.loc[index, 'new_file_structure']
        
        logging.info('COPY: ' + str(input) + '  -->  ' + str(output))
        shutil.copy(input, output)
        
    for index, element in vars.df_flats.iterrows():
        if vars.canceled: return None
        vars.current_file += 1
        window.tab1.progress_bar.setValue(vars.current_file)
        input = vars.df_flats.loc[index, 'input_path']
        output = vars.output_dir_local / vars.df_flats.loc[index, 'new_file_structure']
        
        logging.info('COPY: ' + str(input) + '  -->  ' + str(output))
        shutil.copy(input, output)
        
    for index, element in vars.df_bias.iterrows():
        if vars.canceled: return None
        vars.current_file += 1
        window.tab1.progress_bar.setValue(vars.current_file)
        input = vars.df_bias.loc[index, 'input_path']
        output = vars.output_dir_local / vars.df_bias.loc[index, 'new_file_structure']
        
        logging.info('COPY: ' + str(input) + '  -->  ' + str(output))
        shutil.copy(input, output)
    
@Slot()      
def startProcess(self):
    
    #Setup of Progress bar
    total_files = len(vars.df_lights) + len(vars.df_darks) + len(vars.df_flats) + len(vars.df_bias)
    modifier = int(window.tab1.checkbox_save_locally.isChecked() == True) # + int(window.tab1.checkbox_save_s3.isChecked() == True)
    window.tab1.progress_bar.setMinimum(0)
    window.tab1.progress_bar.setMaximum(total_files * modifier)
    logging.info('Number of files to process: ' + str(total_files * modifier))
    vars.current_file = 0
    
    if window.tab1.checkbox_save_locally.isChecked():
        prepareLocalPaths()
        window.thread_manager.start(copyProcess)
        logging.info("Starting local rename and copy process.")
    else:
        logging.info("No local storage wanted.")
    
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
    window.button_prepare.clicked.connect(prepareLocalPaths)
    window.button_reset.clicked.connect(resetBox)
    
    # Main Tab
    window.tab1.search_box.button_simbad_query.clicked.connect(querySimbad)
    window.tab1.search_box.line_simbad_query.returnPressed.connect(querySimbad)
    window.tab1.search_box.button_sbdb_query.clicked.connect(querySBDB)
    window.tab1.search_box.line_sbdb_query.returnPressed.connect(querySBDB)
    
    # Files Tab
    window.tab2.button_refresh.clicked.connect(populateTreeWidget)
    window.tab2.button_remove_all.clicked.connect(clearFileLists)
    window.tab2.button_remove_selected.clicked.connect(removeItems)
    window.button_add_lights.dropSignal.connect(populateTreeWidget)
    window.button_add_darks.dropSignal.connect(populateTreeWidget)
    window.button_add_flats.dropSignal.connect(populateTreeWidget)
    window.button_add_bias.dropSignal.connect(populateTreeWidget)
    window.tab2.checkbox_paths.stateChanged.connect(populateTreeWidget)
    
    # Process Tab
    window.tab1.button_output_path.clicked.connect(setBaseDirectory)
    window.tab1.button_start.clicked.connect(startProcess)
    window.tab1.button_cancel.clicked.connect(setCancel)
    
    # Metadata Tab
    window.tab4.button_scan_metadata.clicked.connect(readExif)
    window.tab4.button_profile1.clicked.connect(lambda: handleProfile(window, config_path, 'metadata_profile_1'))
    window.tab4.button_profile2.clicked.connect(lambda: handleProfile(window, config_path, 'metadata_profile_2'))
    window.tab4.button_profile3.clicked.connect(lambda: handleProfile(window, config_path, 'metadata_profile_3'))


    # Handle config file
    # get config file location
    config_path = pathlib.Path(QStandardPaths.writableLocation(QStandardPaths.ConfigLocation)) / "astrosort.ini"
    
    if config_path.exists():
        logging.info("Config file found: " + str(config_path))
        handleConfig(window, config_path)
    else:
        logging.info("No config file found, you can add one at: " + str(config_path))
        
    window.show()
    app.exec()