from tkinter import *
from tkinter import messagebox
import mysql.connector
import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model
import keras.utils as image
from PIL import Image, ImageTk

window = None
register_window = None
model = None
hands = None
cap = None
pword_label = None
sign_label = None
sign_history=[]
sign_index_history=[]
start_timer=0

def clear():
    global sign_history, sign_index_history
    sign_history=[]
    sign_index_history=[]
    
def loadmodel():
    global model, hands, cap, class_labels
    model = load_model('model/keras_model.h5')
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mpDraw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)
    class_labels = [
        "5 fingers up",
        "Fist",
        "Peace",
        "Gun",
        "Rock",
        "Thumbs up",
        "Thumbs down",
        "Call",
        "OK",
        "Pinky",
        "Middle finger",
        "Loser",
        "Pointer",
        "Big",
        "Claw",
        "Zero",
        "Three",
        "Half air quotes"
    ]
    
def update_frame():
    global sign_history, pword_label, sign_label, register_window, sign_index_history, start_timer
    try:
        ret, frame = cap.read()
        h, w, c = frame.shape
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(framergb)
        if result.multi_hand_landmarks:
            for handslms in result.multi_hand_landmarks:
                x_max = 0
                y_max = 0
                x_min = w
                y_min = h
                landmarks = []
                for lm in handslms.landmark:
                    x = int(lm.x * w)
                    y = int(lm.y * h)
                    if x > x_max:
                        x_max = x
                    if x < x_min:
                        x_min = x
                    if y > y_max:
                        y_max = y
                    if y < y_min:
                        y_min = y
                    landmarks.append([x, y])
                cv2.rectangle(frame, (x_min-20, y_min-20), (x_max+20, y_max+20), (0, 255, 0), 2)
                roi = frame[y_min-20:y_max+20, x_min-20:x_max+20]
                roi = cv2.resize(roi, (224, 224))
                img_tensor = image.img_to_array(roi)
                img_tensor = np.expand_dims(img_tensor, axis=0)
                img_tensor /= 255.
                prediction = model.predict(img_tensor)
                class_index = np.argmax(prediction[0])
                class_label = class_labels[class_index]
                cv2.putText(frame, class_label, (x_min-20, y_min-40), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 255, 0), 2)
                start_timer+=1
                if start_timer>=35:
                    response = messagebox.askyesno("Confirm Sign", f"Have you chosen {class_label}?")
                    if response:
                        sign_history.append(class_label)
                        sign_index_history.append(str(class_index))
                        signhistory=", ".join(sign_history)
                        sign_label.config(text=f"Signs detected: {signhistory}")
                    start_timer=0
                    
                        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = img.resize((500, 300))
        img_tk = ImageTk.PhotoImage(image=img)
        pword_label.configure(image=img_tk)
        pword_label.image = img_tk
        register_window.after(1, update_frame)
    except:
        update_frame()
def update_frame_login():
    global sign_history, pword_label, sign_label, login_window, sign_index_history, start_timer
    try:
        ret, frame = cap.read()
        h, w, c = frame.shape
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(framergb)
        if result.multi_hand_landmarks:
            for handslms in result.multi_hand_landmarks:
                x_max = 0
                y_max = 0
                x_min = w
                y_min = h
                landmarks = []
                for lm in handslms.landmark:
                    x = int(lm.x * w)
                    y = int(lm.y * h)
                    if x > x_max:
                        x_max = x
                    if x < x_min:
                        x_min = x
                    if y > y_max:
                        y_max = y
                    if y < y_min:
                        y_min = y
                    landmarks.append([x, y])
                cv2.rectangle(frame, (x_min-20, y_min-20), (x_max+20, y_max+20), (0, 255, 0), 2)
                roi = frame[y_min-20:y_max+20, x_min-20:x_max+20]
                roi = cv2.resize(roi, (224, 224))
                img_tensor = image.img_to_array(roi)
                img_tensor = np.expand_dims(img_tensor, axis=0)
                img_tensor /= 255.
                prediction = model.predict(img_tensor)
                class_index = np.argmax(prediction[0])
                class_label = class_labels[class_index]
                cv2.putText(frame, class_label, (x_min-20, y_min-40), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 255, 0), 2)
                start_timer+=1
                if start_timer>=35:
                    response = messagebox.askyesno("Confirm Sign", f"Have you chosen {class_label}?")
                    if response:
                        sign_history.append(class_label)
                        sign_index_history.append(str(class_index))
                        signhistory=", ".join(sign_history)
                        sign_label.config(text=f"Signs detected: {signhistory}")
                    start_timer=0
                        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = img.resize((500, 300))
        img_tk = ImageTk.PhotoImage(image=img)
        pword_label.configure(image=img_tk)
        pword_label.image = img_tk
        login_window.after(1, update_frame_login)
    except:
        update_frame_login()
    
    
    
