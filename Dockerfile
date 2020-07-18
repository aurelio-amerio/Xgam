FROM ubuntu:latest
MAINTAINER aure.amerio@techytok.com

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Rome
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# RUN ls
# Install needed python libraries
RUN apt-get update && yes|apt-get upgrade
RUN apt-get update && apt-get install -y curl git time wget build-essential unzip gfortran libcurl4 libcurl4-openssl-dev cmake

# Install cfitsio
WORKDIR /tmp
RUN wget -O cfitsio_latest.tar.gz http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio_latest.tar.gz
RUN mkdir /cfitsio_latest && tar -C /cfitsio_latest --strip-components=1 -xvf cfitsio_latest.tar.gz
WORKDIR /cfitsio_latest
RUN ./configure --prefix=/cfitsio_latest
RUN make && make install && make clean

# Install HEALPIX
#RUN wget -O Healpix_latest.tar.gz "https://sourceforge.net/projects/healpix/files/latest/download"
#RUN mkdir /Healpix_latest && unzip -d /Healpix_latest Healpix_latest.tar.gz
WORKDIR /tmp
RUN wget -O Healpix_latest.zip "https://sourceforge.net/projects/healpix/files/Healpix_3.60/Healpix_3.60_2019Dec18.zip/download"
RUN mkdir /Healpix_latest && unzip -d /Healpix_latest Healpix_latest.zip
WORKDIR /Healpix_latest
RUN mv Healpix*/* /Healpix_latest/ && mkdir /Healpix_latest/bin && mkdir /Healpix_latest/build && mkdir /Healpix_latest/include && mkdir /Healpix_latest/lib
SHELL ["/bin/bash", "-c"]

RUN wget -O configure "https://sourceforge.net/p/healpix/code/HEAD/tree/branches/branch_v360r1104/configure?format=raw"
RUN wget -O hpxconfig_functions.sh "https://sourceforge.net/p/healpix/code/HEAD/tree/branches/branch_v360r1104/hpxconfig_functions.sh?format=raw"
RUN F_PARAL=1 FITSDIR=/cfitsio_latest/lib/ FITSINC=/cfitsio_latest/include ./configure -L --auto=f90
RUN make && make test && make clean

# Install Polspice
RUN mkdir /PolSpice
WORKDIR /Polspice/
RUN wget -O PolSpice.tar.gz http://www2.iap.fr/users/hivon/software/PolSpice/ftp/PolSpice_v03-06-06.tar.gz
RUN tar --strip-components=1 -xvf PolSpice.tar.gz && mkdir build
WORKDIR /Polspice/build
RUN cmake .. -DCFITSIO=/cfitsio_latest/lib -DHEALPIX=/Healpix_latest
RUN make && make clean
RUN /Polspice/bin/spice -help

WORKDIR /tmp
RUN curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN mkdir /archive/ && mkdir /archive/home/ && mkdir /archive/home/Xgam/ && mkdir /archive/home/Xgam/fermi_data/ && mkdir /run_xgam/ && mkdir /run_xgam/output

# Install anaconda3
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p /run_xgam/anaconda3
ENV PATH /run_xgam/anaconda3/bin:$PATH

# Install healpy and fermitools
RUN conda update -n base -c defaults conda
RUN conda config --add channels conda-forge
RUN conda create -n fermi -c conda-forge/label/cf201901 -c fermi fermitools -y
RUN conda install -y --name fermi healpy numba

RUN apt-get update && apt-get install -y libgl1-mesa-dev

# download fits
# WORKDIR /archive/home/Xgam/fermi_data/photon
# RUN wget -m -P . -nH --cut-dirs=4 -np -e robots=off https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/photon/
# Clone Xgam
WORKDIR /run_xgam
#RUN ls -lh
# RUN git clone https://github.com/nmik/Xgam.git

# copy Xgam package to /run_xgam
COPY Xgam /run_xgam/Xgam

#RUN ls /run_xgam/Xgam/bin -lh

# Creating bashrc file
RUN echo "echo 'Setting Xgam environment...'" > /root/.bashrc \
#RUN echo "export PATH=/run_xgam/anaconda3/bin:$PATH" >> /root/.bashrc \
   && echo "export PATH=/run_xgam/anaconda3/envs/fermi/bin:$PATH" >> /root/.bashrc \
   && echo "export PYTHONPATH=:/run_xgam/:${PYTHONPATH}" >> /root/.bashrc \
   && echo "export PATH=/run_xgam/Xgam/bin:${PATH}" >> /root/.bashrc \
   && echo "export P8_DATA=/archive/home/Xgam/fermi_data" >> /root/.bashrc \
   && echo "export X_OUT=/archive/home/Xgam/fermi_data" >> /root/.bashrc \
   && echo "export X_OUT_FIG=/archive/home/Xgam/fermi_data" >> /root/.bashrc \
   && echo "source activate fermi" >> /root/.bashrc \
   && echo "export HEALPIX=/Healpix_latest" >> /root/.bashrc \
   && echo "echo 'Done.'" >> /root/.bashrc \
RUN echo "bashrc file:" && less /root/.bashrc

# WORKDIR /archive/home/Xgam/fermi_data
# RUN mkdir /home/simone/
# Define entrypoint and default values for args
# CMD ["/bin/bash","-c","source /run_xgam/.bashrc && /archive/home/Xgam/fermi_data/bash_script.sh"]

# clear unused files
RUN apt-get clean
RUN rm -f /tmp/*
RUN rm -f /Polspice/PolSpice.tar.gz

CMD bash
#CMD ["/bin/bash","-c","source /run_xgam/.bashrc && /home/simone/bash_script.sh"]
