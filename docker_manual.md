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
docker run -it -v /f/Users/Aure/Documents/fermi_data:/archive/home/Xgam/fermi_data -v /f/Users/Aure/Documents/GitHub/Xgam/Xgam:/run_xgam/Xgam --name Xgam_machine aureamerio/xgam:latest
```
Place replace `/f/Users/Aure/Documents/fermi_data` with the path to your fermi_data folder.

In the succesive iterations, you can directly start and attach the container shell with the following command:
```bash
docker start -a -i xgam_machine
```

To stop/kill the machine use the command:
```bash
docker stop -t 5 xgam_machine
```

It is often usefull to chain those commands in a single one, not to forget to close the container.

In unix, type:
```bash
docker start -a -i xgam_machine && docker stop -t 5 xgam_machine
```

In windows, type:
```bash
docker start -a -i xgam_machine; docker stop -t 5 xgam_machine
```

# Docker Compose
An alternative way to use this container is through `docker-compose`. <br>
In this case before you can spin the container, it is needed to edit the file `docker-compose.yml` and adjust the path to fermi_data.
To spin the container, first you need to open a shell, cd to the git repository and type `docker-compose up` to start the container. `docker-compose` will download the image and take care of everything. Once the image is running, you can open another shell and type `docker attach xgam_machine` to get access to the shell inside the container. Once you are done, come back to the shell where you typed `docker-compose up` and press `ctrl+c` to gracefully stop the container.

python Xgam/bin/mkdataselection.py -c Xgam/config/config_dataselection_5w.py | tee /archive/home/Xgam/fermi_data/logs/5w_terminal_output.txt

python Xgam/bin/mkdataselection.py -c Xgam/config/config_dataselection_6y.py
python Xgam/bin/mkdataselection.py -c Xgam/config/config_dataselection_10y.py
