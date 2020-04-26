# Build an image that can serve mlflow models.
FROM ubuntu:18.04

ARG MODEL_DIR

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         curl \
         nginx \
         ca-certificates \
         bzip2 \
         build-essential \
         cmake \
         openjdk-8-jdk \
         git-core \
         maven \
    && rm -rf /var/lib/apt/lists/*
# Download and setup miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh

RUN bash ./miniconda.sh -b -p /miniconda && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    rm ./miniconda.sh

ENV PATH="/miniconda/bin:$PATH"
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV GUNICORN_CMD_ARGS="--timeout 60 -k gevent"
# Set up the program in the image
WORKDIR /opt/mlflow

COPY ${MODEL_DIR} /opt/mlflow/mlruns/0/mushroom/
COPY conda.yaml conda.yaml
RUN conda env create -f conda.yaml -n mlflow && \
    echo "conda activate mlflow" >> ~/.bashrc

RUN echo "artifact_location: file:///opt/mlflow/mlruns/0\n\
experiment_id: '0'\n\
lifecycle_stage: active\n\
name: Default\n"\
>> /opt/mlflow/mlruns/0/meta.yaml

RUN echo "artifact_uri: file:///opt/mlflow/mlruns/0/mushroom/artifacts\n\
end_time: 1586488595673\n\
entry_point_name: ''\n\
experiment_id: '0'\n\
lifecycle_stage: active\n\
name: ''\n\
run_id: mushroom\n\
run_uuid: mushroom\n\
source_name: ''\n\
source_type: 4\n\
source_version: ''\n\
start_time: 1586488595672\n\
status: 3\n\
tags: []\n\
user_id: mlflow\n"\
>> /opt/mlflow/mlruns/0/mushroom/meta.yaml

EXPOSE 8000
ENTRYPOINT ["conda", "run", "-n", "mlflow", "mlflow", "models", "serve", "-m", "runs://0/mushroom/model", "-p", "8000"]
CMD ["-h", "0.0.0.0", "--no-conda"]
