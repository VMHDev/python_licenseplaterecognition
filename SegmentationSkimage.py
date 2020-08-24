import cv2
import numpy as np
import imutils
from skimage.filters import threshold_local
from skimage import measure

def sort_contours_left_to_right(character_contours):
    """
    Sắp xếp các contours từ trái sang phải
    """
    i = 0
    boundingBoxes = [cv2.boundingRect(c) for c in character_contours]
    (character_contours, boundingBoxes) = zip(*sorted(zip(character_contours, boundingBoxes),
                                                key=lambda b:b[1][i], reverse=False))
    return character_contours

def segment_characters_from_plate(_ImgInput, _FixedWidth = 400, _FixedAspectRatio = 1.0,                                               
                                              _FixedSolidityRatio = 0.15, _FixedWidthChar = 14,
                                              _HeightRatioMin = 0.5, _HeightRatioMax = 0.95):
    """
    Tách các ký tự ra khỏi biển số
    ...
    Parameters
        ----------
        _ImgInput : Hình ảnh biển số
        _FixedWidth: Chiều rộng kích thước thay đổi
        _FixedSolidityRatio: Tỷ lệ khung hình
        _FixedSolidityRatio: Tỷ lệ độ dày
        _FixedWidthChar: Chiều rộng của ký tự
        _HeightRatioMin: Tỷ lệ chiều cao nhỏ nhất
        _HeightRatioMax: Tỷ lệ chiều cao nhỏ nhất
        ----------
    Returns
        ----------
        Danh sách các ký tự của biển số
        ----------
    """
    V = cv2.split(cv2.cvtColor(_ImgInput, cv2.COLOR_BGR2HSV))[2]
    T = threshold_local(V, 29, offset=15, method='gaussian')
    thresh = (V > T).astype('uint8') * 255
    thresh = cv2.bitwise_not(thresh)

    # Thay đổi kích thước biển số xe thành kích thước chuẩn
    _ImgInput = imutils.resize(_ImgInput, width = _FixedWidth)
    thresh = imutils.resize(thresh, width=_FixedWidth)
    bgr_thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    # Thực hiện phân tích các thành phần được kết nối và khởi tạo mặt nạ để lưu trữ vị trí của các ứng cử viên
    labels = measure.label(thresh, background=0)
    charCandidates = np.zeros(thresh.shape, dtype='uint8')

    # Duyệt qua các thành phần vừa phân tích
    characters = []
    for label in np.unique(labels):
        # Nếu là nền thì bỏ qua
        if label == 0:
            continue
        # Xây dựng mặt nạ để chỉ hiển thị các thành phần được kết nối cho nhãn hiện tại, sau đó tìm contour trong mặt nạ
        labelMask = np.zeros(thresh.shape, dtype='uint8')
        labelMask[labels == label] = 255
        cnts, _ = cv2.findContours(labelMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Nếu tìm thấy contour
        if len(cnts) > 0:
            # Lấy đường viền lớn nhất tương ứng với thành phần trong mặt nạ, sau đó lấy khung giới hạn cho đường viền
            c = max(cnts, key=cv2.contourArea)
            (boxX, boxY, boxW, boxH) = cv2.boundingRect(c)
            
            # Tính tỷ lệ khung hình, độ dày ký tự và tỷ lệ chiều cao cho contour
            aspectRatio = boxW / float(boxH)
            solidity = cv2.contourArea(c) / float(boxW * boxH)
            heightRatio = boxH / float(_ImgInput.shape[0])
            
            # Xác định xem tỷ lệ khung hình, độ rắn và chiều cao của đường viền có vượt quá tỷ lệ cho trước không
            keepAspectRatio = aspectRatio < _FixedAspectRatio
            keepSolidity = solidity > _FixedSolidityRatio
            keepHeight = heightRatio > _HeightRatioMin and heightRatio < _HeightRatioMax
            
            # Nếu tất cả tỷ lệ thỏa thì xét tiếp
            if keepAspectRatio and keepSolidity and keepHeight and boxW > _FixedWidthChar:
                hull = cv2.convexHull(c)
                cv2.drawContours(charCandidates, [hull], -1, 255, -1)

    contours, _ = cv2.findContours(charCandidates, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    img_draw = _ImgInput.copy()
    if contours:
        contours = sort_contours_left_to_right(contours)
        characters = []

        addPixel = 4
        for c in contours:
            (x,y,w,h) = cv2.boundingRect(c)
            if y > addPixel:
                y = y - addPixel
            else:
                y = 0
            if x > addPixel:
                x = x - addPixel
            else:
                x = 0
            img_crop = bgr_thresh[y:y+h+(addPixel*2), x:x+w+(addPixel*2)]
            gray_crop = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
            characters.append(gray_crop)
            cv2.rectangle(img_draw, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return characters, img_draw
    else:
        return None

class SegmentationSkimage():
    '''
    Class tách ký tự ra khỏi biển số sử dụng Skimage
    ...
    Attributes
    ----------
        _TypePlate: Loại biển số (0: Biển dài | 1: Biển ngắn)
        _FixedWidth: Chiều rộng kích thước thay đổi
        _FixedSolidityRatio: Tỷ lệ khung hình
        _FixedSolidityRatio: Tỷ lệ độ dày
        _FixedWidthChar: Chiều rộng của ký tự
        _HeightRatioMin: Tỷ lệ chiều cao nhỏ nhất
        _HeightRatioMax: Tỷ lệ chiều cao lớn nhất
    Methods
    ----------
        segmentation(_ImgInput): Tách ký tự ra khỏi biển số
    '''
    def __init__(self, _TypePlate = 0,  _FixedWidth = 400, _FixedAspectRatio = 1.0,                                               
                                        _FixedSolidityRatio = 0.15, _FixedWidthChar = 14,
                                        _HeightRatioMin = 0.5, _HeightRatioMax = 0.95):
        self.typePlate = _TypePlate
        self.fixedWidth = _FixedWidth       # (Biển dài = 400 | Biển ngắn = 200)
        self.fixedAspectRatio = _FixedAspectRatio
        self.fixedSolidityRatio = _FixedSolidityRatio
        self.fixedWidthChar = _FixedWidthChar
        self.heightRatioMin = _HeightRatioMin
        self.heightRatioMax = _HeightRatioMax

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
        plate = _ImgInput
        if (self.typePlate == 0): # Xử lý biển số dài
            charactersFound, imgDraw = segment_characters_from_plate(_ImgInput = plate, 
                                                            _FixedWidth = self.fixedWidth, 
                                                            _FixedAspectRatio = self.fixedAspectRatio,
                                                            _FixedSolidityRatio = self.fixedSolidityRatio,
                                                            _FixedWidthChar = self.fixedWidthChar,
                                                            _HeightRatioMin = self.heightRatioMin,
                                                            _HeightRatioMax = self.heightRatioMax)
            if charactersFound:
                return charactersFound, imgDraw

        elif (self.typePlate == 1): # Xử lý biển số ngắn
            # Chia biển số thành hai phần trên dưới
            plate_upper = plate[0:int(plate.shape[0]/2), 0:plate.shape[1]]
            plate_lower = plate[int(plate.shape[0]/2): plate.shape[0], 0:plate.shape[1]]

            # Lấy các ký tự của phần trên và phần dưới
            upper_charactersFound, imgDrawUp = segment_characters_from_plate(_ImgInput = plate_upper,
                                                                  _FixedWidth = self.fixedWidth, 
                                                                  _FixedAspectRatio = self.fixedAspectRatio,
                                                                  _FixedSolidityRatio = self.fixedSolidityRatio,
                                                                  _FixedWidthChar = self.fixedWidthChar,
                                                                  _HeightRatioMin = self.heightRatioMin,
                                                                  _HeightRatioMax = self.heightRatioMax)
            lower_charactersFound, imgDrawLow = segment_characters_from_plate(_ImgInput = plate_lower,
                                                                  _FixedWidth = self.fixedWidth, 
                                                                  _FixedAspectRatio = self.fixedAspectRatio,
                                                                  _FixedSolidityRatio = self.fixedSolidityRatio,
                                                                  _FixedWidthChar = self.fixedWidthChar,
                                                                  _HeightRatioMin = self.heightRatioMin,
                                                                  _HeightRatioMax = self.heightRatioMax)
            imgDraw = np.concatenate((imgDrawUp, imgDrawLow), axis=0)
            if (upper_charactersFound and lower_charactersFound):
                charactersFound = upper_charactersFound + lower_charactersFound
                return charactersFound, imgDraw