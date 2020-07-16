# Notes on Docker:
## Build image
To build the docker image, cd to the main folder and type
```bash
docker build -t xgam:latest .
```

## Spin the container
To start the container type for the first time, run the following command:
```bash
docker run -it -v output:/archive/home/Xgam/fermi_data --name Xgam_machine xgam:latest
```
If you want, you can replace `output` with the path to the folder where you desire to save the outputs of the computation.

In the succesive iterations, you can directly start and attach the container shell with the following command:
```bash
docker start -a -i Xgam_machine
```

To stop/kill the machine use the command:
```bash
docker stop -t 5 Xgam_machine
```
