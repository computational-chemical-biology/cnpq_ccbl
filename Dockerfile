FROM ubuntu:22.04
MAINTAINER Ricardo R. da Silva <ridasilva@usp.br>

ENV INSTALL_PATH /ccbl_cnpq
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

RUN apt-get -y update
RUN apt-get install -y wget 
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
RUN /bin/bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh && \
    echo "export PATH=/opt/conda/bin:$PATH" > /etc/profile.d/conda.sh
ENV PATH /opt/conda/bin:$PATH

COPY environment.yml environment.yml
ENV CONDA_PLUGINS_AUTO_ACCEPT_TOS=true
RUN conda env create -f environment.yml
RUN echo "source activate ccbl_cnpq" > ~/.bashrc
ENV PATH /opt/conda/envs/ccbl_cnpq/bin:$PATH

# Installs the dependencies used by Chrome and Selenium
RUN apt-get install --yes --quiet --no-install-recommends \
    gettext \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libx11-6 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    libxshmfence1 \
    wget \
    xdg-utils \
    netcat \
    xvfb \
    libcurl3-gnutls \
    libcurl3-nss \
    libcurl4 \
    libvulkan1 \
 && rm -rf /var/lib/apt/lists/*

# Install Chrome
COPY google-chrome-stable_current_amd64.deb google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
#RUN pip install chromedriver-binary
RUN pip install chromedriver-binary-auto

COPY . .

CMD gunicorn -b 0.0.0.0:5050 --access-logfile - "api.routes:application"
#CMD ["gunicorn", "-c", "python:config.gunicorn", "api.upload:app"]