passwords = {}
button_config = {
    "font": ("Helvetica", 20),
    "width": 20,
    "height": 2,
    "bg": "white",
    "fg": "black",
    "activebackground": "light blue",
    "activeforeground": "black"
}

def establishConnection(host='localhost', username='root', password='1234'):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            autocommit=True
        )
        print('SQL Connected')
        return connection
    except mysql.connector.Error as error:
        print("Failed to connect:", error)
        return None

def startup():
    L = ["CREATE DATABASE IF NOT EXISTS HGRS", "use HGRS",
         "CREATE TABLE IF NOT EXISTS Passwords (Username VARCHAR(30) PRIMARY KEY, Password VARCHAR(30))"]
    for i in L:
        cursor.execute(i)
    recordsfetch()


def welcomePage():
    def success(username):
        def go_back():
            window=Toplevel(successPage)
            cap.release()
            cv2.destroyAllWindows()
            successPage.destroy()
        successPage = Toplevel(window)
        successPage.attributes("-fullscreen", True)
        successPage.title("Success!")
        successPage.configure(bg='black')
        successPage.iconbitmap('assets/handsign.ico')
        logo_image = PhotoImage(file="assets/handsign.png")
        logo_label = Label(successPage, image=logo_image, bg='black')
        logo_label.image = logo_image 
        logo_label.pack(pady=30)
        label1 = Label(successPage, text="You are logged in as: ", font=("Arial", 20, 'bold', 'underline'), fg='white', bg='black')
        label1.pack(pady=5)
        label2 = Label(successPage, text=username, font=("Arial", 30, 'bold', 'underline'), fg='white', bg='black')
        label2.pack(pady=20)
        signout = Button(successPage, text="Sign Out", command=go_back, **button_config)
        signout.pack()
        
    def register():
        def submit_registration(username):
            global sign_index_history
            password="-".join(sign_index_history)
            if username in passwords:
                response = messagebox.askyesno("Username Exists", "Username already exists. Do you want to log in instead?")
                if response:
                    register_window.destroy()
                    login()
            else:
                passwords[username] = password
                cursor.execute("Insert into Passwords values('{}','{}')".format(username, password))
                messagebox.showinfo("Success", "Registration successful!")
                response = messagebox.askyesno("Log in", "Do you want to log in with the same credentials?")
                if response:
                    register_window.destroy()
                    success(username)
                else:
                    register_window.destroy()
        def go_back():
            window=Toplevel(register_window)
            cap.release()
            cv2.destroyAllWindows()
            register_window.destroy()
        loadmodel()
        global pword_label, sign_label, register_window
        clear()
        register_window = Toplevel(window)
        register_window.title("Registration")
        register_window.configure(bg="black")
        register_window.attributes("-fullscreen", True)
        frame = Frame(register_window, bg="black")
        frame.pack(pady=5)
        title_label = Label(frame, text="Registration Page", fg="white", bg="black", font=("Arial", 20,'bold',"underline"))
        title_label.pack(pady=5)
        canvas = Canvas(frame, bg="black", height=2)
        canvas.pack(fill="x", pady=10)
        canvas.create_line(0, 0, 500, 0, fill="white")
        username_label = Label(frame, text="Username:", fg="white", bg="black", font=("Helvetica", 15))
        username_label.pack(pady=5)
        username_entry = Entry(frame, font=("Helvetica", 15))
        username_entry.pack(pady=5)
        pword_label = Label(frame)
        pword_label.pack()
        sign_label = Label(frame, text="Signs detected: None", fg="white", bg="black", font=("Helvetica", 15))
        sign_label.pack()
        update_frame()
        canvas = Canvas(frame, bg="black", height=2)
        canvas.pack(fill="x", pady=10)
        canvas.create_line(0, 0, 500, 0, fill="white")
        submit_button = Button(frame, text="Register", command=lambda:submit_registration(username_entry.get()), **button_config)
        submit_button.pack(pady=3)
        go_back_button = Button(frame, text="Go Back", command=go_back, **button_config)
        go_back_button.pack(pady=3)
        register_window.mainloop()

    def login():
        def submit_login(username):
            global sign_index_history
            password="-".join(sign_index_history)
            if username not in passwords:
                response = messagebox.askyesno("Username does not exist", "Username does not exist in database. Do you want to register instead?")
                if response:
                    login_window.destroy()
                    register()
            else:
                if passwords[username] == password:
                    m1= messagebox.showinfo("Success", "Sucessfully logged in!")
                    if m1 == "ok":
                        login_window.destroy()
                        success(username)
                else:
                     messagebox.showerror("Incorrect Password",
                                 " Incorrect Password Entered. Please check the details once again.")                    
        def go_back():
            window=Toplevel(login_window)
            cap.release()
            cv2.destroyAllWindows()
            login_window.destroy()
        loadmodel()
        global pword_label, sign_label, login_window
        clear()
        login_window = Toplevel(window)
        login_window.title("Login")
        login_window.configure(bg="black")
        login_window.attributes("-fullscreen", True)
        frame = Frame(login_window, bg="black")
        frame.pack(pady=5)
        title_label = Label(frame, text="Login Page", fg="white", bg="black", font=("Arial", 20,'bold',"underline"))
        title_label.pack(pady=5)
        canvas = Canvas(frame, bg="black", height=2)
        canvas.pack(fill="x", pady=10)
        canvas.create_line(0, 0, 500, 0, fill="white")
        username_label = Label(frame, text="Username:", fg="white", bg="black", font=("Helvetica", 15))
        username_label.pack(pady=5)
        username_entry = Entry(frame, font=("Helvetica", 15))
        username_entry.pack(pady=5)
        pword_label = Label(frame)
        pword_label.pack()
        sign_label = Label(frame, text="Signs detected: None", fg="white", bg="black", font=("Helvetica", 15))
        sign_label.pack()
        update_frame_login()
        canvas = Canvas(frame, bg="black", height=2)
        canvas.pack(fill="x", pady=10)
        canvas.create_line(0, 0, 500, 0, fill="white")
        submit_button = Button(frame, text="Login", command=lambda:submit_login(username_entry.get()), **button_config)
        submit_button.pack(pady=3)
        go_back_button = Button(frame, text="Go Back", command=go_back, **button_config)
        go_back_button.pack(pady=3)
        login_window.mainloop()


    def quit_app():
        window.destroy()
    global window
    window = Tk()
    window.attributes("-fullscreen", True)
    window.title("Hand Sign Authentication using OpenCV")
    window.configure(bg='black')
    window.iconbitmap('assets/handsign.ico')
    logo_image = PhotoImage(file="assets/handsign.png")
    logo_label = Label(window, image=logo_image, bg='black')
    logo_label.image = logo_image
    logo_label.pack(pady=30)
    app_name_label = Label(window, text="Hand Sign Authentication using OpenCV", font=("Arial", 20, 'bold', 'underline'), fg='white', bg='black')
    app_name_label.pack()
    line = Canvas(window, height=2, width=window.winfo_screenwidth(), bg='white')
    line.pack(pady=10)
    greeting_label1 = Label(window, text="Greetings Dear User!", fg="white", bg="black", font=("Helvetica", 20))
    greeting_label1.pack(pady=35)
    register_button = Button(window, text="REGISTER", command=register, **button_config)
    register_button.pack(pady=3)
    login_button = Button(window, text="LOGIN", command=login, **button_config)
    login_button.pack(pady=3)
    quit_button = Button(window, text="QUIT", command=quit_app, **button_config)
    quit_button.pack(pady=3)
    window.mainloop()

def recordsfetch():
    global passwords
    query = "SELECT * FROM Passwords"
    cursor.execute(query)
    results = cursor.fetchall()
    for username, password in results:
        passwords[username] = password

conn = establishConnection()
cursor = conn.cursor()
startup()
welcomePage()