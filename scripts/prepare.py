import os

from oemof.tabular.datapackage import building


# set raw data path to the default fuchur raw raw_data_path
# which is: 'home/user/oemof-raw-data'
# change this if you have your raw data stored somewhere else
raw_data_path = os.path.join(os.path.expanduser("~"), "oemof-raw-data")


building.download_data(
    "https://zenodo.org/record/3549531/files/angus-raw-data.zip?download=1",
    directory=raw_data_path,
    unzip_file="",
)
