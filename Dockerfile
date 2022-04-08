#
# sensOCampus | neOCampus end-devices management
#
# F.Thiebolt    feb.21  base image moved from fedora to python
# Thiebolt F.   Oct.17  updates
# Thiebolt F.   Mar.16  initial release
#

# Python image is debian-buster based
FROM python:latest
MAINTAINER "Francois <thiebolt@irit.fr>"

# Switch to bash as default shell
SHELL [ "/bin/bash", "-c" ]

# Build ARGS
ARG APP="/app"

# Runtime & Build-time args
# Location of files to add to the container
# Note this <relative_path> to the build env @ host
ENV DOCKYARD="/dockyard" \
    DESTDIR="/opt/app"

# Switch to root user to enable installation (default)
#USER root

# Copy configuration directory
COPY ${DOCKYARD} ${DOCKYARD}

# Copy application directory
COPY ${APP} ${DESTDIR}

# password generation:
# python -c 'import crypt; print(crypt.crypt("passwd", crypt.mksalt(crypt.METHOD_SHA512)))'

#
# Set-up ssh environnement / password / authorized-key + file copy
RUN echo -e "Starting setup ..." \
    # root passwd
    && echo 'root:$6$TGvTS4A28QdWeLvG$I4A/M/mOSUNoU0rKkRflAO0MTZtJGEGlf/P13vz7l31bLvf8FQAwBmQArcOCNwdmVrBdc.CVIJ848jRQdCChX.' | chpasswd -e \
    # SSH stuffs
    && cp -af ${DOCKYARD}/root / \
    && mkdir -p /root/.ssh \
    && cp -af ${DOCKYARD}/authorized_keys /root/.ssh/ \
    && chmod 600 /root/.ssh/authorized_keys \
    && chmod g-w /root \
    # custom motd message
    && cp -af ${DOCKYARD}/myMotd /etc/motd \
    && chmod 644 /etc/motd \
    # System stuffs
    && apt-get -y update \
    && apt-get -y --allow-unauthenticated install \
        apt-utils \
        git \
        procps \
        tmux \
        host \
        net-tools \
        findutils \
        openssh-server \
        openssh-client \
        python3-pip \
        python3-psycopg2 \
        uwsgi \
        uwsgi-plugin-python3 \
        python3-dev \
        python3-ipython \
        sqlite3 \
        libsqlite3-mod-spatialite \
        mime-support \
        vim \
    # Supervisor setup
    && apt-get -y install python3-pip crudini \
    && pip3 install supervisor \
    && echo_supervisord_conf > /etc/supervisord.conf \
    && crudini --set /etc/supervisord.conf include files /etc/supervisord.d/\*.ini \
    && cp -af ${DOCKYARD}/supervisord.d /etc \
    && mkdir -p /var/log/supervisor \
    # [oct.20] fedora fix for 'unable to open HTTP server'
    && mkdir -p /run/supervisor \
    # SSH server setup
    && mkdir -p /var/run/sshd \
    && ssh-keygen -A \
    # app. python specific requirements
    && pip3 install -r ${DOCKYARD}/requirements.txt

#
# Ports for sshd, django app. and uwsgi stats
EXPOSE 22 8000 8042

# CMD
CMD [ "supervisord", "-n" ]
#, "--loglevel=debug"]

