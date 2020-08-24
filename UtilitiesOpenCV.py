import cv2
import numpy as np

class UtilitiesOpenCV():
    def change_brightness(self, _ImgInput, _Alpha, _Beta):
        """
        Thay đổi độ sáng của ảnh (Tăng độ rõ của ký tự)
        ...
        Parameters
            ----------
            _ImgInput : Hình ảnh biển số
            _Alpha: Độ đo alpha
            _Beta: Độ đo beta
            ----------
        Returns
            ----------
            Hình ảnh sau khi thay đổi độ sáng
            ----------
        """
        img_new = np.asarray(_Alpha * _ImgInput + _Beta, dtype = np.int)
        img_new[img_new>255] = 255
        img_new[img_new<0] = 0
        img_new = np.array(img_new, dtype=np.uint8)
        return img_new

    def resize_2square_keeping_aspectRation(self, _ImgInput, _SizeWidth = 24, _SizeHeight = 24, _Interpolation = cv2.INTER_AREA):
        """
        Thay đổi kích thước hình ảnh giữ nguyên tỷ lệ theo hai chiều
        ...
        Parameters
            ----------
            _ImgInput : Hình ảnh biển số
            _SizeWidth: Chiều dài
            _SizeHeight: Chiều cao
            _Interpolation: Phương pháp nội suy
            ----------
        Returns
            ----------
            Hình ảnh sau khi thay đổi kích thước
            ----------
        """
        h, w = _ImgInput.shape[:2]
        c = None if len(_ImgInput.shape) < 3 else _ImgInput.shape[2]

        if h == w:
            return cv2.resize(_ImgInput, (_SizeWidth, _SizeHeight), _Interpolation)
        if h > w:
            dif = h
        else:
            dif = w

        x_pos = int((dif - w)/2.)
        y_pos = int((dif - h)/2.)
        if c is None:
            mask = np.zeros((dif, dif), dtype=_ImgInput.dtype)
            mask[y_pos:y_pos+h, x_pos:x_pos+w] = _ImgInput[:h, :w]
        else:
            mask = np.zeros((dif, dif, c), dtype=_ImgInput.dtype)
            mask[y_pos:y_pos+h, x_pos:x_pos+w, :] = _ImgInput[:h, :w, :]
        return cv2.resize(mask, (_SizeWidth, _SizeHeight), _Interpolation)

    def resize_border_threshold(self, _ImgInput, _SizeWidth = 26, _SizeHeight = 26, _Border = 1, _BorderType = cv2.BORDER_CONSTANT, _ThresholdMin = 127):
        """
        Thay đổi kích thước hình ảnh giữ nguyên tỷ lệ theo hai chiều và thêm lề
        ...
        Parameters
            ----------
            _ImgInput : Hình ảnh biển số
            _SizeWidth: Chiều dài
            _SizeHeight: Chiều cao
            _Border: Kích thước lề
            _BorderType: Phương pháp thêm lề (cv2.BORDER_CONSTANT | cv2.BORDER_REPLICATE)
            ----------
        Returns
            ----------
            Hình ảnh sau khi thay đổi kích thước
            ----------
        """
        # Thay đổi kích thước
        resizedBorder = cv2.resize(_ImgInput, dsize=(_SizeWidth, _SizeHeight))
        resizedBorder = cv2.copyMakeBorder(resizedBorder, top=_Border, bottom=_Border, left=_Border, right=_Border, borderType=_BorderType)
        
        # Phân ngưỡng
        resizedThreshold = cv2.threshold(resizedBorder, _ThresholdMin, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]     

        return resizedThreshold

    def resize_border(self, _ImgInput, _SizeWidth = 24, _SizeHeight = 24, _Border = 2, _BorderType = cv2.BORDER_CONSTANT):
        """
        Thay đổi kích thước hình ảnh giữ nguyên tỷ lệ theo hai chiều và thêm lề
        ...
        Parameters
            ----------
            _ImgInput : Hình ảnh biển số
            _SizeWidth: Chiều dài
            _SizeHeight: Chiều cao
            _Border: Kích thước lề
            _BorderType: Phương pháp thêm lề (cv2.BORDER_CONSTANT | cv2.BORDER_REPLICATE)
            ----------
        Returns
            ----------
            Hình ảnh sau khi thay đổi kích thước
            ----------
        """
        resizedKeep = self.resize_2square_keeping_aspectRation(_ImgInput, _SizeWidth, _SizeHeight, cv2.INTER_AREA)
        
        resizedBorder = cv2.copyMakeBorder(
            resizedKeep,
            top = _Border,
            bottom = _Border,
            left = _Border,
            right = _Border,
            borderType = cv2.BORDER_CONSTANT
        )

        return resizedBorder

    def resize_height(self, _ImgInput, _SizeHeight = 110):
        """
        Thay đổi kích thước hình ảnh giữ nguyên tỷ lệ theo chiều cao
        ...
        Parameters
            ----------
            _ImgInput : Hình ảnh biển số
            _SizeHeight: Chiều cao
            ----------
        Returns
            ----------
            Hình ảnh sau khi thay đổi kích thước
            ----------
        """        
        aspect_ratio = float(_ImgInput.shape[0])/float(_ImgInput.shape[1])
        window_width = _SizeHeight/aspect_ratio
        result = cv2.resize(_ImgInput, (int(window_width), int(_SizeHeight)))
        return result

    def resize_width(self, _ImgInput, _SizeWidth = 470):
        """
        Thay đổi kích thước hình ảnh giữ nguyên tỷ lệ theo chiều dài
        ...
        Parameters
            ----------
            _ImgInput : Hình ảnh biển số
            _SizeWidth: Chiều dài
            ----------
        Returns
            ----------
            Hình ảnh sau khi thay đổi kích thước
            ----------
        """        
        aspect_ratio = float(float(_ImgInput.shape[1]/_ImgInput.shape[0]))
        window_height = _SizeWidth/aspect_ratio
        result = cv2.resize(_ImgInput, (int(_SizeWidth), int(window_height)))
        return result
    def change_brightness(self, _ImgInput, _Alpha, _Beta):
        """
        Thay đổi độ sáng của ảnh (Tăng độ rõ của ký tự)
        ...
        Parameters
            ----------
            _ImgInput : Hình ảnh biển số
            _Alpha: Độ đo alpha
            _Beta: Độ đo beta
            ----------
        Returns
            ----------
            Hình ảnh sau khi thay đổi độ sáng
            ----------
        """
        img_new = np.asarray(_Alpha * _ImgInput + _Beta, dtype = np.int)
        img_new[img_new>255] = 255
        img_new[img_new<0] = 0
        img_new = np.array(img_new, dtype=np.uint8)
        return img_new

    def resize_2square_keeping_aspectRation(self, _ImgInput, _SizeWidth = 24, _SizeHeight = 24, _Interpolation = cv2.INTER_AREA):
        """
        Thay đổi kích thước hình ảnh giữ nguyên tỷ lệ theo hai chiều
        ...
        Parameters
            ----------
            _ImgInput : Hình ảnh biển số
            _SizeWidth: Chiều dài
            _SizeHeight: Chiều cao
            _Interpolation: Phương pháp nội suy
            ----------
        Returns
            ----------
            Hình ảnh sau khi thay đổi kích thước
            ----------
        """
        h, w = _ImgInput.shape[:2]
        c = None if len(_ImgInput.shape) < 3 else _ImgInput.shape[2]

        if h == w:
            return cv2.resize(_ImgInput, (_SizeWidth, _SizeHeight), _Interpolation)
        if h > w:
            dif = h
        else:
            dif = w

        x_pos = int((dif - w)/2.)
        y_pos = int((dif - h)/2.)
        if c is None:
            mask = np.zeros((dif, dif), dtype=_ImgInput.dtype)
            mask[y_pos:y_pos+h, x_pos:x_pos+w] = _ImgInput[:h, :w]
        else:
            mask = np.zeros((dif, dif, c), dtype=_ImgInput.dtype)
            mask[y_pos:y_pos+h, x_pos:x_pos+w, :] = _ImgInput[:h, :w, :]
        return cv2.resize(mask, (_SizeWidth, _SizeHeight), _Interpolation)

    def resize_border(self, _ImgInput, _SizeWidth = 24, _SizeHeight = 24, _Border = 2, _BorderType = cv2.BORDER_CONSTANT):
        """
        Thay đổi kích thước hình ảnh giữ nguyên tỷ lệ theo hai chiều và thêm lề
        ...
        Parameters
            ----------
            _ImgInput : Hình ảnh biển số
            _SizeWidth: Chiều dài
            _SizeHeight: Chiều cao
            _Border: Kích thước lề
            _BorderType: Phương pháp thêm lề (cv2.BORDER_CONSTANT | cv2.BORDER_REPLICATE)
            ----------
        Returns
            ----------
            Hình ảnh sau khi thay đổi kích thước
            ----------
        """
        resizedKeep = self.resize_2square_keeping_aspectRation(_ImgInput, _SizeWidth, _SizeHeight, cv2.INTER_AREA)
        
        resizedBorder = cv2.copyMakeBorder(
            resizedKeep,
            top = _Border,
            bottom = _Border,
            left = _Border,
            right = _Border,
            borderType = cv2.BORDER_CONSTANT
        )

        return resizedBorder

    def resize_height(self, _ImgInput, _SizeHeight = 110):
        """
        Thay đổi kích thước hình ảnh giữ nguyên tỷ lệ theo chiều cao
        ...
        Parameters
            ----------
            _ImgInput : Hình ảnh biển số
            _SizeHeight: Chiều cao
            ----------
        Returns
            ----------
            Hình ảnh sau khi thay đổi kích thước
            ----------
        """        
        aspect_ratio = float(_ImgInput.shape[0])/float(_ImgInput.shape[1])
        window_width = _SizeHeight/aspect_ratio
        result = cv2.resize(_ImgInput, (int(window_width), int(_SizeHeight)))
        return result

    def resize_width(self, _ImgInput, _SizeWidth = 470):
        """
        Thay đổi kích thước hình ảnh giữ nguyên tỷ lệ theo chiều dài
        ...
        Parameters
            ----------
            _ImgInput : Hình ảnh biển số
            _SizeWidth: Chiều dài
            ----------
        Returns
            ----------
            Hình ảnh sau khi thay đổi kích thước
            ----------
        """        
        aspect_ratio = float(float(_ImgInput.shape[1]/_ImgInput.shape[0]))
        window_height = _SizeWidth/aspect_ratio
        result = cv2.resize(_ImgInput, (int(_SizeWidth), int(window_height)))
        return result