import os
import glob
import shutil
import xml.etree.ElementTree as ET

def get_class_id(name):
    class_dict = {
        'crazing': 0,
        'inclusion': 1,
        'patches': 2,
        'pitted_surface': 3,
        'rolled-in_scale': 4,
        'scratches': 5
    }

    return class_dict.get(name)

def xml_to_yolo(dataset_path = "NEU-DET", image_width=200, image_height=200):
    """ Function that converts the annotations in xml format (PASCAL VOC) to YOLO """

    annotations_path = os.path.join(dataset_path, "all", "annotations")
    labels_path = os.path.join(dataset_path, "all", "labels")

    if not os.path.isdir(annotations_path):
        print("Xml annotations path does not exist")
        exit(-1)

    if not os.path.isdir(labels_path):
        print("Txt labels path does not exist")
        exit(-1)
   
    for file in glob.glob(os.path.join(annotations_path, '*')):
        new_file = file.replace(annotations_path, labels_path).replace('.xml', '.txt')

        tree = ET.parse(file)
        root = tree.getroot()
    
        for obj in root.findall('object'):
            name = obj.find('name').text
            bndbox = obj.find('bndbox')
            
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)

            x_center = ((xmax + xmin) / 2) / image_width
            y_center = ((ymax + ymin) / 2) / image_height
            w = (xmax - xmin) / image_width
            h = (ymax - ymin) / image_height
            class_id = get_class_id(name)
            
            with open(new_file, "a+") as f:
                f.write(f'{class_id} {x_center} {y_center} {w} {h}\n')

def split_data(dataset_path):
    if not os.path.isdir(dataset_path):
        print("Dataset path does not exist")
        exit(-1)
    
    # Create the corresponding folders: test1, test2, test3, test4, train1, train2, train3, and train4
    for i in range(1, 5):
        test_path = os.path.join(dataset_path, "test" + str(i))
        train_path = os.path.join(dataset_path, "train" + str(i))

        if not os.path.isdir(test_path):
            os.mkdir(test_path)
            os.mkdir(os.path.join(test_path, "images"))
            os.mkdir(os.path.join(test_path, "labels"))

        if not os.path.isdir(train_path):
            os.mkdir(train_path)
            os.mkdir(os.path.join(train_path, "images"))
            os.mkdir(os.path.join(train_path, "labels"))

        # Read the division given and copy the files to the corresponding folders
        with open(os.path.join("data_partition", "test" + str(i) + ".txt"), 'r') as test_file:
            test_lines = test_file.readlines()
        
        with open(os.path.join("data_partition", "train" + str(i) + ".txt"), 'r') as train_file:
            train_lines = train_file.readlines()

        for line in test_lines:
            img_file = os.path.join(dataset_path, "all", "images", line.strip())
            label_file = os.path.join(dataset_path, "all", "labels", line.strip().replace(".jpg", ".txt"))

            shutil.copy(img_file, os.path.join(test_path, "images"))
            shutil.copy(label_file, os.path.join(test_path, "labels"))

        for line in train_lines:
            img_file = os.path.join(dataset_path, "all", "images", line.strip())
            label_file = os.path.join(dataset_path, "all", "labels", line.strip().replace(".jpg", ".txt"))

            shutil.copy(img_file, os.path.join(train_path, "images"))
            shutil.copy(label_file, os.path.join(train_path, "labels"))


if __name__ == '__main__':
    dataset_path = "NEU-DET"    

    xml_to_yolo(dataset_path)
    split_data(dataset_path)