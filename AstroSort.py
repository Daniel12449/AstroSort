import sys
import pathlib
import shutil
import datetime
import logging

from astroquery.simbad import Simbad
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from UserInterface import MainWindow
from global_vars import *

output_path = None
object_name = None
category = "DeepSky"
camera = None
focal_length = None
location = None
canceled = False
        
# -- Start of functions ---
def querySimbad():
    mainWindow.combo_box_query.clear()
    queryString = mainWindow.line_simbad_query.text()
    
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
                mainWindow.combo_box_query.addItem(name, coordinates)
        except: 
            QtWidgets.QMessageBox.about(None, "Simbad Search", "Simbad was unable to find an object")
            logging.warning("Simbad was unable to find a matching object.")
                    
def updateCoordinates():
    global object_name
    mainWindow.label_ra_coordinates.setText(mainWindow.combo_box_query.currentData()[0])
    mainWindow.label_dec_coordinates.setText(mainWindow.combo_box_query.currentData()[1])
    object_name = mainWindow.combo_box_query.currentData()[2].replace(" ", "")
    logging.info("Object set to " + object_name + " with coordinates: RA " + mainWindow.combo_box_query.currentData()[0] + " and DEC " + mainWindow.combo_box_query.currentData()[1])
    
def updateObjectName(source):
    global object_name
    
    if source == 1:
        object_name = mainWindow.line_object_name1.text()
    elif source == 2:
        object_name = mainWindow.line_object_name2.text()
    elif source == 3:
        object_name = mainWindow.line_object_name3.text()
    elif source == 5:
        object_name = mainWindow.line_object_name4.text()
        
    logging.info("Object name set to: " + str(object_name))
    
def updateCategory(source):
    global category
    
    if source == 0:
        category = "DeepSky"
    elif source == 1:
        category = "SolarSystem"
    elif source == 2:
        category = "Comets"
    elif source == 3:
        category = "Constellations"
    elif source == 4:
        category = mainWindow.line_category.text()
        
    logging.info("Object category set to: " + str(category))
    
def openFiles(target):
    file_list = QtWidgets.QFileDialog.getOpenFileNames()[0]
    path_list = [pathlib.Path(p) for p in file_list]
    
    if target == 'lights':
        for path in path_list:
            light_files.append(path)
            mainWindow.list_lights.addItem(path.name)
            logging.info("Light file added: " + str(path))
    elif target == 'darks':
        for path in path_list:
            dark_files.append(path)
            mainWindow.list_darks.addItem(path.name)
            logging.info("Dark file added: " + str(path))
    elif target == 'flats':
        for path in path_list:
            flat_files.append(path)
            mainWindow.list_flats.addItem(path.name)
            logging.info("Flat file added: " + str(path))
    elif target == 'bias':
        for path in path_list:
            bias_files.append(path)
            mainWindow.list_bias.addItem(path.name)
            logging.info("Bias file added: " + str(path))
    updateStatusBar()
            
def removeFiles(target):
    if target == 'lights':
        row = mainWindow.list_lights.currentRow()
        logging.info("Removing light file: " + str(light_files[row]))
        light_files.pop(row)
        mainWindow.list_lights.takeItem(row)
        
    elif target == 'darks':
        row = mainWindow.list_darks.currentRow()
        logging.info("Removing dark file: " + str(dark_files[row]))
        dark_files.pop(row)
        mainWindow.list_darks.takeItem(row)
        
    elif target == 'flats':
        row = mainWindow.list_flats.currentRow()
        logging.info("Removing flat file: " + str(flat_files[row]))
        flat_files.pop(row)
        mainWindow.list_flats.takeItem(row)
        
    elif target == 'bias':
        row = mainWindow.list_lights.currentRow()
        logging.info("Removing bias file: " + str(bias_files[row]))
        light_files.pop(row)
        mainWindow.list_lights.takeItem(row)
    updateStatusBar()
        
def updateOutputPath():
    global output_path
    outputPath = QtWidgets.QFileDialog.getExistingDirectory()
    mainWindow.line_output_path.setText(outputPath)
    output_path = pathlib.Path(outputPath)
    logging.info("Output path set to: " + str(output_path))
    
def updateCamera():
    global camera
    camera = mainWindow.line_camera.text()
    logging.info("Camera set to: " + camera)
    
def updateFocalLength():
    global focal_length
    focal_length = mainWindow.line_focal_length.text()
    logging.info("Focal length set to: " + focal_length)
    
def updateLocation():
    global location
    location = mainWindow.line_location.text()
    logging.info("Location set to: " + location)
    
def updateStatusBar():
    mainWindow.statusBar_line_filecount.setText("Lights: " + str(len(light_files)) + " · Darks: " + str(len(dark_files)) + " · Flats: " + str(len(flat_files)) + " · Bias: " + str(len(bias_files)))
    
def updateDate():
    if light_files != []:
        first_file = light_files[0]
        date = datetime.datetime.fromtimestamp(first_file.stat().st_mtime, tz=datetime.timezone.utc)
        mainWindow.date.setDate(date)
        logging.info("Date set to: " + str(date))
        
def setCancel():
    global canceled
    if canceled == False:
        canceled = True
        logging.warning("Process canceled!")
    elif canceled == True:
        canceled = False
        logging.info("Process reset.")
    
