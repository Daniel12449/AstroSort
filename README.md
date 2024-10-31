
<h1 align="center">AstroSort</h1>

<h3 align="center">AstroSort is a tool to help organize raw astrophotography images. </h3>
<br/>

<p align="center">
<img src="img/main_tab.png" width="800" >
<img src="img/files_tab.png" width="800" >
<img src="img/metadata_tab.png" width="800" title="Screenshots of AstroQuery">
</p>

- copy and rename added images into a easily recognizable structure
- handles light, dark, flat and bias frames
- inserts additional information into the folder structure and file names such as:
  object, date, camera, focal length, exposure time and iso/gain value
- most of the metadata can be pulled from the image files if exiftool is available on PATH
- object search following categories: Deep Sky, large and small solar system objects, constellations and a custom category
- generated folder structure can be used directly in common stacking software
- no restriction for file type
- no changes to the raw files with exception of the name

### Example of new file structure:
```
ObjectCategory/
└── ObjectName
    └── Date_Location
        └── Camera_Focal-Length
            ├── BIAS
            │   └── B_Exposure_ISO/Gain_Image-Name
            ├── DARKS
            │   └── D_30s_800_IMG_4398.CR2
            ├── FLATS
            │   └── F_30s_800_IMG_4401.CR2
            └── LIGHTS
                └── L_30s_800_IMG_4393.CR2
```

### Built using:
- [PySide6](https://wiki.qt.io/Main)
- [Astroquery](https://github.com/astropy/astroquery)
