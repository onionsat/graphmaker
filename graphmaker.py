import customtkinter as ctk
from customtkinter import filedialog
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import os
from tkinter import messagebox
import traceback

#Unix timestamp@#coords|gps_satelites|gps_date|gps_angle|temperature|humidity|pressure|altitude|acc_x|acc_y|acc_z
#1701033480717@#47.5269, 19.0580|5|2023-11-23 16:53:42|8.79|24.23|33.03|1006.32|25.60|0.47|0.12|11.02

def dataSelecter(file):
    #szélességi kör
    latitude = []
    #hossúsági kör
    longitude = []
    #hőmérséklet
    temperature = []
    #páratartalom
    humidity = []
    #nyomás
    pressure = []
    #magasság
    altitude=[]
    #x irányú gyorsulás
    x_acc = []
    #y irányú gyorsulás
    y_acc = []
    #z irányú gyorsulás
    z_acc = []
    #szumma gyorsulás
    acc = []

    with open(file, "r") as dataFile:
        for line in dataFile:
            currentLine = line.split("|")
        
            #gps coords
            currentGPScoords = currentLine[0].split("#")
            currentGPScoords = currentGPScoords[1]
            currentGPScoords = currentGPScoords.split(", ")
            currentLatitude = currentGPScoords[0]
            currentLongitude = currentGPScoords[1]

            #bme280 datas
            currentTemperature = currentLine[4]
            currentHumidity = currentLine[5]
            currentPressure = currentLine[6]
            currentAltitude = currentLine[7]

            #adxl345 datas
            current_x_acc = currentLine[8]
            current_y_acc = currentLine[9]
            current_z_acc = currentLine[10]

            try:
                currentLatitude = float(currentLatitude)
                currentLongitude = float(currentLongitude)
                currentTemperature = float(currentTemperature)
                currentHumidity = float(currentHumidity)
                currentPressure = float(currentPressure)
                currentAltitude = float(currentAltitude)
                current_x_acc = float(current_x_acc)
                current_y_acc = float(current_y_acc)
                current_z_acc = float(current_z_acc)
            except:
                pass
            else:
                latitude.append(currentLatitude)
                longitude.append(currentLongitude)
                temperature.append(currentTemperature)
                humidity.append(currentHumidity)
                pressure.append(currentPressure)
                altitude.append(currentAltitude)
                x_acc.append(current_x_acc)
                y_acc.append(current_y_acc)
                z_acc.append(current_z_acc)

                currentSumAcc = math.sqrt(current_x_acc**2 + current_y_acc**2 + current_z_acc**2)
                acc.append(currentSumAcc)
        
        return [latitude, longitude, temperature, humidity, pressure, altitude, x_acc, y_acc, z_acc, acc]


def degrees_to_radians(degrees):
    return degrees * (math.pi / 180)


