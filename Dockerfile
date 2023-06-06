FROM ghcr.io/tiiuae/fog-ros-baseimage-builder:sha-c549c2f AS builder

COPY . $SRC_DIR/octomap_server2

RUN apt update && \
    apt install -y octomap-staticdev

RUN /packaging/build_colcon.sh

#  ▲               runtime ──┐
#  └── build                 ▼

FROM ghcr.io/tiiuae/fog-ros-baseimage:sha-c549c2f

RUN apt update && \
    apt install -y octomap-staticdev \
    pcl-ros \
    pcl-conversions \
    pcl-msgs \
    octomap-ros \
    octomap-msgs \
    laser-geometry \
    rosidl-generator-py \
    rosidl-generator-c \
    boost

ENTRYPOINT [ "/entrypoint.sh" ]
COPY entrypoint.sh /entrypoint.sh

COPY --from=builder $INSTALL_DIR $INSTALL_DIR
