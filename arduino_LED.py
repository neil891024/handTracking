import serial

COM_PORT = 'COM3'  # 根據連結的Arduino的通訊埠修改設定
BAUD_RATES = 9600
arduinoSerial = serial.Serial(COM_PORT, BAUD_RATES)

try:
    while True:
        choice = input('1:開燈　0:關燈　9:關閉程式  ')
        if choice == '1':
            print('開燈')
            arduinoSerial.write(b'1')
        elif choice == '0':
            print('關燈')
            arduinoSerial.write(b'0')
        elif choice == '9':
            print('關閉程式')
            arduinoSerial.close()
            exit()
        else:
            print('指令錯誤')

except KeyboardInterrupt:
    arduinoSerial.close()    # 清除序列通訊物件
    print('關閉程式')