def create_graph(choice):
    try:
        data = dataSelecter(flightLog)

        if choice == "Position Graph":
            #szélességi
            currentLatitudeList = data[0]
            #hosszúsági
            currentLongitudeList = data[1]
            #magasság
            currentAltitudeList = data[5]
            #a listák mostani hossza       
            currentLenght = len(currentLatitudeList)

            goodLatitudeList = []
            goodLongitudeList = []
            goodAltitudeList = []


            for h in range(0,currentLenght):
                if currentLatitudeList[h] != 0 and currentLongitudeList[h] != 0:
                    goodLatitudeList.append(currentLatitudeList[h])
                    goodLongitudeList.append(currentLongitudeList[h])
                    goodAltitudeList.append(currentAltitudeList[h])
            
            #már jók az adatok
            goodLenght = len(goodAltitudeList)
            latitudeDistances = []
            longitudeDistances = []

            #kiválasztom a referenciakoordinátákat
            latitudeRef = goodLatitudeList[0]
            longitudeRef = goodLongitudeList[0]

            #átváltom a referenciákat radiánba
            latitudeRef = degrees_to_radians(latitudeRef)
            longitudeRef = degrees_to_radians(longitudeRef)

            #formula: acos(sin(lat1)*sin(lat2)+cos(lat1)*cos(lat2)*cos(lon2-lon1))*6371, lon1 és lat1 a referenciák
            for j in range(0,goodLenght):
                currentLongitudeRadian = degrees_to_radians(goodLongitudeList[j])
                currentLatitudeRadian = degrees_to_radians(goodLatitudeList[j])

                #lon2 = lon1, lon1=ref
                #currentLatitudeDistance = (math.acos(math.sin(latitudeRef)*math.sin(currentLatitudeRadian)+math.cos(latitudeRef)*math.cos(currentLatitudeRadian)*math.cos(currentLatitudeRadian-latitudeRef)))*6371000
                currentLatitudeDistance = (math.acos(math.sin(latitudeRef)*math.sin(currentLatitudeRadian)+math.cos(latitudeRef)*math.cos(currentLatitudeRadian)))*6371000

                #lat2=lat1, lat1=ref
                helper = currentLongitudeRadian-longitudeRef
                currentLongitudeDistance = (math.acos(math.sin(latitudeRef)*math.sin(latitudeRef)+math.cos(latitudeRef)*math.cos(latitudeRef)*math.cos(helper)))*6371000
            
                latitudeDistances.append(currentLatitudeDistance)
                longitudeDistances.append(currentLongitudeDistance)

            
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot(latitudeDistances, longitudeDistances, goodAltitudeList, c='g', marker='o')

            # Set labels and title
            ax.set_xlabel('Distance[m]')
            ax.set_ylabel('Distance[m]')
            ax.set_zlabel('Height[m]')
            ax.set_title('Position Graph')
            ax.invert_xaxis()
            ax.set_zlim(0,1500)

            plt.show()


        if choice == "Altitude-Temperature":
            plt.plot(data[5], data[2])

            plt.xlabel("Altitude")
            plt.ylabel("Temperture")
            plt.title(choice)
            plt.ylim(-20,60)

            plt.show()
    
        if choice == "Altitude-Humidity":
            plt.plot(data[5], data[3])

            plt.xlabel("Altitude")
            plt.ylabel("Humidity")
            plt.title(choice)
            plt.ylim(0,100)

            plt.show()

        if choice == "Altitude-Pressure":
            plt.plot(data[5], data[4])

            plt.xlabel("Altitude")
            plt.ylabel("Pressure")
            plt.title(choice)
            plt.ylim(0,1500)

            plt.show()
            

        if choice == "Altitude-Accelerations":
            plt.plot(data[5], data[6], color='r', label="x_acc")
            plt.plot(data[5], data[7], color='b', label="y_acc")
            plt.plot(data[5], data[8], color='g', label="z_acc")

            plt.xlabel("Altitude")
            plt.ylabel("Accceleration")
            plt.title(choice)

            plt.legend()

            plt.show()


        if choice == "Altitude-Acceleration":
            plt.plot(data[5], data[9])

            plt.xlabel("Altitude")
            plt.ylabel("Acceleration")
            plt.title(choice)

            plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"{traceback.format_exc()}")
    
    selected_option.set("Choose a graph!")


def select_file():
    global flightLog, currentfile_label
    flightLog = filedialog.askopenfilename()
    fileName = os.path.basename(flightLog)
    currentfile_label.configure(text=f"Current file is: {fileName}")


flightLog = ""

root = ctk.CTk()
root.title("OnionSAT Graphmaker")
root.geometry("300x125")

selected_option = ctk.StringVar(value="Choose a graph!")

currentfile_label = ctk.CTkLabel(root, text="Choose a file!")
currentfile_label.pack(pady=5)

select_file_button = ctk.CTkButton(root, text="Select a file", command = select_file)
select_file_button.pack(pady=0)

option_menu = ctk.CTkOptionMenu(master=root, values=["Position Graph", "Altitude-Temperature", "Altitude-Humidity", "Altitude-Pressure","Altitude-Accelerations", "Altitude-Acceleration"], command=create_graph, variable=selected_option)
option_menu.pack(pady=5)

root.mainloop()