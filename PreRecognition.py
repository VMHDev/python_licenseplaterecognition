import cv2
import numpy as np
from OpenCV.DetectionOpenCV import DetectionOpenCV
from OpenCV.SegmentationOpenCV import SegmentationOpenCV
from OpenCV.UtilitiesOpenCV import UtilitiesOpenCV
from YOLO.DetectionYOLO import DetectionYOLO
from WPODNET.DetectionWPODNET import DetectionWPODNET
from Skimage.SegmentationSkimage import SegmentationSkimage

class PreRecognition():
    def __init__(self, _TypePlate = 0):
        self.typePlate = _TypePlate                 # Loại biển số
    
    def detection(self, _ImgInput, _TypeDetection = 2, _Object = None):
        """
        Hàm phát hiện biển số trong ảnh
        ...
        Parameters
            ----------
            _ImgInput : Hình ảnh biển số
            _TypeDetection: Phương pháp phát hiện (0: OpenCV | 1: YOLO | 2: WPODNET)
            _Object: Lớp dữ liệu phương pháp tách biển
            ----------
        Returns
            ----------
            Hình ảnh biển số phát hiện được
            ----------
        """        
        img_vehicle = _ImgInput.copy()
        img_plate = np.array([])
        if _Object == None:
            return 0, img_plate

        if _TypeDetection == 0:         # Sử dụng OpenCV
            detectionOpenCV = DetectionOpenCV()
            detectionOpenCV.sizeMax = _Object.sizeMax
            detectionOpenCV.sizeMin = _Object.sizeMin
            detectionOpenCV.resizeWidth = _Object.resizeWidth
            detectionOpenCV.resizeHeight = _Object.resizeHeight
            detectionOpenCV.cannyThreshold1 = _Object.cannyThreshold1
            detectionOpenCV.cannyThreshold2 = _Object.cannyThreshold2
            return detectionOpenCV.detection(img_vehicle)

        elif _TypeDetection == 1:       # Sử dụng YOLO
            detectionYOLO = DetectionYOLO()
            detectionYOLO.config = _Object.config
            detectionYOLO.weights = _Object.weights
            detectionYOLO.classes = _Object.classes
            detectionYOLO.scale = _Object.scale
            return detectionYOLO.detection(img_vehicle)

        elif _TypeDetection == 2:       # Sử dụng WPODNET
            detectionWPODNET = DetectionWPODNET()
            detectionWPODNET.modelWPODNET = _Object.modelWPODNET
            detectionWPODNET.sizeMax = _Object.sizeMax
            detectionWPODNET.sizeMin = _Object.sizeMin
            detectionWPODNET.threshold = _Object.threshold
            return detectionWPODNET.detection(img_vehicle)

        else:
            return 0, img_plate

    def segmentation(self, _ImgInput, _TypeSegmentation = 1, _Object = None):
        """
        Hàm tách ký tự ra khỏi biển số
        ...
        Parameters
            ----------
            _ImgInput : Hình ảnh biển số
            _TypeSegmentation: Phương pháp tách biển (0: Sử dụng Skimage | 1: Sử dụng OpenCV)
            _Object: Lớp dữ liệu phương pháp tách biển
            ----------
        Returns
            ----------
            Trạng thái: 1 - Thành công | 0 - Thất bại
            Danh sách các ký tự tách được
            Hình ảnh biển số được Contours
            ----------
        """
        img_plate = _ImgInput.copy()
        lst_char = []
        img_contour = np.array([])
        img_binary = np.array([])
        if _Object == None:
            return 0, lst_char, img_contour, img_binary

        if _TypeSegmentation == 0:         # Sử dụng Skimage
            segmentationSkimage = SegmentationSkimage()
            segmentationSkimage.typePlate = _Object.typePlate
            segmentationSkimage.fixedWidth = _Object.fixedWidth       # (Biển dài = 470 | Biển ngắn = 280)
            segmentationSkimage.fixedAspectRatio = _Object.fixedAspectRatio
            segmentationSkimage.fixedSolidityRatio = _Object.fixedSolidityRatio
            segmentationSkimage.fixedWidthChar = _Object.fixedWidthChar
            segmentationSkimage.heightRatioMin = _Object.heightRatioMin
            segmentationSkimage.heightRatioMax = _Object.heightRatioMax
            lst_char, img_contour, img_binary = segmentationSkimage.segmentation(img_plate)
            return 1, lst_char, img_contour, img_binary

        elif _TypeSegmentation == 1:       # Sử dụng OpenCV
            segmentationOpenCV = SegmentationOpenCV()
            segmentationOpenCV.typePlate = _Object.typePlate
            segmentationOpenCV.sizeWidth = _Object.sizeWidth
            segmentationOpenCV.sizeHeight = _Object.sizeHeight
            segmentationOpenCV.border = _Object.border
            segmentationOpenCV.threshold = _Object.threshold
            segmentationOpenCV.cropPadding = _Object.cropPadding
            segmentationOpenCV.ratioMin = _Object.ratioMin
            segmentationOpenCV.ratioMax = _Object.ratioMax
            segmentationOpenCV.gaussFilter = _Object.gaussFilter
            segmentationOpenCV.bilaFilter= _Object.bilaFilter

            lst_char, img_contour, img_binary = segmentationOpenCV.segmentation(img_plate)            
            return 1, lst_char, img_contour, img_binary
        else:
            return 0, lst_char, img_contour, img_binary
    def __init__(self, _TypePlate = 0):
        self.typePlate = _TypePlate                 # Loại biển số
    
    def detection(self, _ImgInput, _TypeDetection = 2, _Object = None):
        """
        Hàm phát hiện biển số trong ảnh
        ...
        Parameters
            ----------
            _ImgInput : Hình ảnh biển số
            _TypeDetection: Phương pháp phát hiện (0: OpenCV | 1: YOLO | 2: WPODNET)
            _Object: Lớp dữ liệu phương pháp tách biển
            ----------
        Returns
            ----------
            Hình ảnh biển số phát hiện được
            ----------
        """        
        img_vehicle = _ImgInput.copy()
        img_plate = np.array([])
        if _Object == None:
            return 0, img_plate

        if _TypeDetection == 0:         # Sử dụng OpenCV
            detectionOpenCV = DetectionOpenCV()
            detectionOpenCV.sizeMax = _Object.sizeMax
            detectionOpenCV.sizeMin = _Object.sizeMin
            detectionOpenCV.resizeWidth = _Object.resizeWidth
            detectionOpenCV.resizeHeight = _Object.resizeHeight
            detectionOpenCV.cannyThreshold1 = _Object.cannyThreshold1
            detectionOpenCV.cannyThreshold2 = _Object.cannyThreshold2
            return detectionOpenCV.detection(img_vehicle)

        elif _TypeDetection == 1:       # Sử dụng YOLO
            detectionYOLO = DetectionYOLO()
            detectionYOLO.config = _Object.config
            detectionYOLO.weights = _Object.weights
            detectionYOLO.classes = _Object.classes
            detectionYOLO.scale = _Object.scale
            return detectionYOLO.detection(img_vehicle)

        elif _TypeDetection == 2:       # Sử dụng WPODNET
            detectionWPODNET = DetectionWPODNET()
            detectionWPODNET.modelWPODNET = _Object.modelWPODNET
            detectionWPODNET.sizeMax = _Object.sizeMax
            detectionWPODNET.sizeMin = _Object.sizeMin
            detectionWPODNET.threshold = _Object.threshold
            return detectionWPODNET.detection(img_vehicle)

        else:
            return 0, img_plate

    def segmentation(self, _ImgInput, _TypeSegmentation = 1, _Object = None):
        """
        Hàm tách ký tự ra khỏi biển số
        ...
        Parameters
            ----------
            _ImgInput : Hình ảnh biển số
            _TypeSegmentation: Phương pháp tách biển (0: Sử dụng Skimage | 1: Sử dụng OpenCV)
            _Object: Lớp dữ liệu phương pháp tách biển
            ----------
        Returns
            ----------
            Trạng thái: 1 - Thành công | 0 - Thất bại
            Danh sách các ký tự tách được
            Hình ảnh biển số được Contours
            ----------
        """
        img_vehicle = _ImgInput.copy()
        lst_char = []
        img_contour = np.array([])
        img_binary = np.array([])
        if _Object == None:
            return 0, lst_char, img_contour, img_binary

        if _TypeSegmentation == 0:         # Sử dụng Skimage
            segmentationSkimage = SegmentationSkimage()
            segmentationSkimage.typePlate = _Object.typePlate
            segmentationSkimage.fixedWidth = _Object.fixedWidth       # (Biển dài = 470 | Biển ngắn = 280)
            segmentationSkimage.fixedAspectRatio = _Object.fixedAspectRatio
            segmentationSkimage.fixedSolidityRatio = _Object.fixedSolidityRatio
            segmentationSkimage.fixedWidthChar = _Object.fixedWidthChar
            segmentationSkimage.heightRatioMin = _Object.heightRatioMin
            segmentationSkimage.heightRatioMax = _Object.heightRatioMax
            lst_char, img_contour, img_binary = segmentationSkimage.segmentation(img_vehicle)
            return 1, lst_char, img_contour, img_binary

        elif _TypeSegmentation == 1:       # Sử dụng OpenCV
            segmentationOpenCV = SegmentationOpenCV()
            segmentationOpenCV.typePlate = _Object.typePlate
            segmentationOpenCV.sizeWidth = _Object.sizeWidth
            segmentationOpenCV.sizeHeight = _Object.sizeHeight
            segmentationOpenCV.border = _Object.border
            segmentationOpenCV.threshold = _Object.threshold
            segmentationOpenCV.cropPadding = _Object.cropPadding
            segmentationOpenCV.ratioMin = _Object.ratioMin
            segmentationOpenCV.ratioMax = _Object.ratioMax
            segmentationOpenCV.gaussFilter = _Object.gaussFilter
            segmentationOpenCV.bilaFilter= _Object.bilaFilter

            lst_char, img_contour, img_binary = segmentationOpenCV.segmentation(img_vehicle)            
            return 1, lst_char, img_contour, img_binary
        else:
            return 0, lst_char, img_contour, img_binary