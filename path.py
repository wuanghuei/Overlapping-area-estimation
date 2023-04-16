import os
import numpy as np


def create_scene_folders(n):
    base_dir = "MMB"
    scene = 'SCENE_' + str(n)
    # scenes.append(text)

    scene_dir = os.path.join(base_dir, scene)
    os.makedirs(scene_dir, exist_ok=True)
    return scene_dir


def create_txt(data,n):
    scene_dir = create_scene_folders(n)
    for cam in range(len(data.keys())):
        cam_file = os.path.join(scene_dir, f"CAM_{cam+1}.txt")
        with open(cam_file, "w") as f:
            for i in range(len(data[cam])):
                frame = f"frame_{i+1}.jpg"
                sorted = hull_sort(data[cam][i][0])
                flat_list = [str(num) for sublist in sorted for subsublist in sublist for num in subsublist]
                bbox = "(" + ",".join(flat_list) + ")"
                #bbox = data[cam][i][0]  # Replace with the actual bounding box coordinate           
                time_process = data[cam][i][1]  # Replace with the actual time taken to process the frame
                line = f"{frame}, {bbox}, {time_process}\n"
                f.write(line)
        
def hull_sort(hull):
    x = hull.T[0]
    x = x.tolist()[0]
    y = hull.T[1]
    y = y.tolist()[0]

    xmean = sum(x)/len(x)
    ymean = sum(y)/len(y)

    xax = [i - xmean for i in x]
    yax = [i - ymean for i in y]

    xax = np.array([xax])
    yax = np.array([yax])

    # get complex numbers

    zs = xax + 1j * yax
    verts_sorted = hull[np.angle(zs).argsort()][0]
    return verts_sorted
