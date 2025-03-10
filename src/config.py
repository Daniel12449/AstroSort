from configparser import ConfigParser
import logging
import vars

def handleConfig(window, config_path):
    
    cfg = ConfigParser()
    cfg.read(config_path)
    
    # [main]
    window.tab1.checkbox_filename.setChecked(cfg.getboolean('main', 'replace_names', fallback=False))

    window.tab1.line_output_path.setText(cfg.get('main', 'local_output_path', fallback=''))
    window.tab1.checkbox_save_locally.setChecked(cfg.getboolean('main', 'enable_local_storage', fallback=True))
    
    # [S3]
    if cfg.has_section('S3'):
        window.tab1.line_output_s3.setText(cfg.get('S3', 's3_output_bucket', fallback=''))
        vars.s3_bucket = window.tab1.line_output_s3.text()
        window.tab1.checkbox_save_s3.setChecked(cfg.getboolean('S3', 'enable_s3_upload', fallback=False))
        vars.use_s3 = True
        
    
    
def handleProfile(window, config_path, profile):
    
    cfg = ConfigParser()
    cfg.read(config_path)
    
    if cfg.has_section(profile):
        settings = dict(cfg.items(profile))
    else:
        logging.info("No profile stored.")
        return
    
    if 'default_location' in settings: window.tab4.line_location.setText(settings['default_location'])
    
    if 'dark_exp' in settings: window.tab4.line_exposure_dark.setText(settings['dark_exp'])
    if 'flat_exp' in settings: window.tab4.line_exposure_flat.setText(settings['flat_exp'])
    if 'bias_exp' in settings: window.tab4.line_exposure_bias.setText(settings['bias_exp'])
    if 'dark_iso' in settings: window.tab4.line_iso_dark.setText(settings['dark_iso'])
    if 'flat_iso' in settings: window.tab4.line_iso_flat.setText(settings['flat_iso'])
    if 'bias_iso' in settings: window.tab4.line_iso_bias.setText(settings['bias_iso'])
    
    if 'type' in settings:
        if settings['type'] == 'exif':
            if 'default_camera_model' in settings: window.tab4.exif_camera.setText(settings['default_camera_model'])
            if 'default_exposure_time' in settings: window.tab4.exif_exposure.setText(settings['default_exposure_time'])
            if 'default_iso' in settings: window.tab4.exif_iso.setText(settings['default_iso'])
            if 'default_focal_length' in settings: window.tab4.exif_focal_length.setText(settings['default_focal_length'])
            
        if settings['type'] == 'fits':
            if 'default_camera_model' in settings: window.tab4.fits_camera.setText(settings['default_camera_model'])
            if 'default_exposure_time' in settings: window.tab4.fits_exposure.setText(settings['default_exposure_time'])
            if 'default_iso' in settings: window.tab4.fits_gain.setText(settings['default_iso'])
            if 'default_focal_length' in settings: window.tab4.fits_focal_length.setText(settings['default_focal_length'])
            


