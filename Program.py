import os
import time
import sys
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import simpledialog, messagebox
import pandas as pd
from openpyxl import *

# Instalación.
# pyinstaller --onefile --add-data "Excusas racionales de la adicción.xlsx;." --hidden-import=openpyxl --noconsole Program.py

# Variables globales.

if getattr(sys, 'frozen', False):
    # Si estamos en un entorno congelado.
    App_Path = sys._MEIPASS
else:
    # Si estamos en un entorno normal.
    App_Path = os.path.dirname(os.path.abspath(__file__))

EXCUSE_FILE = os.path.join(App_Path, "Excusas racionales de la adicción.xlsx")
START_HOUR = "22:30"
END_HOUR = "06:00"
PASSWORD = "123Fracaso$"
MINUTES = 15
EXTENSION_TIME = MINUTES * 60

# DataFrame
NAME_COLUMN_EXCUSES = 'Excusa'
NAME_COLUMN_TIME_OF_EXCUSE = 'Fecha y hora'
NAME_COLUMN_TASK_DONE_OR_NOT = 'Realizado'

def Shutdown():
    os.system("shutdown /s /t 1")

def Check_If_Now_Is_In_Hour_Range(Start_Hour, End_Hour):
    Now = datetime.now().time()
    Start = datetime.strptime(Start_Hour, "%H:%M").time()
    End = datetime.strptime(End_Hour, "%H:%M").time()
    if Start < End:
        return Start <= Now <= End
    else:
        return Now >= Start or Now <= End

def Show_Modal_Window(Title, Message, Input_Required=False, Default_Value="", Additional_Button=False):
    Root = tk.Tk()
    Root.attributes('-topmost', True)
    Root.withdraw()  # Oculta la ventana principal
    
    if Input_Required:
        User_Input = simpledialog.askstring(Title, Message, initialvalue=Default_Value, parent=Root)
    else:
        if Additional_Button:
            User_Input = messagebox.askyesno(Title, Message, parent=Root)
        else:
            User_Input = None
            messagebox.showwarning(Title, Message, parent=Root)
    
    Root.deiconify()  # Muestra la ventana principal para destruirla después
    Root.destroy()
    return User_Input

def Request_Password():
    return Show_Modal_Window("Tiempo de dejar...", "¿Vale la pena ingresar la contraseña?", True)

def Show_Warning():
    Show_Modal_Window("Se apaga", "Tenés 1 minutito para ir poniendo la contraseña...")

def Request_Excuse(Previous_Excuse="", Minutes = 30):
    # Crear una ventana principal para la aplicación de Tkinter
    Root = tk.Tk()
    Root.attributes('-topmost', True)
    Root.withdraw()  # Oculta la ventana principal
    
    # Solicitar excusa al usuario
    Excuse = simpledialog.askstring("Excusa", f"¿Para qué necesitás {Minutes} minutos más?", parent=Root)
    
    # Mostrar un mensaje de confirmación con la excusa anterior si existe
    Message = "¿Cumpliste con lo que justificaba estirar la adicción?"
    if Previous_Excuse:
        Message += f"\n\nExcusa previa: {Previous_Excuse}"
    
    # Agregar un botón adicional para confirmar que se hizo una parte
    Task_Done = messagebox.askyesno("Task Check", Message, parent=Root) if Previous_Excuse else None
    
    # Cerrar la ventana principal
    Root.deiconify()
    Root.destroy()
    
    return Excuse, Task_Done

def Get_Previous_Excuse():
    if os.path.exists(EXCUSE_FILE):
        df = pd.read_excel(EXCUSE_FILE)
        if len(df) > 0:
            Last_Excuse = df.iloc[-1]
            return Last_Excuse[NAME_COLUMN_EXCUSES], Last_Excuse.name
    else:
        return "", None

def Log_Excuse(Excuse, Task_Done, Previous_Index=None):

    if Task_Done:
        Task_Done = 'Sí'
    else:
        Task_Done = 'No'

    if os.path.exists(EXCUSE_FILE):
        df = pd.read_excel(EXCUSE_FILE)
    else:
        df = pd.DataFrame(columns=[NAME_COLUMN_TIME_OF_EXCUSE, NAME_COLUMN_EXCUSES, NAME_COLUMN_TASK_DONE_OR_NOT])
    
    if Previous_Index is not None and Previous_Index in df.index:
        df.at[Previous_Index, NAME_COLUMN_TASK_DONE_OR_NOT] = Task_Done
    
    Formatted_Date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    New_Record = pd.DataFrame({NAME_COLUMN_TIME_OF_EXCUSE: [Formatted_Date], NAME_COLUMN_EXCUSES: [Excuse], NAME_COLUMN_TASK_DONE_OR_NOT: ""})
    df = pd.concat([df, New_Record], ignore_index=True)
    df.to_excel(EXCUSE_FILE, index=False)

def Regressive_Count(Minutes = 30):
    Show_Warning()
    Start_Time = datetime.now()
    while (datetime.now() - Start_Time).seconds < 60:
        Password_Input = Request_Password()
        if Password_Input == PASSWORD:
            Previous_Excuse, Previous_Index = Get_Previous_Excuse()
            Excuse, Task_Done = Request_Excuse(Previous_Excuse, MINUTES)
            Log_Excuse(Excuse, Task_Done, Previous_Index)
            Show_Modal_Window("Estado", f"Pusiste bien la contraseña y pospusiste el apagado por {Minutes} minutos. No hagas más trampa que te estoy viendo.")
            return True
    return False

# Loop principal.
Start_Time = datetime.now()
while True:
    Active_Start_Time = datetime.now()
    if Check_If_Now_Is_In_Hour_Range(START_HOUR, END_HOUR):
        if Regressive_Count(Minutes = MINUTES):
            time.sleep(EXTENSION_TIME)
        else:
            Show_Modal_Window("Estado", "Contraseña incorrecta. Cuidadito, pibe, no vaya a ser que te equivoques más seguido.")
            Shutdown()
            break
    time.sleep(60)
