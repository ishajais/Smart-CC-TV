import cv2
import numpy as np

def load_yolo_model():
    
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    
    layers_names = net.getLayerNames()
    output_layers = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return net, classes, output_layers

def detect_objects(image, net, output_layers, classes):
    height, width = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:  
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

              
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    
    for i in range(len(boxes)):
        if i in indices:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = (0, 255, 0)  
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            cv2.putText(image, f"{label} {confidence:.2f}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return image

if __name__ == "__main__":
    
    net, classes, output_layers = load_yolo_model()

    
    image = cv2.imread("path_to_your_image.jpg")

    
    detected_image = detect_objects(image, net, output_layers, classes)

    cv2.imshow("Object Detection", detected_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
