# ----------------------------------------------------------------------------
# -                        Open3D: www.open3d.org                            -
# ----------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2018-2021 www.open3d.org
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
# ----------------------------------------------------------------------------

import open3d as o3d
import numpy as np
import matplotlib.image as mpimg
import os
import re


def visualize_rgbd(rgbd_image):
    print(rgbd_image)

    o3d.visualization.draw_geometries([rgbd_image])

    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
        rgbd_image,
        o3d.camera.PinholeCameraIntrinsic(
            o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault))
    # Flip it, otherwise the pointcloud will be upside down.
    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    o3d.visualization.draw_geometries([pcd])


# This is special function used for reading NYU pgm format
# as it is written in big endian byte order.
def read_nyu_pgm(filename, byteorder='>'):
    with open(filename, 'rb') as f:
        buffer = f.read()
    try:
        header, width, height, maxval = re.search(
            b"(^P5\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PGM file: '%s'" % filename)
    img = np.frombuffer(buffer,
                        dtype=byteorder + 'u2',
                        count=int(width) * int(height),
                        offset=len(header)).reshape((int(height), int(width)))
    img_out = img.astype('u2')
    return img_out


def nyu_dataset():
    print("Read NYU dataset")
    # Open3D does not support ppm/pgm file yet. Not using o3d.io.read_image here.
    # MathplotImage having some ISSUE with NYU pgm file. Not using imread for pgm.
    dir_path = os.path.dirname(os.path.abspath(__file__))
    color_raw = mpimg.imread(
        dir_path + "/../../test_data/RGBD/other_formats/NYU_color.ppm")
    depth_raw = read_nyu_pgm(
        dir_path + "/../../test_data/RGBD/other_formats/NYU_depth.pgm")
    color = o3d.geometry.Image(color_raw)
    depth = o3d.geometry.Image(depth_raw)
    rgbd_image = o3d.geometry.RGBDImage.create_from_nyu_format(
        color, depth, convert_rgb_to_intensity=False)

    print("Displaying NYU color and depth images and pointcloud ...")
    visualize_rgbd(rgbd_image)


def redwood_dataset():
    print("Read Redwood dataset")
    dir_path = os.path.dirname(os.path.abspath(__file__))
    color_raw = o3d.io.read_image(dir_path +
                                  "/../../test_data/RGBD/color/00000.jpg")
    depth_raw = o3d.io.read_image(dir_path +
                                  "/../../test_data/RGBD/depth/00000.png")
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
        color_raw, depth_raw, convert_rgb_to_intensity=False)

    print("Displaying Redwood color and depth images and pointcloud ...")
    visualize_rgbd(rgbd_image)


def sun_dataset():
    print("Read SUN dataset")
    dir_path = os.path.dirname(os.path.abspath(__file__))
    color_raw = o3d.io.read_image(
        dir_path + "/../../test_data/RGBD/other_formats/SUN_color.jpg")
    depth_raw = o3d.io.read_image(
        dir_path + "/../../test_data/RGBD/other_formats/SUN_depth.png")
    rgbd_image = o3d.geometry.RGBDImage.create_from_sun_format(
        color_raw, depth_raw, convert_rgb_to_intensity=False)

    print("Displaying SUN color and depth images and pointcloud ...")
    visualize_rgbd(rgbd_image)


def tum_dataset():
    print("Read TUM dataset")
    dir_path = os.path.dirname(os.path.abspath(__file__))
    color_raw = o3d.io.read_image(
        dir_path + "/../../test_data/RGBD/other_formats/TUM_color.png")
    depth_raw = o3d.io.read_image(
        dir_path + "/../../test_data/RGBD/other_formats/TUM_depth.png")
    rgbd_image = o3d.geometry.RGBDImage.create_from_tum_format(
        color_raw, depth_raw, convert_rgb_to_intensity=False)

    print("Displaying TUM color and depth images and pointcloud ...")
    visualize_rgbd(rgbd_image)


if __name__ == "__main__":
    nyu_dataset()
    redwood_dataset()
    sun_dataset()
    tum_dataset()
