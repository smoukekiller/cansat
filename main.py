import tkintermapview
import tkinter as tk
import threading
import serial
import time
#sigma main class
class Win:

    #new skibidi update function
    def update(self) -> None:
        for widget in self.data_frame.winfo_children():
            widget.destroy()
        self.write_data()

        self.data["predicted latitude"] = round(self.data["predicted latitude"] + 0.001, 6)
        self.root.after(1000, self.update)

    #sigma data
    def write_data(self) -> None:


        for name, value in self.data.items(): 
            label = tk.Label(self.data_frame, text=f"{name}:{value}", font=("Arial", 12), bg="lightgrey")
            label.pack(side="top", anchor="nw")
        self.marker_of_prediction.set_position(self.data["latitude"], self.data["longitude"])


    def __init__(self) -> None:
        #create sigma window
        self.root = tk.Tk()
        self.root.title("Sigma fish map")
        self.root.geometry("1920x1080")  
        self.timer = time.time()
        self.ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)
        data = self.ser.readline().decode('utf-8').strip()
        





        if data:
            print(f"Received data: {data}")
        self.data = {
            "predicted latitude": 63.094227,
            "predicted longitude": 21.608214,
            "latitude": 63.094227,
            "longitude": 21.608214,
            "velocity": 0,
            "altitude": 0,
            "gpstime": 0
        }            
        self.zoom = 15
        #coordinates 
        self.start_latitude, self.start_longitude = 63.094227, 21.608214
        #create sigma Frames 
        self.map_frame = tk.Frame(self.root, width=600, height=600)
        self.data_frame = tk.Frame(self.root, width=400, height=600, bg="lightgrey")
        self.marker_latitude, self.marker_longitude = 63.094227, 21.608214

        #some settings that I found in google that allow window to scale properly
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)


        #assign sigma frames to sigma grids
        self.map_frame.grid(row=0, column=0, sticky="nsew")
        self.data_frame.grid(row=0, column=1, sticky="nsew")

        #create sigma map
        self.map_widget = tkintermapview.TkinterMapView(self.map_frame, width=600, height=600)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_position(self.start_latitude, self.start_longitude)  # San Francisco coordinates
        self.map_widget.set_zoom(self.zoom)

        self.marker_of_prediction = self.map_widget.set_marker(self.data["predicted latitude"], self.data["predicted longitude"])
        
        self.thread = threading.Thread(target=self.ReadSerial, args=(), daemon=True)
        self.thread.start()

        self.root.after(100, self.update)
        self.root.mainloop()
    
    def ReadSerial(self):
        while True:
            data = self.ser.readline().decode('utf-8').strip()
            if data:
                print(f"Received data: {data}")
                if (data[0:4] == "DATA"):
                    pass
                elif (data[0:11] == "Coordinates"):
                    data = data.replace("Coordinates:", "")
                    arr = data.split(",")
                    print(arr)
                    self.data["gpstimer"] = int(arr[0])
                    self.data["latitude"] = float(arr[1])
                    self.data["longitude"] = float(arr[2])
                    




#skibidi update function
# def update():
#     print(1)
#     root.after(1000, update)


if __name__ == "__main__":
    window = Win()
    


#erhm what the sigma
#sigma fishes rule the world
#Kiril is gay
