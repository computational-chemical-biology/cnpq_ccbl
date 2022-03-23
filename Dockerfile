FROM continuumio/miniconda:latest
MAINTAINER Ricardo R. da Silva <ridasilva@usp.br>

ENV INSTALL_PATH /ccbl_cnpq
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY environment.yml environment.yml
RUN conda env create -f environment.yml
RUN echo "source activate ccbl_cnpq" > ~/.bashrc
ENV PATH /opt/conda/envs/ccbl_cnpq/bin:$PATH

COPY . .

CMD gunicorn -b 0.0.0.0:5050 --access-logfile - "api.routes:application"
#CMD ["gunicorn", "-c", "python:config.gunicorn", "api.upload:app"]

