# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 22:28:03 2023

@author: Jackson Wilt

Modified code from Fluid Lab - University of Amsterdam (Github)
"""

import matplotlib as mpl
import os
import cv2
import numpy as np
import scipy as scp
from skimage import morphology as morph
from skimage.measure import regionprops
import matplotlib.pyplot as plt
from matplotlib.image import imread


"""
#OVERVIEW:
#Hello! This code will analyze bending filaments and create arrays of their
#skeletonized geometries and calculate the curvature values. No values are 
#normalized or scaled so that will need to be included for each respective video dimensions.

#It is split into THREE main SECTIONS:
#
#       SECTION 1: Skeletonization and Tracking (for several sample frames)
#
#       SECTION 2: Plotting curvature values on the nodes of sample images
#
#       SECTION 3: Plotting max curvature values over time
#
#       SECTION 4: Plotting curvature along filament over a specified time range
"""


###############################################################################
#
"""
#Section 1: This is the main section that designates the way the video and images
#           are processed and in order to tune the blurring, erosion, tracking, 
#           and binarization effects you will modify them here. You are able to 
#           import a video file and export images using an ffmpeg for video 
#           processing. Sample images are extracted from all frames to plot their
#           nodal locations and spline fits using the skeleton values.
# 
#           Also to correctly initialize the skeleton/spline you must define a
#           clamping point for the filament. (Where it is rigidly connected off-screen)
"""
plt.figure(dpi=300)
xClamp = 841
yClamp = 0
size = 160
yminHook = yClamp - size
ymaxHook = yClamp + size

testFrameNums = []
testFrames = []
nTestframes = 9

######################## INPUT NEW FILE LOCATIONS ############################
root = r"C:\Users\jacks\Downloads/"  # change as applicable
ffmpeg_path = 'C:\FFmpeg\bin'
os.environ['PATH'] = ffmpeg_path + ';' + os.environ['PATH']
fileName = "single_filament_actuation.mp4"  # name of video to be analysed
path = root + fileName
imagesFolderPath = imagesFolderPath = path[:-4] + '-frames/'
##############################################################################


plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 20


def videoToImages(path):
    """
    Input: path of the to store frames

    Checks if an image folder exists. If not creates png files of the video and stores them in a folder.
    A de-interlacing filter is used while aquiring the frames.
    Returns amount of frames created.
    """
    print(os.path.exists(path[:-1]))
    # Create frames
    if (os.path.exists(path[:-1]) == False):
        videoPath = path[:-8]  # location of video
        os.makedirs(path[:-1])  # location of folder with frames
        ffmpeg_path = 'C:\FFmpeg\bin'
        os.environ['PATH'] = ffmpeg_path + ';' + os.environ['PATH']
        os.system("ffmpeg -i {} -filter_complex bwdif -vsync 0 {}%06d.png".format(
            "\"" + videoPath + '.mp4"', "\"" + imagesFolderPath + '"'))
        # Goes through created frames and removes faulty frames:
        for image in (os.listdir(path)):
            if image.startswith("._"):
                os.remove(path + image)
        nFrames = len(os.listdir(path))
        print("Number of frames created : " + str(nFrames))
    else:
        nFrames = len(os.listdir(path))
        print("Folder contains : " + str(nFrames) + " frames")
    return nFrames


nFrames = videoToImages(imagesFolderPath)
# FPS, FRAME_COUNT, DURATION = sf.findVideoProperties(path)


def showMultiplePlots(framesList, title):
    nTestframes = len(framesList)
    plt.figure(figsize=(10, 10))
    plt.suptitle(str(title))
    for i in np.arange(0, nTestframes):
        plt.subplot(3, 3, i+1)
        plt.imshow(framesList[i])
        plt.title("Frame number : " + str(testFrameNums[i]))
        i += 1


def binarization(frame):
    """
    Input: Frame as np.array
    Output: Frame as np.array in binary form
    """
#     frame = cv2.fastNlMeansDenoising(frame, None, 20, 7, 21)
    kernel = np.ones((3, 3), 'uint8')
    frame = cv2.blur(frame, (3, 3))
    frame = cv2.erode(frame, kernel)
    tresh = 0.1  # important thresh holding factor
    frame[frame >= tresh] = 1  # 0.7
    frame[frame < tresh] = 0  # 0.7
    frame[yminHook:ymaxHook, 0:xClamp] = 0
    return frame


def openFrame(n):
    """
    Input: Framenumber
    Opens an image corresponding with the framenumber
    """
    if n > nFrames:
        print("Framenumber too high. Image does not exist. Folder contains : " +
              str(nFrames) + " frames")
    else:
        fileName = ""
        i = 0
        while i < 6 - len(str(n)):
            fileName += "0"
            i += 1
        fileName = fileName + str(n) + ".png"
        frame = imread(imagesFolderPath + fileName)
        return frame


def cropFrame(frame, xmin, xmax, ymin, ymax):
    """
    Input: image as array & cropping area
    Output: cropped frame as array
    """
    frame = frame[ycropmin:ycropmax, xcropmin:xcropmax]
    return frame


def showMultiplePlots(framesList, title):
    nTestframes = len(framesList)
    plt.figure(figsize=(30, 30))
    plt.suptitle(str(title))
    for i in np.arange(0, nTestframes):
        plt.subplot(3, 3, i+1)
        plt.imshow(framesList[i])
        plt.title("Frame number : " + str(testFrameNums[i]))
        i += 1


testFrameNums = []
testFrames = []
nTestframes = 9

# Opening a set amount of testframes
for i in np.arange(0, nTestframes):
    frameNum = round((nFrames-2)/nTestframes)*i + 1
    testFrameNums.append(frameNum)
    testFrames.append(openFrame(frameNum))
showMultiplePlots(testFrames, "Testframes unedited")


# Specify cropping area
ycropmin = 0
ycropmax = -1
xcropmin = 0
xcropmax = 1500

# Apply cropping to testframes
croppedTestFrames = []
for frame in testFrames:
    testframe = cropFrame(frame.copy(), xcropmin, xcropmax, ycropmin, ycropmax)
    croppedTestFrames.append(testframe)

showMultiplePlots(croppedTestFrames, "Cropped testframes")

colorChannel = 2
croppedTestFrames2 = []
for frame in croppedTestFrames:
    test = frame.copy()
    croppedTestFrames2.append(test[:, :, colorChannel])
showMultiplePlots(croppedTestFrames2, "1 color channel")

# Plotting all 3 color channels seperately
plt.figure(figsize=(10, 4))
for i in np.arange(0, 3):
    testframe = croppedTestFrames[3].copy()
    plt.subplot(1, 3, i+1)
    plt.title("Channel " + str(i))
    plt.imshow(testframe[:, :, i])
plt.show()


colorChannel = 2
croppedTestFrames2 = []
for frame in croppedTestFrames:
    test = frame.copy()
    croppedTestFrames2.append(test[:, :, colorChannel])
showMultiplePlots(croppedTestFrames2, "1 color channel")

binaryTestFrames = []
for frame in croppedTestFrames2:
    test = frame.copy()
    binaryTestFrames.append(binarization(test))
showMultiplePlots(binaryTestFrames, "Frames as binary")


def reflect_boundaries(arr):
    lr = np.fliplr(arr)
    new = np.concatenate((lr, arr, lr), axis=1)
    ud = np.flipud(new)
    return np.concatenate((ud, new, ud), axis=0)


def set_borders_to(arr, value=0):
    new_array = arr.copy()
    new_array[0, :] = value
    new_array[-1, :] = value
    new_array[:, 0] = value
    new_array[:, -1] = value
    return new_array


def inverse_reflect_boundaries(arr):
    return np.hsplit(np.vsplit(arr, 3)[1], 3)[1]


def node_detection(bitmap):
    """
    takes boolean-like 2d array und finds nodes (2 or more neigbours) and
    endpoints (extractly 1 neigbour) in network
    returns (nodes, endpoints) as seperate arrays
    """
    skeleton = np.where(bitmap != 0, 1, 0)
    sum = (np.roll(skeleton,  1, axis=1) +
           np.roll(skeleton, -1, axis=1) +
           np.roll(skeleton,  1, axis=0) +
           np.roll(skeleton, -1, axis=0) +
           np.roll(np.roll(skeleton, 1, axis=0), 1, axis=1) +
           np.roll(np.roll(skeleton, 1, axis=0), -1, axis=1) +
           np.roll(np.roll(skeleton, -1, axis=0), 1, axis=1) +
           np.roll(np.roll(skeleton, -1, axis=0), -1, axis=1))
    nodes = np.where(sum > 2, 1, 0) * skeleton
    endpoints = np.where(sum == 1, 1, 0) * skeleton
    return nodes, endpoints


def remove_branch_crit(branch, endpoints, branch_thresh):
    """ checks critiria if branch should be removed:
    1. lenghts < branch_thresh
    2. contains endpoints (i.e. does not connect anything)
    """
    if np.max(branch + endpoints) > 1 and np.sum(branch) < branch_thresh:
        return True
    else:
        return False


def extract_network(mask, n):
    """
    returns a modified mask containing only the n largest objects, smaller
    objects are masked
    if n==None the mask is returned unchanged
    """
    if n == None:
        return mask
    # returns mask that contains only the n largest connected areas
    labels = morph.label(mask, connectivity=2)
    regions = regionprops(labels)
    areas = np.argsort([r.area for r in regions])
    # list of labels of the n largest areas
    selected_labels = [regions[a].label for a in areas[-n:]]
    return np.where(np.isin(labels, selected_labels), 1., 0.)


def extract_skeleton(mask, method='medial_axis', branch_thresh=50, extract=1):
    """ creates skeleton of bool-like image, removes small branches
    (smaller than branch_thresh)

    method = 'medial_axis':
    returns the line consiting of pixels that have 2 (or more) nearest pixels;
    often many small branches emerge

    method = 'skeletonize':
    returns the skeleton calculated via morph. thinning, which does not
    guarantee to get the center line in a pixel(!) image
    """
    refl_mask = reflect_boundaries(mask)
    if method == 'medial_axis':
        # returns the line consiting of pixels that have 2 (or more)
        # nearest pixels; often many small branches emerge
        medial_axis = morph.medial_axis(refl_mask)
    elif method == 'skeletonize':
        # returns the skeleton calculated via morph. thinning, which does not
        # guarantee to get the center line in a pixel(!) image
        medial_axis = morph.skeletonize(refl_mask)
    medial_axis = inverse_reflect_boundaries(medial_axis)
    medial_axis = set_borders_to(medial_axis, value=0)
    if branch_thresh > 0:
        last_medial_axis = medial_axis.copy()
        while True:
            nodes, endpoints = node_detection(medial_axis)
            seperated_skel = medial_axis - nodes
            seper_l, no_l = morph.label(seperated_skel, connectivity=2,
                                        return_num=True)
            # iterate over branches
            for l in range(1, no_l+1):
                branch = np.where(seper_l == l, 1, 0)
                # remove branches that don't connect anything and are shorter than
                # branch_thresh
                if remove_branch_crit(branch, endpoints, branch_thresh):
                    medial_axis = np.where(branch == 1, 0, medial_axis)
                    # plt.imshow(medial_axis)
                    # plt.show()
            # add nodes to conncect network again
            medial_axis = np.logical_or(medial_axis, nodes)
            # remove nodes that are not longer part of the network
            medial_axis = morph.remove_small_objects(medial_axis, 6,
                                                     connectivity=2)
            # thinning necessary since nodes that lost a branch are wider that 1px
            medial_axis = morph.skeletonize(medial_axis)
            medial_axis = extract_network(medial_axis, extract)
            if np.all(last_medial_axis == medial_axis):
                break
            else:
                last_medial_axis = medial_axis.copy()
    return medial_axis


def sort_skel(skel, x, y, endpoint=None, max_dist=20):
    """
    skel: skeletonized image (only one skel!)

    Returns:
        sort_list: sorted list from start to begin for parametrization
    """
    points = np.asarray(
        np.where(skel))                   # get coordinates of skel
    nodepoints, endpoints = node_detection(
        skel)  # find node and endpoints of skel
    points2 = points                             # copy
    endpoint_list = np.asarray(np.where(endpoints))  # make list
    endpoint_list = endpoint_list.T
    clamp_point = [y, x]
    sort_list = [clamp_point]  # initialize
    ref_point = clamp_point
    # loop over list and find the minimal distance towards a reference point
    # by that one subsequently 'walks' on the curve and sorts it accordingly
    for i in range(np.shape(points)[1]):
        pos = np.argmin(
            np.sqrt((points2[0]-ref_point[0])**2+(points2[1]-ref_point[1])**2))
        ref_point = points2[:, pos]
        points2 = np.delete(points2, pos, axis=1)  # delete previous point
        sort_list.append(ref_point)
    sort_list = np.asarray(sort_list)
    # remove ill-defined points close to start to avoid loopy splines.
    while np.sqrt((sort_list[-1, 0]-sort_list[0, 0])**2 + (sort_list[-1, 1]-sort_list[0, 1])**2) < max_dist:
        sort_list = sort_list[:len(sort_list)-1]
    return sort_list


branchTresh = 50
testSkeletons = []
for frame in binaryTestFrames:
    skel = extract_skeleton(frame, method='skeletonize',
                            branch_thresh=branchTresh, extract=1)
    testSkeletons.append(skel)
# showMultiplePlots(testSkeletons, "Skeletonized testframes")


def fit_spline_to_contour(contour, N=10000, sampling=20, max_dist=600):
    """ fits spline to contour
    Args:
        contour (2xN): list of points of skeleton
        N (int, optional): Number of sub-sampling steps after interpolation. Defaults to 10000.
        sampling (int, optional): Number of sub-sampling steps for interpolation. Defaults to 20.
    Returns:
        array: contains interpolated x,y, derivative x and y and 2nd derivatives.
    """
    contour = np.asarray(contour)
    shape = np.shape(contour)
    if shape[1] < shape[0]:
        contour = contour.T
    # get the cumulative distance along the contour
    dist = np.sqrt((contour[0, :-1] - contour[0, 1:]) **
                   2 + (contour[1, :-1] - contour[1, 1:])**2)
    dist_along = np.concatenate(([0], dist.cumsum()))
    dist_along = dist_along[:np.min([int(max_dist), len(dist_along)])]
    # build a spline representation of the contour
    interval = np.linspace(0, len(dist_along)-1, sampling, dtype='int')
    spline, u = scp.interpolate.splprep(
        contour[:, interval], u=dist_along[interval], s=3, k=4)
    if N == 0:
        N = len(dist_along)
    # resample it at smaller distance intervals
    interp_d = np.linspace(dist_along[0], dist_along[-1], N)
    interp_y, interp_x = scp.interpolate.splev(interp_d, spline)
    deriv_y, deriv_x = scp.interpolate.splev(
        interp_d, spline, der=1)  # first derivative
    dd_y, dd_x = scp.interpolate.splev(interp_d, spline, der=2)
    return np.asarray([interp_x, interp_y, deriv_x, deriv_y, dd_x, dd_y])


N = 100
sampling = 20

testContours = []
plt.figure(dpi=300)
for skel in testSkeletons:
    plt.imshow(skel)
    sort_list = sort_skel(skel, xClamp, yClamp, max_dist=20)
    contour = fit_spline_to_contour(
        sort_list, N=N, sampling=sampling, max_dist=2000)
    plt.plot(contour[0, :], contour[1, :])
    testContours.append(contour)
plt.show()

plt.figure(figsize=(20, 20))
# plt.suptitle("Contours of testframes")
# plt.scatter(point[1],points[0],s=2, color = 'yellow', label = 'skeleton')
# plt.imshow(croppedFrames[testnum], cmap = 'gray')

for i in np.arange(0, nTestframes):
    contour = testContours[i]
    plt.subplot(3, 3, i+1)
    plt.imshow(croppedTestFrames2[i], cmap='gray')
    plt.scatter(contour[0, :], contour[1, :], c="red", label='contour', s=1)
    plt.title("Frame number : " + str(testFrameNums[i]))
    i += 1
    plt.scatter(xClamp, yClamp,  s=20, color='red', label='Clamping point')
plt.legend()
plt.show()

# %%
"""
#Section 2: Short section to replot the nodal locations of the sample frames with
#           their exact curvature values using the classic curvature equation:
#
#                np.abs(d2x_dt2 * dy_dt - dx_dt * d2y_dt2) / (dx_dt * dx_dt + dy_dt * dy_dt)**1.5
#
##https://stackoverflow.com/questions/28269379/curve-curvature-in-numpy
"""

nTestframes = 9
plt.figure(figsize=(11, 11), dpi=400)
for i in np.arange(0, nTestframes):
    contour = testContours[i]

    dx_dt = np.gradient(contour[0, :])
    dy_dt = np.gradient(contour[1, :])
    velocity = np.array([[dx_dt[i], dy_dt[i]] for i in range(dx_dt.size)])
    ds_dt = np.sqrt(dx_dt * dx_dt + dy_dt * dy_dt)
    tangent = np.array([1/ds_dt] * 2).transpose() * velocity

    tangent_x = tangent[:, 0]
    tangent_y = tangent[:, 1]

    deriv_tangent_x = np.gradient(tangent_x)
    deriv_tangent_y = np.gradient(tangent_y)

    dT_dt = np.array([[deriv_tangent_x[i], deriv_tangent_y[i]]
                     for i in range(deriv_tangent_x.size)])

    length_dT_dt = np.sqrt(
        deriv_tangent_x * deriv_tangent_x + deriv_tangent_y * deriv_tangent_y)

    normal = np.array([1/length_dT_dt] * 2).transpose() * dT_dt

    d2s_dt2 = np.gradient(ds_dt)
    d2x_dt2 = np.gradient(dx_dt)
    d2y_dt2 = np.gradient(dy_dt)

    curvature = np.abs(d2x_dt2 * dy_dt - dx_dt * d2y_dt2) / \
        (dx_dt * dx_dt + dy_dt * dy_dt)**1.5
    t_component = np.array([d2s_dt2] * 2).transpose()
    n_component = np.array([curvature * ds_dt * ds_dt] * 2).transpose()

    acceleration = t_component * tangent + n_component * normal

    plt.subplot(3, 3, i+1)
    plt.imshow(croppedTestFrames2[i], cmap='gray')
    plt.scatter(contour[0, :], contour[1, :],
                c=curvature, label='Curvature', s=1)
    plt.title("Frame number : " + str(testFrameNums[i]))
    i += 1
    plt.scatter(xClamp, yClamp,  s=20, color='red', label='Clamping point')
plt.legend()
plt.show()


# %%
"""
#Section 3: Here we subdivide all frames into equidistant spacings from all test frames.
#           This takes some time to process because each frame is analyzed and fit with 
#           skeletonization and applied curvature calculations. The resulting plot displayed 
#           in this section contains the approximated maximum curvature (calculated mean of top 20%
#           but I tested several others that are commented out) over time.

