import numpy as np
import cv2
import matplotlib.pyplot as plt
import time


def get_hull(img_need_aligned, img_template):
    MAX_FEATURES = 200
    im1Gray = cv2.cvtColor(img_need_aligned, cv2.COLOR_BGR2GRAY)
    im2Gray = cv2.cvtColor(img_template, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)
    
    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Use homography
    pts1 = cv2.KeyPoint_convert(keypoints1)
    listpt1 = np.int32([pts1])
    hull1 = cv2.convexHull(listpt1,False)

    return hull1 

def get_hulls(lst):
    hulls = []
    used = {}
    cams  = range(len(lst))
    for n in cams:
        used[n] = []
        for n2 in cams:
            if n != n2 and n2 not in used[n]:
                used[n].append(n2)
                if n2 in used.keys():
                    used[n2].append(n)
                else:
                    used[n2] = [n]            
        if used[n] == []:
            used[n] = 1
    for i in used.keys():
        img = lst[i]
        img2 = lst[used[i][0]]
        time_st = time.time()
        hull12 = get_hull(img,img2)
        time_et= (time.time() - time_st) / 10
        hulls.append([hull12, time_et])
    return hulls


def get_lines(hulls, lst):
    images = []
    for i in range(len(hulls)):
        images.append(cv2.polylines(lst[i], [hulls[i][0]],True, (255, 0, 0), 3))
    return images




