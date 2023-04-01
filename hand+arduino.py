#判斷手勢控制LED動作(電燈全開、全關)
#副函式順序 hand_angle
import cv2
import mediapipe as mp
import math
import time
import serial

#python控arduino LED
COM_PORT = 'COM3'  # 根據連結的Arduino的通訊埠修改設定
BAUD_RATES = 9600
arduinoSerial = serial.Serial(COM_PORT, BAUD_RATES)

mp_drawing = mp.solutions.drawing_utils #mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles #mediapipe 繪圖樣式
mp_hands = mp.solutions.hands #mediapipe 偵測手掌方法

def vector_2d_angle(v1, v2):
    """根據兩點的座標，計算角度"""
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]

    try: #嘗試將angle_轉為角度
        angle_= math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
        #math.acos 回傳反正弦值 math.degrees將角度轉為弧度，或是弧度轉為角度
    except:
        angle_ = 180
    return angle_

def hand_angle(hand_): 
    """根據傳入的 21 個節點座標，得到該手指的角度"""
    angle_list = []
    # thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
        ((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1])))
        )
    angle_list.append(angle_)
    # index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
        ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
        )
    angle_list.append(angle_)
    # middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),
        ((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1])))
        )
    angle_list.append(angle_)
    # ring 無名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),
        ((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1])))
        )
    angle_list.append(angle_)
    # pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),
        ((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))
        )
    angle_list.append(angle_)
    return angle_list

def hand_pos(finger_angle): #判斷角度範圍，回傳該角度代表的文字
    """根據手指角度的串列內容，返回對應的手勢名稱"""
    f1 = finger_angle[0]   # 大拇指角度
    f2 = finger_angle[1]   # 食指角度
    f3 = finger_angle[2]   # 中指角度
    f4 = finger_angle[3]   # 無名指角度
    f5 = finger_angle[4]   # 小拇指角度

    # 小於 50 表示手指伸直，大於等於 50 表示手指捲縮
    if f1>50 and f2>50 and f3<50 and f4>50 and f5>50:
        return 'hello'
    elif f1>=50 and f2<50 and f3>=50 and f4>=50 and f5>=50:
        return '1'
    else:
        return ''

cap = cv2.VideoCapture(0)            # 讀取攝影機
fontFace = cv2.FONT_HERSHEY_SIMPLEX  # 印出文字的字型
lineType = cv2.LINE_AA               # 印出文字的邊框

# mediapipe 啟用偵測手掌
with mp_hands.Hands( 
    #使用mpHands呼叫Hands函式
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    # model_complexity 模型複雜度 
    # min detection confidence 最小檢測置信度
    # min tracking confidence 最小跟踪置信度

    if not cap.isOpened(): #檢查攝像機有無啟動
        print("Cannot open camera")
        exit() #直接讓程式終止

    w, h = 700,400 #設定影像尺寸
    while True:
        ret, img = cap.read() #讀取每幀的圖片
        img = cv2.resize(img, (w,h)) # 縮小尺寸，加快處理效率
        if not ret: #判斷有沒有讀到圖片
            print("Cannot receive frame")
            break

        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #轉換成 RGB 色彩
        results = hands.process(img2) #偵測手勢
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                finger_points = [] #記錄手指節點座標的串列
                for i in hand_landmarks.landmark:
                    # 將 21 個節點換算成座標，記錄到 finger_points
                    x = i.x*w
                    y = i.y*h
                    finger_points.append((x,y))
                if finger_points:
                    finger_angle = hand_angle(finger_points) # 計算手指角度，回傳長度為 5 的串列
                    #print(finger_angle)                     # 印出角度 ( 有需要就開啟註解 )
                    #time.sleep(1)                           # 延遲時間
                    text = hand_pos(finger_angle)            # 取得手勢所回傳的內容
                    if text == 'hello':
                        arduinoSerial.write(b'1')
                    elif text == '1':
                        arduinoSerial.write(b'0') 
                    cv2.putText(img, text, (30,120), fontFace, 5, (255,255,255), 10, lineType) # 印出文字
                    
        cv2.imshow('oxxostudio', img)
        if cv2.waitKey(5) == ord('q'):
            break
cap.release() #關閉攝像機
cv2.destroyAllWindows() #關閉窗口