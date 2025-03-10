import pandas
df_lights = pandas.DataFrame()
df_darks = pandas.DataFrame()
df_flats = pandas.DataFrame()
df_bias = pandas.DataFrame()

output_dir_local = None
s3_bucket = None
output_dir_s3 = None
canceled = False
current_file = 0

use_s3 = False
s3_bucket_list = []