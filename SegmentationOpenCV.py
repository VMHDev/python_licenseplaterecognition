import numpy as np
import cv2
from OpenCV.UtilitiesOpenCV import UtilitiesOpenCV

def sort_contours(character_contours):
    """
    Sắp xếp các contours từ trái sang phải
    """
    reverse = False
    i = 0
    boundingBoxes = [cv2.boundingRect(c) for c in character_contours]
    (character_contours, boundingBoxes) = zip(*sorted(zip(character_contours, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    return character_contours

def segment_characters_from_plate(_ImageInput, _RatioMin = 1.5, _RatioMax = 7.5, _CropPadding = 2):
    """
    Tách các ký tự ra khỏi biển số
    ...
    Parameters
        ----------
        _ImgInput : Hình ảnh biển số
        _RatioMin: Tỷ lệ nhỏ nhất
        _RatioMax: Tỷ lệ lớn nhất
        ----------
    Returns
        ----------
        Danh sách các ký tự của biển số
        ----------
    """
    img_data = _ImageInput.copy()
    # Segment kí tự
    kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thre_mor = cv2.morphologyEx(img_data, cv2.MORPH_DILATE, kernel3)
    lstContours, _  = cv2.findContours(thre_mor, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    characters =[]
    img_draw = cv2.cvtColor(_ImageInput, cv2.COLOR_GRAY2BGR)
    for item in sort_contours(lstContours):
        (x, y, w, h) = cv2.boundingRect(item)
        ratio = h/w
        if _RatioMin <= ratio <= _RatioMax: # Chọn các contour đảm bảo về tỷ lệ weight/height
            if h/_ImageInput.shape[0]>=0.6: # Chọn các contour cao từ 60% biển số trở lên
                xB = x-_CropPadding
                xE = x+w+_CropPadding
                yB = y-_CropPadding
                yE = y+h+_CropPadding

                if(xB < 0): xB = x
                if(yB < 0): yB = y

                # Vẽ khung chữ nhật cho các ký tự segment được
                cv2.rectangle(img_draw, (xB , yB), (xE , yE), (0, 255, 0), 2)
                # Tách các số ra khỏi biển số
                curr_num = thre_mor[yB : yE , xB : xE]

                characters.append(curr_num)     
    return characters, img_draw


class SegmentationOpenCV():
    '''
    Class tách ký tự ra khỏi biển số sử dụng OpenCV
    ...
    Attributes
    ----------
        _TypePlate: Loại biển số (0: Biển dài | 1: Biển ngắn)
        _HeightRatioMin: Tỷ lệ nhỏ nhất
        _HeightRatioMax: Tỷ lệ lớn nhất
    Methods
    ----------
        segmentation(_ImgInput): Tách ký tự ra khỏi biển số
    '''
    def __init__(self, _TypePlate = 0, _SizeWidth = 0, _SizeHeight = 0, _Border = 0, 
                       _Threshold = 0, _CropPadding = 2, _RatioMin = 1.5, _RatioMax = 7.5, _GaussFilter = 3, _BilaFilter = 0):
        self.typePlate = _TypePlate
        self.sizeWidth = _SizeWidth
        self.sizeHeight = _SizeHeight
        self.border = _Border
        self.threshold = _Threshold
        self.cropPadding = _CropPadding
        self.ratioMin = _RatioMin
        self.ratioMax = _RatioMax
        self.gaussFilter = _GaussFilter
        self.bilaFilter= _BilaFilter

    def segmentation(self, _ImgInput):
        '''
            Tách các ký tự ra khỏi biển số
            ...
            Parameters
                ----------
                _ImgInput : Hình ảnh biển số
                ----------
            Returns
                ----------
                Danh sách các ký tự của biển số
                ----------
        '''
        charactersFound = []
        imgDraw = np.array([])
        imgBinary = np.array([])
        # Tiến hành tiền xử lý ảnh
          # Chuyển ảnh biển số về ảnh xám
        img_gray = cv2.cvtColor(_ImgInput, cv2.COLOR_BGR2GRAY)
          # Lọc ảnh:
        img_filter = img_gray.copy()
        if self.gaussFilter != 0:
            img_filter = cv2.GaussianBlur(img_gray, (self.gaussFilter, self.gaussFilter), 1)
        if self.bilaFilter != 0:
            img_filter = cv2.bilateralFilter(img_gray, self.bilaFilter, 75, 75)
          # Phân ngưỡng
        img_binary =  cv2.threshold(img_filter, self.threshold, 255, cv2.THRESH_BINARY_INV +  cv2.THRESH_OTSU)[1]        

        # Tiến hành tách ký tự
        plate = img_binary.copy()
        if (self.typePlate == 0):  # Xử lý biển số dài
            charactersFound, imgDraw = segment_characters_from_plate(_ImageInput = plate,
                                                                                _RatioMin = self.ratioMin,
                                                                                _RatioMax = self.ratioMax, 
                                                                                _CropPadding = self.cropPadding)
            return charactersFound, imgDraw, img_binary

        if (self.typePlate == 1):  # Xử lý biển số ngắn
            upper_charactersFound = []
            lower_charactersFound = []
            imgDrawUp = np.array([])
            imgDrawLow = np.array([])

            # Chia biển số thành hai phần trên dưới và tùy chỉnh kích thước
            utilitiesOpenCV = UtilitiesOpenCV()
            plate_upper = plate[0:int(plate.shape[0]/2), 0:plate.shape[1]]
            plate_lower = plate[int(plate.shape[0]/2): plate.shape[0], 0:plate.shape[1]]

            img_resize_upper = plate_upper.copy()
            img_resize_lower = plate_lower.copy()

            if self.sizeHeight != 0: 
                img_resize_upper = utilitiesOpenCV.resize_height(_ImgInput = img_resize_upper, _SizeHeight = self.sizeHeight)
                img_resize_lower = utilitiesOpenCV.resize_height(_ImgInput = img_resize_lower, _SizeHeight = self.sizeHeight)
            if self.sizeWidth != 0:
                img_resize_upper = utilitiesOpenCV.resize_width(_ImgInput = img_resize_upper, _SizeWidth = self.sizeWidth)
                img_resize_lower = utilitiesOpenCV.resize_width(_ImgInput = img_resize_lower, _SizeWidth = self.sizeWidth)
            if self.border != 0:
                img_resize_upper = cv2.copyMakeBorder(
                    img_resize_upper,
                    top = self.border,
                    bottom = self.border,
                    left = self.border,
                    right = self.border,
                    borderType = cv2.BORDER_REPLICATE
                )
                img_resize_lower = cv2.copyMakeBorder(
                    img_resize_lower,
                    top = self.border,
                    bottom = self.border,
                    left = self.border,
                    right = self.border,
                    borderType = cv2.BORDER_REPLICATE
                )

            # Lấy các ký tự của phần trên và phần dưới
            upper_charactersFound, imgDrawUp = segment_characters_from_plate(_ImageInput = img_resize_upper,
                                                                        _RatioMin = self.ratioMin,
                                                                        _RatioMax = self.ratioMax,
                                                                        _CropPadding = self.cropPadding)
            lower_charactersFound, imgDrawLow = segment_characters_from_plate(_ImageInput = img_resize_lower,
                                                                        _RatioMin = self.ratioMin,
                                                                        _RatioMax = self.ratioMax,
                                                                        _CropPadding = self.cropPadding)

            if (len(upper_charactersFound) > 0 and len(lower_charactersFound) > 0):
                charactersFound = upper_charactersFound + lower_charactersFound
                imgDraw = np.concatenate((imgDrawUp, imgDrawLow), axis=0)
            return charactersFound, imgDraw, img_binary
        return charactersFound, imgDraw, img_binary