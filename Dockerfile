FROM ghcr.io/tiiuae/fog-ros-baseimage-builder:sha-62e6243 AS builder

COPY . $SRC_DIR/octomap_server2

RUN apt update && \
    apt install -y octomap-staticdev

RUN /packaging/build_colcon.sh

#  ▲               runtime ──┐
#  └── build                 ▼

FROM ghcr.io/tiiuae/fog-ros-baseimage:sha-62e6243

RUN apt update && \
    apt install -y octomap-staticdev \
    pcl-ros \
    pcl-conversions \
    pcl-msgs \
    octomap-ros \
    octomap-msgs \
    laser-geometry \
    boost

ENTRYPOINT [ "/entrypoint.sh" ]
COPY entrypoint.sh /entrypoint.sh

COPY --from=builder $INSTALL_DIR $INSTALL_DIR
