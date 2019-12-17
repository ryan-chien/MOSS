FROM ubuntu:18.04

ARG project_name=default
ARG project_language=python


ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH


##These need to be distinct for some reason
RUN apt-get update
RUN apt-get install -y libxss1 \
	aptitude \
	software-properties-common \
	ed \
	less \
	locales \
	vim-tiny \
	wget \
	ca-certificates \
	gnupg \
	fonts-texgyre \
	sudo \
	bzip2 \
	libglib2.0-0 \
	libxext6 \
	libsm6 \
	libxrender1 \
	git \
	mercurial \
	subversion \
	&& wget --quiet http://pki.arl.psu.edu/CertEnroll/ARL_Root_CA.crt \
	&& mv ARL_Root_CA.crt /usr/local/share/ca-certificates \
    && /usr/sbin/update-ca-certificates \
    && wget --quiet https://artifactory.arl.psu.edu/arl-cacerts/bundle/arl_custom_cert_bundle.pem \
    && mkdir /certs && mv arl_custom_cert_bundle.pem /certs/. \
	&& rm -rf /var/lib/apt/lists/*

RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh -O ~/anaconda.sh \
    && /bin/bash ~/anaconda.sh -b -p /opt/conda \
    && rm ~/anaconda.sh \
    && ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh \
    && echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc \
    && echo "conda activate base" >> ~/.bashrc \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete \
    && /opt/conda/bin/conda clean -afy
	
RUN pip config set global.cert /certs/arl_custom_cert_bundle.pem \
	&& conda config --set ssl_verify /certs/arl_custom_cert_bundle.pem \
	&& add-apt-repository ppa:marutter/c2d4u3.5 \
	&& add-apt-repository ppa:ubuntugis/ubuntugis-unstable

RUN apt-get update && \
	aptitude install -y libudunits2-dev \
	libgdal-dev \
	libgeos-dev \
	libproj-dev \
	default-jre \
	libhdf5-dev \
	&& rm -rf /var/lib/apt/lists/*
	
RUN apt-get update \ 
	&& apt-get install -y libquantlib0* \
	&& rm -rf /var/lib/apt/lists/*

RUN useradd docker \
	&& mkdir /home/docker \
	&& chown docker:docker /home/docker \
	&& addgroup docker staff
	
##Setup a spark and tensorflow venv, and add the cookiecutter setup script to the environment
RUN conda config --add channels conda-forge \
	&& conda install python=3.7.3 pep8 pylint \
	&& conda create -y -n tensorflow_cpu pip python=3.6 \
	&& conda create -y -n pyspark_env pip python=3.7.3 \
	&& conda install --name tensorflow_cpu tensorflow==2.0.0 \
	&& conda install --name pyspark_env pyspark \
	&& conda clean --all -y

##Defaulting to bash for comfort
CMD [ "/bin/bash" ]