#           In general the curves regardless of the mean values of top 5,10,20 each has 
#           similar maximum caps at full inflation however the lower percent such as 5 has
#           more noise at full actuation. The recovered state is more realistice with lower
#           percents but by a marginal amount. The smoothing is necessary to eliminate the
#           large spikes in curvature.
"""
testFrameNums = []
testFrames = []


nTestframes = 1000

# Opening a set amount of testframes
for i in np.arange(0, nTestframes):
    frameNum = round(((nFrames-2)/nTestframes)*i + 1)
    testFrameNums.append(frameNum)
    testFrames.append(openFrame(frameNum))
# showMultiplePlots(testFrames, "Testframes unedited")


# Specify cropping area
ycropmin = 0
ycropmax = -1
xcropmin = 0
xcropmax = 1500

# Apply cropping to testframes
croppedTestFrames = []
testContours = []
tick = 0
for frame in testFrames:
    testframe = cropFrame(frame.copy(), xcropmin, xcropmax, ycropmin, ycropmax)
    frame = testframe

    colorChannel = 2
    test = frame.copy()
    croppedTestFrames2 = test[:, :, colorChannel]
    test = croppedTestFrames2.copy()
    binaryTestFrames = binarization(test)

    branchTresh = 50
    frame = binaryTestFrames.copy()

    skel = extract_skeleton(frame, method='skeletonize',
                            branch_thresh=branchTresh, extract=1)

    N = 100
    sampling = 20
    sort_list = sort_skel(skel, xClamp, yClamp, max_dist=20)
    contour = fit_spline_to_contour(
        sort_list, N=N, sampling=sampling, max_dist=2000)
    testContours.append(contour)

    print(tick)
    tick = tick+1


def remove_outliers_and_calculate_mean(data, threshold=2):
    # Calculate the mean and standard deviation of the data
    data_mean = np.mean(data)
    data_std = np.std(data)

    # Define a criteria for identifying outliers
    lower_bound = data_mean - threshold * data_std
    upper_bound = data_mean + threshold * data_std

    # Filter out the outliers
    filtered_data = [x for x in data if lower_bound <= x <= upper_bound]

    # Calculate the mean of the filtered data
    mean_without_outliers = np.mean(filtered_data)

    return mean_without_outliers


def remove_outliers(data, threshold=2):
    # Calculate the mean and standard deviation of the data
    data_mean = np.mean(data)
    data_std = np.std(data)

    # Define a criteria for identifying outliers
    lower_bound = data_mean - threshold * data_std
    upper_bound = data_mean + threshold * data_std

    # Filter out the outliers
    filtered_data = [x for x in data if lower_bound <= x <= upper_bound]

    return filtered_data


def average_top_5_percent(arr):
    # Sort the array in descending order
    sorted_arr = sorted(arr, reverse=True)

    # Calculate the index representing the top 10 percent
    top_5_percent_index = int(len(sorted_arr) * 0.05)

    # Take the slice containing the top 10 percent elements
    top_5_percent_slice = sorted_arr[:top_5_percent_index]

    # Calculate the average of the elements in the slice
    average_top_5_percent = sum(top_5_percent_slice) / len(top_5_percent_slice)
    # average_top_5_percent =remove_outliers_and_calculate_mean(sorted_arr[:top_5_percent_index])
    return average_top_5_percent


def average_top_10_percent(arr):
    # Sort the array in descending order
    sorted_arr = sorted(arr, reverse=True)

    # Calculate the index representing the top 10 percent
    top_10_percent_index = int(len(sorted_arr) * 0.1)

    # Take the slice containing the top 10 percent elements
    top_10_percent_slice = sorted_arr[:top_10_percent_index]

    # Calculate the average of the elements in the slice
    average_top_10_percent = sum(
        top_10_percent_slice) / len(top_10_percent_slice)
    # average_top_10_percent =remove_outliers_and_calculate_mean(sorted_arr[:top_10_percent_index])

    return average_top_10_percent


def average_top_20_percent(arr):
    # Sort the array in descending order
    sorted_arr = sorted(arr, reverse=True)

    # Calculate the index representing the top 20 percent
    top_20_percent_index = int(len(sorted_arr) * 0.2)

    # Take the slice containing the top 20 percent elements
    top_20_percent_slice = sorted_arr[:top_20_percent_index]

    # Calculate the average of the elements in the slice
    average_top_20_percent = sum(
        top_20_percent_slice) / len(top_20_percent_slice)
    # average_top_20_percent =remove_outliers_and_calculate_mean(sorted_arr[:top_20_percent_index])

    return average_top_20_percent


plt.figure(figsize=(11, 11))
addcurvemean = []
all_curvatures = []
addcurvemean_top5pct = []
addcurvemean_top10pct = []
addcurvemean_top20pct = []
for i in np.arange(0, nTestframes):
    contour = testContours[i]

    dx_dt = np.gradient(contour[0, :])
    dy_dt = np.gradient(contour[1, :])
    velocity = np.array([[dx_dt[i], dy_dt[i]] for i in range(dx_dt.size)])
    ds_dt = np.sqrt(dx_dt * dx_dt + dy_dt * dy_dt)
    tangent = np.array([1/ds_dt] * 2).transpose() * velocity

    tangent_x = tangent[:, 0]
    tangent_y = tangent[:, 1]

    deriv_tangent_x = np.gradient(tangent_x)
    deriv_tangent_y = np.gradient(tangent_y)

    dT_dt = np.array([[deriv_tangent_x[i], deriv_tangent_y[i]]
                     for i in range(deriv_tangent_x.size)])

    length_dT_dt = np.sqrt(
        deriv_tangent_x * deriv_tangent_x + deriv_tangent_y * deriv_tangent_y)

    normal = np.array([1/length_dT_dt] * 2).transpose() * dT_dt

    d2s_dt2 = np.gradient(ds_dt)
    d2x_dt2 = np.gradient(dx_dt)
    d2y_dt2 = np.gradient(dy_dt)

    curvature = np.abs(d2x_dt2 * dy_dt - dx_dt * d2y_dt2) / \
        (dx_dt * dx_dt + dy_dt * dy_dt)**1.5

    remove_outliers_and_calculate_mean

    addcurvemean.append(np.mean(curvature))
    # addcurvemean_top5pct.append(average_top_5_percent(curvature))
    # addcurvemean_top10pct.append(average_top_10_percent(curvature))
    # addcurvemean_top20pct.append(average_top_20_percent(curvature))
    all_curvatures.append(curvature)
    addcurvemean.append(remove_outliers_and_calculate_mean(curvature))
    # addcurvemean_top5pct.append(average_top_5_percent(curvature))
    # addcurvemean_top10pct.append(average_top_10_percent(curvature))
    addcurvemean_top20pct.append(average_top_20_percent(curvature))

plt.plot(addcurvemean, color='red')
# plt.plot(addcurvemean_top5pct, color = 'green')
# plt.plot(addcurvemean_top10pct, color = 'blue')
plt.plot(addcurvemean_top20pct, color='orange')
plt.ylim([0, 0.05])
plt.legend()
plt.show()


plt.figure(figsize=(6, 6), dpi=300)
# plt.plot(addcurvemean_top20pct, color = 'green')

plt.plot(scp.signal.savgol_filter(
    addcurvemean_top20pct, 20, 5), color='purple')


csfont = {'fontname': 'Arial'}
hfont = {'fontname': 'Arial'}
plt.rcParams["font.family"] = "Arial"
plt.ylim([0, 0.06])
plt.title("Curvature Tracking Over Time", **csfont)
plt.legend()
plt.show()


# %%
"""
#Section 4: This section plots the full curvature profile along a filament for 
#           specified time scales (in this case every 100images which can extrapolate
#           timesteps given fps is provided). Each set of 100 images coincides 
#           with testing at exact empirical pressure values
"""


def LINES_MultiplePlots(all_curvatures, title, time_separation):
    c1 = 'red'  # blue
    c2 = 'blue'  # green

    plt.figure(figsize=(12, 12), dpi=300)
    plt.suptitle(str(title))
    for j in range(0, 9):
        plt.subplot(3, 3, j+1)
        for i in np.arange(time_separation*j, time_separation*(j+1)):
            n = time_separation*(j+1)
            plt.plot(all_curvatures[i][:-3], color=colorFader(c1, c2, i/n))
            # plt.title("Frame number : " + str(testFrameNums[i]))
            plt.ylim([0, 0.02])


testFrameNums = []
testFrames = []
nTestframes = 9


plt.figure(figsize=(6, 6), dpi=300)


def colorFader(c1, c2, mix=0):  # fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1 = np.array(mpl.colors.to_rgb(c1))
    c2 = np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)


s = 0
n = 100
c1 = 'red'  # blue
c2 = 'blue'  # green
for i in range(s, n):
    if i > s and i < n:
        plt.plot(all_curvatures[i][:-3], color=colorFader(c1, c2, i/n))
        plt.ylim([0, 0.02])
plt.show()

LINES_MultiplePlots(
    all_curvatures, "Full Curvature Profiles Different Pressures (1psi-9psi)", 100)