@Slot()
def copy_and_rename():
    global object_name, output_path, camera, focal_length, canceled, category, location
    
    if object_name == None or output_path == None:
        QtWidgets.QMessageBox.about(None, "Error", "Please select an object and output path first.")
        logging.error("Object and/or output path not set!")
    
    if camera == None:
        QtWidgets.QMessageBox.about(None, "Error", "Please enter a camera first.")
        logging.error("Camera name not set!")
        
    if focal_length == None:
        QtWidgets.QMessageBox.about(None, "Error", "Please enter the focal length first.")
        logging.error("Focal length not set!")
        
    if location == None:
        QtWidgets.QMessageBox.about(None, "Error", "Please enter a location first.")
        logging.error("Location not set!")
        
    else:
        date = str(mainWindow.date.date().day()) + "-" + str(mainWindow.date.date().month()) + "-" + str(mainWindow.date.date().year())
        output_path_final = output_path / pathlib.Path(category) / pathlib.Path(object_name) / pathlib.Path(date + "_" + location) / pathlib.Path(camera + "_" + focal_length)
        logging.info("Base output path set to: " + str(output_path_final))
        
        # Progress Bar
        total_files = len(light_files) + len(dark_files) + len(flat_files) + len(bias_files)
        mainWindow.progress_bar.setMinimum(0)
        mainWindow.progress_bar.setMaximum(total_files)
        current_file = 0
        
        for file in light_files:
            if canceled: return None
            current_file += 1
            mainWindow.progress_bar.setValue(current_file)
            source = file
            destination_path = output_path_final / pathlib.Path('LIGHTS') 
            destination_path.mkdir(parents=True, exist_ok=True)
            filename = "L_" + camera + "_" + focal_length + "_" + file.name
            destination = destination_path / pathlib.Path(filename)
            
            logging.info("Copy started: " + str(source) + " ----> " + str(destination))
            shutil.copy(source, destination)
            
        for file in dark_files:
            if canceled: return None
            current_file += 1
            mainWindow.progress_bar.setValue(current_file)
            source = file
            destination_path = output_path_final / pathlib.Path('DARKS') 
            destination_path.mkdir(parents=True, exist_ok=True)
            filename = "D_" + camera + "_" + focal_length + "_" + file.name
            destination = destination_path / pathlib.Path(filename)
            
            logging.info("Copy started: " + str(source) + " ----> " + str(destination))
            shutil.copy(source, destination)
            
        for file in flat_files:
            if canceled: return None
            current_file += 1
            mainWindow.progress_bar.setValue(current_file)
            source = file
            destination_path = output_path_final / pathlib.Path('FLATS') 
            destination_path.mkdir(parents=True, exist_ok=True)
            filename = "F_" + camera + "_" + focal_length + "_" + file.name
            destination = destination_path / pathlib.Path(filename)
            
            logging.info("Copy started: " + str(source) + " ----> " + str(destination))
            shutil.copy(source, destination)

        for file in bias_files:
            if canceled: return None
            current_file += 1
            mainWindow.progress_bar.setValue(current_file)
            source = file
            destination_path = output_path_final / pathlib.Path('BIAS') 
            destination_path.mkdir(parents=True, exist_ok=True)
            filename = "B_" + camera + "_" + focal_length + "_" + file.name
            destination = destination_path / pathlib.Path(filename)
            
            logging.info("Copy started: " + str(source) + " ----> " + str(destination))
            shutil.copy(source, destination)

@Slot()      
def startProcess(self):
    mainWindow.thread_manager.start(copy_and_rename)
    logging.info("Starting rename and copy process.")

if __name__ == "__main__":    
    app = QtWidgets.QApplication([])
    mainWindow = MainWindow()
    mainWindow.resize(1200, 600)
    
    logging.basicConfig(level=logging.INFO)
    
    mainWindow.combo_box_category.currentIndexChanged.connect(mainWindow.displayStack)
    mainWindow.line_object_name1.editingFinished.connect(lambda: updateObjectName(1))
    mainWindow.line_object_name2.editingFinished.connect(lambda: updateObjectName(2))
    mainWindow.line_object_name3.editingFinished.connect(lambda: updateObjectName(3))
    mainWindow.line_object_name4.editingFinished.connect(lambda: updateObjectName(4))
    mainWindow.line_category.editingFinished.connect(lambda: updateCategory(5))
    
    mainWindow.button_query.clicked.connect(querySimbad)
    mainWindow.line_simbad_query.returnPressed.connect(querySimbad)
    mainWindow.combo_box_query.currentIndexChanged.connect(updateCoordinates)
    mainWindow.line_camera.editingFinished.connect(updateCamera)
    mainWindow.line_focal_length.editingFinished.connect(updateFocalLength)
    mainWindow.line_location.editingFinished.connect(updateLocation)
    
    mainWindow.button_add_lights.clicked.connect(lambda: openFiles('lights'))
    mainWindow.button_add_darks.clicked.connect(lambda: openFiles('darks'))
    mainWindow.button_add_flats.clicked.connect(lambda: openFiles('flats'))
    mainWindow.button_add_bias.clicked.connect(lambda: openFiles('bias'))
    
    mainWindow.button_del_lights.clicked.connect(lambda: removeFiles('lights'))
    mainWindow.button_del_darks.clicked.connect(lambda: removeFiles('darks'))
    mainWindow.button_del_flats.clicked.connect(lambda: removeFiles('flats'))
    mainWindow.button_del_bias.clicked.connect(lambda: removeFiles('bias'))
    
    mainWindow.button_output_path.clicked.connect(updateOutputPath)
    mainWindow.list_lights.model().rowsInserted.connect(updateDate)
    mainWindow.button_cancel.clicked.connect(setCancel)
    mainWindow.button_start.clicked.connect(startProcess)
    
    mainWindow.show()
    sys.exit(app.exec())

        