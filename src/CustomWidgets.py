from PySide6 import QtWidgets
from PySide6.QtCore import Signal
import vars
import pathlib, logging, pandas
            
class DropButton(QtWidgets.QPushButton):    
    dropSignal = Signal(int) 
    
    def __init__(self, parent=None, *args, **kwargs):
        super(DropButton, self).__init__(parent, *args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):     
        self.dropSignal.emit(1)
        md = event.mimeData()
        if md.hasUrls():
            file_list = md.urls()            
            path_list = [pathlib.Path(p.toLocalFile()) for p in file_list]
            name_list = [p.name for p in path_list]
            
            files = pandas.DataFrame({
                'name': name_list,
                'input_path': path_list
            })

            if self.objectName() == 'button_add_lights':
                vars.df_lights = pandas.concat([vars.df_lights, files], ignore_index=True)
                logging.info('''Light files added: \n''' + str(vars.df_lights))
                    
            if self.objectName() == 'button_add_darks':
                vars.df_darks = pandas.concat([vars.df_darks, files], ignore_index=True)
                logging.info('''Dark files added: \n''' + str(vars.df_darks))
                    
            if self.objectName() == 'button_add_flats':
                vars.df_flats = pandas.concat([vars.df_flats, files], ignore_index=True)
                logging.info('''Flat files added: \n''' + str(vars.df_flats))
                    
            if self.objectName() == 'button_add_bias':
                vars.df_bias = pandas.concat([vars.df_bias, files], ignore_index=True)
                logging.info('''Bias files added: \n''' + str(vars.df_bias))
            event.acceptProposedAction()

class searchWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super(searchWidget, self).__init__(parent, *args, **kwargs)
        
        def add_horizontal_widgets(layout, widget1, widget2):
            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(widget1)
            hbox.addWidget(widget2)
            layout.addLayout(hbox)
        
        searchTab0 = QtWidgets.QWidget()
        searchTab1 = QtWidgets.QWidget()
        searchTab2 = QtWidgets.QWidget()
        searchTab3 = QtWidgets.QWidget()
        searchTab4 = QtWidgets.QWidget()
        
        self.addTab(searchTab0, "Deep Sky")
        self.addTab(searchTab1, "Large Solar System Bodies")
        self.addTab(searchTab2, "Small Solar System Bodies")
        self.addTab(searchTab3, "Constellations")
        self.addTab(searchTab4, "Custom")
        
        ## searchTab0: Simbad search
        # Object definitions
        self.button_simbad_query = QtWidgets.QPushButton("Search")
        self.line_simbad_query = QtWidgets.QLineEdit(placeholderText="Enter Object")
        self.combo_box_query_simbad = QtWidgets.QComboBox()
        self.combo_box_query_simbad.setStyleSheet("combobox-popup: 0;")
        
        # Layout definition
        vbox_astromeric_solution = QtWidgets.QVBoxLayout()
        vbox_astromeric_solution.addWidget(QtWidgets.QLabel("Search for object"))
        add_horizontal_widgets(vbox_astromeric_solution, self.line_simbad_query, self.button_simbad_query)
        vbox_astromeric_solution.addWidget(self.combo_box_query_simbad)
        
        hbox_coordinates = QtWidgets.QHBoxLayout()
        vbox_astromeric_solution.addLayout(hbox_coordinates)
        searchTab0.setLayout(vbox_astromeric_solution)
        
        ## searchTab1: Large Solar System Bodies
        # Object definition
        self.combo_box_planets = QtWidgets.QComboBox()
        self.combo_box_planets.addItems(['Sun', 'Mercury', 'Venus', 'Earth', 'Moon', 'Mars', 'Jupyter', 'Saturn', 'Uranus', 'Neptune', 'Custom'])
        self.line_largeBodies_custom = QtWidgets.QLineEdit(placeholderText="Enter object")
        #Layout definition
        vbox_largeBodies = QtWidgets.QVBoxLayout()
        add_horizontal_widgets(vbox_largeBodies, QtWidgets.QLabel('Select object'), self.combo_box_planets)
        add_horizontal_widgets(vbox_largeBodies, QtWidgets.QLabel('Enter custom object'), self.line_largeBodies_custom)
        searchTab1.setLayout(vbox_largeBodies)
        
        ## searchTab2: sbdb search
        # Object definitions
        self.button_sbdb_query = QtWidgets.QPushButton("Search")
        self.line_sbdb_query = QtWidgets.QLineEdit(placeholderText="Enter Object")
        self.label_full_name = QtWidgets.QLabel()
        self.label_short_name = QtWidgets.QLabel()
        self.label_type = QtWidgets.QLabel()

        # Layout definition
        vbox_sbdb_solution = QtWidgets.QVBoxLayout()
        vbox_sbdb_solution.addWidget(QtWidgets.QLabel("Search for object (eg. Asteroids, Comets, dawarf planets)"))
        add_horizontal_widgets(vbox_sbdb_solution, self.line_sbdb_query, self.button_sbdb_query)
        add_horizontal_widgets(vbox_sbdb_solution, QtWidgets.QLabel("Full Name: "),  self.label_full_name)
        add_horizontal_widgets(vbox_sbdb_solution, QtWidgets.QLabel("Short Name: "), self.label_short_name)
        add_horizontal_widgets(vbox_sbdb_solution, QtWidgets.QLabel("Type: "), self.label_type)
        searchTab2.setLayout(vbox_sbdb_solution)
        
        ## searchTab3: Constellations
        # Object definitions
        constellation_list = ['Andromeda', 'Antlia', 'Apus', 'Aquarius', 'Aquila', 'Ara', 'Aries', 'Auriga', 'Bootes', 'Caelum', 
                              'Camelopardalis', 'Cancer', 'Canes Venatici', 'Canis Major', 'Canis Minor', 'Capricornus', 'Carina', 
                              'Cassiopeia', 'Centaurus', 'Cepheus', 'Cetus ', 'Chamaeleon', 'Circinus', 'Columba', 'Coma Berenices', 
                              'Corona Australis', 'Corona Borealis', 'Corvus', 'Crater', 'Crux', 'Cygnus', 'Delphinus', 'Dorado', 
                              'Draco', 'Equuleus', 'Eridanus', 'Fornax', 'Gemini', 'Grus', 'Hercules', 'Horologium', 'Hydra', 
                              'Hydrus', 'Indus', 'Lacerta', 'Leo', 'Leo Minor', 'Lepus', 'Libra', 'Lupus', 'Lynx', 'Lyra', 'Mensa', 
                              'Microscopium', 'Monoceros', 'Musca', 'Norma', 'Octans', 'Ophiuchus', 'Orion', 'Pavo', 'Pegasus', 'Perseus', 
                              'Phoenix', 'Pictor', 'Pisces', 'Piscis Austrinus', 'Puppis', 'Pyxis', 'Reticulum', 'Sagitta', 'Sagittarius', 
                              'Scorpius', 'Sculptor', 'Scutum', 'Serpens', 'Sextans', 'Taurus', 'Telescopium', 'Triangulum ', 'Triangulum Australe', 
                              'Tucana', 'Ursa Major', 'Ursa Minor', 'Vela', 'Virgo', 'Volans', 'Vulpecula']
        
        completer_constellation = QtWidgets.QCompleter(constellation_list)
        self.line_constellation = QtWidgets.QLineEdit(placeholderText="Enter Constellation")
        self.line_constellation.setCompleter(completer_constellation)
        

        # Layout definitions
        vbox_constellations = QtWidgets.QVBoxLayout()
        add_horizontal_widgets(vbox_constellations, QtWidgets.QLabel("Enter name of constellation: "), self.line_constellation)
        searchTab3.setLayout(vbox_constellations)
        
        ## searchTab3: Custom Field
        # Object definitions
        self.line_custom_category = QtWidgets.QLineEdit(placeholderText="Enter category")
        self.line_custom_name = QtWidgets.QLineEdit(placeholderText="Enter name")
        
        # Layout definitions
        vbox_custom = QtWidgets.QVBoxLayout()
        add_horizontal_widgets(vbox_custom, QtWidgets.QLabel("Enter custom category: "), self.line_custom_category)
        add_horizontal_widgets(vbox_custom, QtWidgets.QLabel("Enter custom object name: "), self.line_custom_name)
        searchTab4.setLayout(vbox_custom)
        