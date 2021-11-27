FROM python:3.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app 
ADD . /app

# install uwsgi
# uwsgi, adapted from https://github.com/docker-library/python.git
# in file python/3.6/slim/Dockerfile
RUN set -ex \
    && buildDeps=' \
        gcc \
        libbz2-dev \
        libc6-dev \
        libgdbm-dev \
        liblzma-dev \
        libncurses-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        libpcre3-dev \
        make \
        tcl-dev \
        tk-dev \
        wget \
        xz-utils \
        zlib1g-dev \
    ' \
    && deps=' \
        libexpat1 \
    ' \
    && apt-get update && apt-get install -y $buildDeps $deps --no-install-recommends  && rm -rf /var/lib/apt/lists/* \
    && pip install uwsgi \
    && apt-get purge -y --auto-remove $buildDeps \
    && find /usr/local -depth \
    \( \
        \( -type d -a -name test -o -name tests \) \
        -o \
        \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
    \) -exec rm -rf '{}' +


# Install python3 dependencies
COPY ./requirements.txt /var/www/requirements.txt
RUN echo "***** install python and python dependencies"
RUN pip install -r /var/www/requirements.txt
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords

# Run the specified command within the container.
CMD ["uwsgi", "app.ini"]


