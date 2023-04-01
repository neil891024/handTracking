#openCV+mediapipe 手部追蹤
import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands #要使用的是手部模型
hands = mpHands.Hands(model_complexity=0,min_detection_confidence=0.5,min_tracking_confidence=0.5) #使用mpHands呼叫Hands函式
#參數設定 25:30
mpDraw = mp.solutions.drawing_utils
handLmsStyle = mpDraw.DrawingSpec(color=(0,0,255),thickness=5) #設定點的顏色、粗度
handConStyle = mpDraw.DrawingSpec(color=(0,255,0),thickness=10) #設定線的顏色、粗度
pTime = 0
cTime = 0

while True:
    ret,img = cap.read()
    if ret:
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #手部偵測需要RGB的圖片
        result = hands.process(imgRGB)
        #print(result.multi_hand_landmarks) #回傳偵測到所有手的21點的座標

        imgHeight = img.shape[0] #高度
        imgWidth = img.shape[1] #寬度
        
        if result.multi_hand_landmarks:#判斷是否有偵測到手
            for handLms in result.multi_hand_landmarks: #畫出偵測到的每隻手
                mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS,handLmsStyle,handConStyle) 
                #參數順序1.圖片 2.handLms(手的21點) 3.將點用線連接起來 4.設定點的樣式 5.設定線的樣式
                for i,lm in enumerate(handLms.landmark): #找出21個點的座標，enumerate(seq,[start=0])
                    xPos = int(lm.x*imgWidth) 
                    yPos = int(lm.y*imgHeight)
                    #因座標顯示的數為比例，需乘於視窗大小才為點的座標
                    #cv2.putText(img,str(i),(xPos-25,yPos+5),cv2.FONT_HERSHEY_COMPLEX,0.4,(0,0,255),2) #再點上寫上編號
                    #參數順序 1.圖片 2.文字 3.位置 4.字型 5.大小 6.顏色 7.粗度

                    if i ==4: #把任一點放大
                        cv2.circle(img, (xPos,yPos), 10 ,(0,0,255),cv2.FILLED)
                    print(i,xPos,yPos) #i=第幾個，從0開始

        cTime = time.time() #取得現在的時間
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, f"FPS : {int(fps)}",(30, 50),cv2.FONT_HERSHEY_COMPLEX, 1,(255,0,0),3)

        cv2.imshow('img',img)
    
    if cv2.waitKey(1) == ord('q'):
        break

