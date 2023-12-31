import os
import cv2
import shutil
import hydra
from omegaconf import DictConfig
from pathlib import Path
from pycocotools.coco import COCO

VAL_NB = TEST_NB = 300

def cocobox2yolo(img_path, coco_box):
	I = cv2.imread(img_path)
	Image_hight, Image_width = I.shape[0:2]

	[left, top, box_width, box_hight] = coco_box
	x_center = (left + box_width / 2) / Image_width
	y_center = (top + box_hight / 2) / Image_hight

	box_width /= Image_width
	box_hight /= Image_hight
	Yolobbx = [x_center, y_center, box_width, box_hight]

	return Yolobbx


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
	dataset_folder = 'coco'
	coco_version = 'train2017'

	data_path = cfg['data_path']
	REAL_DATA_PATH = Path(data_path['base']) / data_path['real']
	DATASETS_DATA_PATH = Path(data_path['datasets'])

	# Specify the results path
	(REAL_DATA_PATH).mkdir(parents=True, exist_ok=True)
	
	real_data_images = REAL_DATA_PATH / 'images'
	real_data_labels = REAL_DATA_PATH / 'labels'
	real_data_captions = REAL_DATA_PATH / 'captions'
	
	(real_data_images).mkdir(parents=True, exist_ok=True)
	(real_data_labels).mkdir(parents=True, exist_ok=True)
	(real_data_captions).mkdir(parents=True, exist_ok=True)

	(DATASETS_DATA_PATH).mkdir(parents=True, exist_ok=True)
	coco_path = DATASETS_DATA_PATH / dataset_folder / 'Coco_1FullPerson'
	coco_bbx_path = DATASETS_DATA_PATH / dataset_folder / 'Coco_1FullPerson_bbx'
	coco_caps_path = DATASETS_DATA_PATH / dataset_folder / 'Coco_1FullPerson_caps'

	coco_annotations_path = DATASETS_DATA_PATH / dataset_folder / 'annotations'

	annFile = coco_annotations_path / f'instances_{coco_version}.json'
	annFile_keypoints = coco_annotations_path / f'person_keypoints_{coco_version}.json'
	annFile_captions = coco_annotations_path / f'captions_{coco_version}.json'

	coco = COCO(annFile.absolute())
	coco_keypoints = COCO(annFile_keypoints.absolute())
	coco_captions = COCO(annFile_captions.absolute())

	catIds = coco.getCatIds(catNms=['person'])

	all_images = list(coco_path.glob('*.jpg'))

	for img_path in all_images:
		img_path = str(img_path.absolute())
		img_id = int(img_path.split('/')[-1].split('.jpg')[0])
		Keypoints_annIds = coco_keypoints.getAnnIds(imgIds = img_id, catIds = catIds, iscrowd = None)
		Keypoints_anns = coco_keypoints.loadAnns(Keypoints_annIds)

		caps_annIds = coco_captions.getAnnIds(imgIds = img_id);
		caps_anns = coco_captions.loadAnns(caps_annIds)

		bbox_text_path = img_path.replace('.jpg', '.txt').replace('Coco_1FullPerson','Coco_1FullPerson_bbx')
		bbox_text_path = Path(bbox_text_path)

		captions_text_path = img_path.replace('.jpg', '.txt').replace('Coco_1FullPerson','Coco_1FullPerson_caps')
		captions_text_path = Path(captions_text_path)

		with open(bbox_text_path, 'w') as file:
			coco_box = Keypoints_anns[0]['bbox']
			Yolo_bbx = cocobox2yolo(img_path,coco_box)
			KP_Yolo_format = '0 '+' '.join(list(map(str, Yolo_bbx)))
			file.write(KP_Yolo_format)

		with open(captions_text_path, 'w') as file:
			captions = [caps['caption'] for caps in caps_anns]
			file.write('\n'.join(captions))

	# move all files
	counter = 0
	for file_name in os.listdir(coco_path):
		counter += 1
		
		name =  file_name.split('.')[0]
		img_file = name + '.jpg'
		txt_file = name + '.txt'
		
		image = coco_path / img_file
		label = coco_bbx_path / txt_file
		caption = coco_caps_path / txt_file

		if os.path.isfile(image) and os.path.isfile(label) and os.path.isfile(caption):
			if counter < VAL_NB:
				images_dir = Path(str(real_data_images).replace('/real/', '/val/'))
				labels_dir = Path(str(real_data_labels).replace('/real/', '/val/'))
				test_dir = Path(str(real_data_captions).replace('/real/', '/val/'))
			elif counter < VAL_NB + TEST_NB:
				images_dir = Path(str(real_data_images).replace('/real/', '/test/'))
				labels_dir = Path(str(real_data_labels).replace('/real/', '/test/'))
				test_dir = Path(str(real_data_captions).replace('/real/', '/test/'))
			else:
				images_dir = real_data_images
				labels_dir = real_data_labels
				test_dir = real_data_captions

			(images_dir).mkdir(parents=True, exist_ok=True)
			(labels_dir).mkdir(parents=True, exist_ok=True)
			(test_dir).mkdir(parents=True, exist_ok=True)

			shutil.copy(image, images_dir / img_file)
			shutil.copy(label, labels_dir / txt_file)
			shutil.copy(caption, test_dir / txt_file)

if __name__ == "__main__":
   main()
