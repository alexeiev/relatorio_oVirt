FROM almalinux:8.9

LABEL MAINTAINER="AlexeievFA"

WORKDIR /app

RUN dnf install -y unzip gcc libxml2-devel vim && \
curl -sSL -o v1.0.0.zip https://github.com/alexeiev/relatorio_oVirt/archive/refs/tags/v1.0.0.zip && \
unzip v1.0.0.zip && cd relatorio_oVirt-1.0.0

RUN dnf install -y http://resources.ovirt.org/pub/yum-repo/ovirt-release44.rpm && \
dnf install -y python3-ovirt-engine-sdk4 
RUN pip3 install -r relatorio_oVirt-1.0.0/requirements.txt

WORKDIR /app/relatorio_oVirt-1.0.0

VOLUME /app/relatorio_oVirt-1.0.0

ENTRYPOINT ["/bin/bash"]
