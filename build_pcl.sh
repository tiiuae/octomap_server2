#!/bin/bash

mkdir -p build
pushd build
cmake -DWITH_OPENGL=FALSE \
      -DWITH_PCAP=FALSE \
      -DWITH_VTK=FALSE \
      -DWITH_LIBUSB=FALSE \
      -DWITH_QT=FALSE \
      -DBUILD_features=OFF \
      -DBUILD_filters=OFF \
      -DBUILD_geometry=OFF \
      -DBUILD_kdtree=OFF \
      -DBUILD_keypoints=OFF \
      -DBUILD_ml=OFF \
      -DBUILD_outofcore=OFF \
      -DBUILD_people=OFF \
      -DBUILD_recognition=OFF \
      -DBUILD_registration=OFF \
      -DBUILD_sample_consensus=OFF \
      -DBUILD_search=OFF \
      -DBUILD_segmentation=OFF \
      -DBUILD_stereo=OFF \
      -DBUILD_surface=OFF \
      -DBUILD_tracking=OFF \
      -DBUILD_visualization=OFF \
      ..

make -j$(nproc) install
popd

