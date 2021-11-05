FROM centos:centos8

RUN  mkdir -p /opt/zbxproxy/externalscripts && \
    mkdir -p /opt/zbxproxy/config && \
    mkdir -p /var/lib/zabbix/enc && \
    dnf --quiet makecache && \
    dnf -y install --setopt=tsflags=nodocs --setopt=install_weak_deps=False --best \
            epel-release && \
