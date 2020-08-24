import cv2
import numpy as np
from WPODNET.lib_detection import load_model, detect_lp, im2single

class DetectionWPODNET():
    def __init__(self, _ModelWPODNET = '', _SizeMax = 608, _SizeMin = 288, _Threshold = 0.5):
        self.modelWPODNET = _ModelWPODNET           # Mô hình WPOD để nhận diện
        self.sizeMax = _SizeMax                     # Kích thước ước lượng biển số lớn nhất trong ảnh
        self.sizeMin = _SizeMin                     # Kích thước ước lượng biển số nhỏ nhất trong ảnh
        self.threshold = _Threshold                 # Ngưỡng nhận diện
        

    def detection(self, _ImgInput):
        img_vehicle = _ImgInput
        img_plate = np.array([])
        # Load mô hình WPOD để nhận diện
        wpod_net_path = self.modelWPODNET
        if wpod_net_path == '':
            return 0, None
        wpod_net = load_model(wpod_net_path)
        
        # Kích thước lớn nhất và nhỏ nhất của 1 chiều ảnh => Điều chỉnh để lấy trọn vẹn biển số
        Dmax = self.sizeMax
        Dmin = self.sizeMin
        
        # Lấy tỷ lệ giữa W và H của ảnh và tìm ra chiều nhỏ nhất
        ratio = float(max(img_vehicle.shape[:2])) / min(img_vehicle.shape[:2])
        side = int(ratio * Dmin)
        bound_dim = min(side, Dmax)
        _ , LpImg, _ = detect_lp(wpod_net, im2single(img_vehicle), bound_dim, lp_threshold=self.threshold)
        
        # Nếu hình không có biển số hoặc có nhiều hơn 1 biển thì không xử lý nữa
        if len(LpImg) != 1:
            return 0, img_plate
        else:
            plate = LpImg[0]
            img_plate = cv2.convertScaleAbs(plate, alpha=(255.0))
            return 1, img_plate