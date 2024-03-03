import numpy as np
import cv2
vc=cv2.VideoCapture("v1.avi")
if vc.isOpened():
    open,frame = vc.read()
else:
    open = False
while open:
    ret,frame = vc.read()
    if frame is None:
        break
    if ret == True:
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        cache,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
        gauss = cv2.GaussianBlur(thresh,(5,5),0)
        kernel = np.ones((3,3),np.uint8)
        dilate = cv2.dilate(gauss,kernel,iterations=2)
        #dilate = cv2.resize(dilate,(int(dilate.shape[0]*2),int(dilate.shape[1])))
        
        contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cleaned=[]
        for line in cv2.HoughLinesP(dilate,rho=1,theta=np.pi/10,threshold=15,minLineLength=1,maxLineGap=4):
            for x1,y1,x2,y2 in line:
                if abs(y2-y1)>1:
                    cleaned.append((x1,y1,x2,y2))
                    cv2.line(frame,(x1,y1),(x2,y2),[255,0,0],2)
        '''
        for cnt in contours:
            rect = cv2.minAreaRect(cnt)
            #print("rect:\n" , rect)
            points = cv2.boxPoints(rect)
            #print("\npoints_back:\n" , points)
            points = np.int0(points/3)
            binary = cv2.drawContours(frame , [points] , 0 ,(255,255,255) , 2)
        '''

        '''
        bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]
        for bbox in bounding_boxes:
            #[x , y, w, h] = bbox
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            #cnt = np.array([[x,y],[x+w,y],[x,y+h],[x+w,y+h]]) # 必须是array数组的形式
            rect = cv2.minAreaRect(contours[0]) # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
            box = cv2.boxPoints(rect) # 获取最小外接矩形的4个顶点坐标(ps: cv2.boxPoints(rect) for OpenCV 3.x)
            box = np.int0(box)
            # 画出来
            cv2.drawContours(frame, [box], 0, (255, 0, 0), 1)  
        '''
        cv2.imshow("test",frame)
        if cv2.waitKey(10) & 0xFF ==27 :
            break
vc.release()
cv2.destroyWindow()