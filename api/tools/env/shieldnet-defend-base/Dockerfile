FROM ubuntu:22.04

ARG SHIELDNET_DEFEND_BRANCH
ENV DEBIAN_FRONTEND="noninteractive"

RUN apt update && \
    apt install -y wget python3 python3-pip git gnupg2 gcc g++ cmake make vim libc6-dev curl policycoreutils automake autoconf libtool apt-transport-https lsb-release python3-cryptography sqlite3

RUN mkdir shieldnetdefend && curl -sL https://github.com/shieldnetdefend/shieldnetdefend/tarball/${SHIELDNET_DEFEND_BRANCH} | tar zx --strip-components=1 -C shieldnetdefend
RUN make -C /shieldnetdefend/src deps
