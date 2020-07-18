# Notes on Docker:
## Build image
To build the docker image, cd to the main folder and type
```bash
docker build -t xgam:latest .
```

Alternatively one can also pull the built image from docker hub using the following command:
```bash
docker pull aureamerio/xgam:latest
```
## Download data
Before you are able to use this container, you need to download the following files. A download manager like Jdownloader is suggested and it is advisable to adjust the number of simultaneous downloads as n=max_download_speed_in_MBs/500
- First create a folder called fermi_data,
- Then download the weekly data from https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/photon/ and place it in the fermi_data/photon folder
Please download only the files you intend to use, as the whole dataset takes more than 100Gb.
- Finally download https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/mission/spacecraft/lat_spacecraft_merged.fits and place it in fermi_data/spacecraft

## Spin the container
To start the container type for the first time, run the following command:
```bash
docker run -it -v /f/Users/Aure/Documents/fermi_data:/archive/home/Xgam/fermi_data --name Xgam_machine xgam:latest
```
Place replace `/f/Users/Aure/Documents/fermi_data` with the path to your fermi_data folder.

In the succesive iterations, you can directly start and attach the container shell with the following command:
```bash
docker start -a -i Xgam_machine
```

To stop/kill the machine use the command:
```bash
docker stop -t 5 Xgam_machine
```


python bin/mkdataselection.py -c config/config_dataselection.py
