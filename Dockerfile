FROM tensorflow/tensorflow:latest-gpu-py3

RUN apt-get update && apt-get install -y \
	build-essential \
	cmake \
	pkg-config \
	libjpeg8-dev \
	libtiff5-dev \
	libjasper-dev \
	libpng12-dev \
	python3-matplotlib \
	git

#installs opencv 4.1.0
RUN curl -o 4.1.0.zip https://codeload.github.com/opencv/opencv/zip/4.1.0 \
	&& unzip 4.1.0.zip \
	&& cd opencv-4.1.0/ \
	&& mkdir build \
	&& cd build \
	&& cmake CMAKE_BUILD_TYPE=RELEASE \
		-D CMAKE_INSTALL_PREFIX=/usr/local \
		-D INSTALL_PYTHON_EXAMPLES=ON \
		 -D INSTALL_C_EXAMPLES=OFF \
		.. \
	&& make -j16 \
	&& make install \
	&& cd / \
	&& rm /4.1.0.zip 
RUN rm -r opencv-4.1.0

# Cytomine-python-client

RUN mkdir /root/Cytomine
RUN cd /root/Cytomine/ && git clone https://github.com/cytomine/Cytomine-python-client.git && cd Cytomine-python-client/ && git checkout v1.1.1
RUN cd /root/Cytomine/Cytomine-python-client/client/ && python setup.py build && python setup.py install
RUN cd /root/Cytomine/Cytomine-python-client/utilities/ &&  python setup.py build && python setup.py install

RUN cd /root/Cytomine/ && git clone https://github.com/cytomine/Cytomine-tools.git && cd Cytomine-tools/ && git checkout tags/v1.1

COPY hello.py app/

WORKDIR app

ENTRYPOINT ["python3","hello.py"]
