	Image detector tool, author: Liu Weizhi
1. Detect cropped images (E.g. GIJ-900 crop)
	1.1 Select checkpoint file under File menu
	1.2 Select folder containing images you want to test
	1.3 Create Tensorflow Daemon using Create damon button under Daemon menu
	1.4 (Optional) Select threshold for detecting defects, default value is 0.9, which is recommended
	1.5 Select testing mode: Observe, Continuous and Offline (not implemented)
		1.5.1 Observe mode: Observe detection result image by image, press Forward_inference to detect
		next image, and press Backward_inference to detect previous image
		1.5.2 Continous mode: Detect images without stopping untill reach the last image, press 
		Pause_inference to stop continuous testing
2. Detect original images
	2.1 Enable cropping under Crop image menu
	2.2 Choose template, default one is located ./templates/abs_template.bmp
	2.3 (Optional) Select margin
	2.4 Follow steps from 1.1 to 1.5

3. Switch image display mode
	3.1 Press <shift> button to switch display mode. There are three mode:
		3.1.1 Box mode displays the boxes labelling defects
		3.1.2 Prob mode displays boxes together with probability
		3.1.3 Ori mode only displays original image

3. Log
	All Observe mode, Continous mode and Offline mode will generate NG/OK image history after you start
	detection for the first time. So don't forget to reset the detection history if you want to save images
	labeled as NG/OK.
	3.1 Reset detetion history: clear detection history in order to save NG/OK images in the following steps
	3.2 Show images labeled as NG: store images labeled as NG
	3.3 Show images labeld as OK: store images labeled as OK
