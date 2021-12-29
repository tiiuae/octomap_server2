ros_distro=${ROS_DISTRO:=foxy}

iname=${PACKAGE_NAME:=pcl_conversions}

docker build \
  --build-arg UID=$(id -u) \
  --build-arg GID=$(id -g) \
  --build-arg ROS_DISTRO=${ros_distro} \
  --build-arg PACKAGE_NAME=${iname} \
  --pull \
  -f Dockerfile.test -t "octomap-test:latest" .
