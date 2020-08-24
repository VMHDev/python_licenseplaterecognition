import cv2
import numpy as np

def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

def draw_prediction(img, classes, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    
    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
    color = COLORS[class_id]

    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)

    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

class DetectionYOLO():
    def __init__(self, _Config = '', _Weights = '', _Classes = '', _Scale = 0.00392):
        self.config = _Config
        self.weights = _Weights
        self.classes = _Classes
        self.scale = _Scale

    def detection(self, _ImgInput):
        image_YOLO = _ImgInput

        if self.config == '' or self.weights == '' or self.classes == '':
            return 0, None

        Width = image_YOLO.shape[1]
        Height = image_YOLO.shape[0]
        scale = self.scale

        classes = None

        with open(self.classes, 'r') as f:
            classes = [line.strip() for line in f.readlines()]

        net = cv2.dnn.readNet(self.weights, self.config)

        blob = cv2.dnn.blobFromImage(image_YOLO, scale, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)

        outs = net.forward(get_output_layers(net))

        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.5
        nms_threshold = 0.4

        # Thực hiện xác định bằng HOG và SVM
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])
        img_plate = np.array([])
        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
        if len(indices) != 1:
            return 0, img_plate

        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            draw_prediction(image_YOLO, classes, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
            img_plate = image_YOLO[round(y):round(y + h), round(x):round(x + w),  :]

        if np.shape(img_plate) == ():
            return 0, img_plate
        else:
            return 1, img_plate