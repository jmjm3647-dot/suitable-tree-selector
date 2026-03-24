import serial
ser = serial.Serial("COM3", 115200)

#file = open("microbitmoisture.csv","w")
#file.write("Temperature,Moisture\n")
#file.close()

for i in range(100):
    data = ser.readline().decode("utf-8").strip()
    print(data) #Print data to see if it is correct.
    
    separate_data = data.split(",")
    if len(separate_data) == 2:
        temp = separate_data[0]
        moisture = separate_data[1]

        file = open("microbitmoisture.csv","a")
        file.write(temp)
        file.write(",")
        file.write(moisture)
        file.write("\n")
        file.close()
