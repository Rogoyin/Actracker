# Importar bibliotecas
import pandas as pd
import numpy as np
import tkinter as tk
import datetime as dt
import sys
import time

# Agregar ruta para módulos adicionales
sys.path.append('c:/Users/tomas/Documents/Programación/Github/Patricionog/Modulio')

# Importar módulos adicionales
import Appio as ap
import Archivio as ac
import Databasio as bd
import Datetimio as dm
import Dictio as dc
import Excelio as ex
import Footio as ft
import Foragio as fg
import Framio as fr
import Graphio as gr
import Highlightio as hg
import Inputio as ip
import Listio as ls
import Mathio as mt
import Notio as nt
import Numbio as nb
import Numpio as nm
import Stringio as st
import Timio as tm
import Tkintio as tn
import Toolio as to

# Minutos del período
Minutes_Period = 1

# Tolerancia.
Time_Error = 1

# Definir columnas
INICIO = 'Inicio'
FINAL = 'Final'
PLAN_PREVISTO = 'Plan_Previsto'
ACTIVIDAD_REALIZADA = 'Actividad_Realizada'
EXPLICACION = 'Explicación'

# Función para deshabilitar eventos
def Disable_Event():
    pass  

# Función para manejar cuando se ha hecho la actividad
def Press_Done():
    global df, Last_Row_Index
        
    df.loc[Last_Row_Index, ACTIVIDAD_REALIZADA] = df.loc[Last_Row_Index, PLAN_PREVISTO]
    df.loc[Last_Row_Index, EXPLICACION] = 'Soy un crack' 
    Open_Promise_Window()

# Función para manejar cuando no se ha hecho la actividad
def Press_Undone():
    global Window
    Open_Activity_Window()

# Función para abrir la ventana de actividad
def Open_Activity_Window():
    global Window, df, Last_Row_Index
    Activity_Window = tk.Toplevel(Window) 
    Activity_Window.title("Actividad realizada")
    Activity_Window.geometry("300x200")
    
    Activity_Window.grab_set()         
    Activity_Window.transient(Window)  
    Activity_Window.protocol("WM_DELETE_WINDOW", Disable_Event)

    Label = tk.Label(Activity_Window, text="¿Qué hiciste en lugar de lo previsto?")
    Label.pack(pady=20)

    Justification_Box = tk.Entry(Activity_Window)
    Justification_Box.pack(pady=10)

    def Press_Close():
        global df, Last_Row_Index
        df.loc[Last_Row_Index, EXPLICACION] = Justification_Box.get()
        Activity_Window.destroy()
        Open_Promise_Window()

    Close_Button = tk.Button(Activity_Window, text="Close", command=Press_Close)
    Close_Button.pack()

    Window.wait_window(Activity_Window)

# Función para abrir la ventana de promesa
def Open_Promise_Window():
    global Window, Minutes_Period

    Promise_Window = tk.Toplevel(Window) 
    Promise_Window.title("Additional Information")
    Promise_Window.geometry("300x200")
    
    Promise_Window.grab_set()         
    Promise_Window.transient(Window)  
    Promise_Window.protocol("WM_DELETE_WINDOW", Disable_Event)

    Label = tk.Label(Promise_Window, text=f"¿Qué vas a hacer en los próximos {Minutes_Period} minutos?")
    Label.pack(pady=20)

    Promise_Box = tk.Entry(Promise_Window)
    Promise_Box.pack(pady=10)

    def Press_Promise():
        global df, Last_Row_Index, Minutes_Period, End_Last_Period, Now_Minus_Period, Difference_Minutes
        global INICIO, FINAL, PLAN_PREVISTO, ACTIVIDAD_REALIZADA, EXPLICACION
        
        if Difference_Minutes >= Time_Error or len(df) < 1:
            Current_Date_Time = dm.Add_Time_Delta()
            Future_Date_Time = dm.Add_Time_Delta(Minutes_Period)

            Period = {
                INICIO: Current_Date_Time,
                FINAL: Future_Date_Time,
                PLAN_PREVISTO: Promise_Box.get(),
                ACTIVIDAD_REALIZADA: '-',
                EXPLICACION: '-'
            }
        
            df = fr.Add_Row_To_DataFrame(Period, df, Fill='-')
        
        else:  
            Inicio = df.loc[Last_Row_Index, INICIO]
            Final = df.loc[Last_Row_Index, FINAL]

            Period = {INICIO: Inicio,
                      FINAL: Final,
                      PLAN_PREVISTO: Promise_Box.get(),
                      ACTIVIDAD_REALIZADA: '-',
                      EXPLICACION: '-'
                    }
        
            df = fr.Add_Row_To_DataFrame(Period, df, Fill='-')

        Window.destroy()

    Promise_Button = tk.Button(Promise_Window, text="Promise", command=Press_Promise)
    Promise_Button.pack()

    Window.wait_window(Promise_Window)


##################
### PROGRAMA #####
##################

# Función para ejecutar la lógica principal.
def Run_Main_Logic():

    global df, Window, End_Last_Period, Now_Minus_Period, Time_Error, Last_Row_Index, Difference_Minutes
    
    # Cargar base de datos
    df = pd.read_excel('Periods.xlsx')
    
    # Índice de la última fila
    if len(df) == 1:
        Last_Row_Index = 0
    else:
        Last_Row_Index = len(df) - 1

    # Calcular el tiempo desde ahora hacia atrás con el período elegido.
    Now_Minus_Period = dt.datetime.now() - dt.timedelta(minutes=Minutes_Period)

    # Si el df no está vacío, busca el final del período en la última fila.
    if len(df) > 0:
        End_Last_Period = df.loc[Last_Row_Index, FINAL]  # Obtener el final del período
      
        # Verificar si End_Last_Period es un objeto Timestamp
        if isinstance(End_Last_Period, pd.Timestamp):
            
            End_Last_Period = End_Last_Period.to_pydatetime() 
        elif isinstance(End_Last_Period, str):
            try:
                End_Last_Period = dt.datetime.strptime(End_Last_Period, '%Y-%m-%d %H:%M')
            except ValueError as e:
                print(f"Error al convertir la cadena a datetime: {e}")  
                End_Last_Period = None
                
        else:
            print(f"Tipo de dato inesperado: {type(End_Last_Period)}")    
    else:
        
        End_Last_Period = Now_Minus_Period
        

    Difference = Now_Minus_Period - End_Last_Period
    
    Difference_Minutes = round(Difference.total_seconds() / 60)
    
    if Difference_Minutes <= Time_Error and len(df) > 0:

        Window = tk.Tk()
        Window.title("Pasaron los quince...")
        Window.geometry("400x300")

        Etiqueta = tk.Label(Window, text=f"Este era tu plan: \n\n {df[PLAN_PREVISTO][Last_Row_Index]} \n\n ¿Lo hiciste?")
        Etiqueta.pack()

        Yes_Button = tk.Button(Window, text="Sí", command=Press_Done)
        Yes_Button.pack()

        No_Button = tk.Button(Window, text="No", command=Press_Undone)
        No_Button.pack()

        Window.mainloop()

    else:
        Window = tk.Tk()
        Window.title("Se inicia un nuevo período.")
        Window.geometry("400x300")

        Etiqueta = tk.Label(Window, text=f"Arranque, maestro.")
        Etiqueta.pack()

        def Press_Start():           
            Open_Promise_Window()

        Start_Button = tk.Button(Window, text = "Empezar", command = Press_Start)
        Start_Button.pack()

        Window.mainloop()

    # Reemplazar cualquier valor no válido (como '-') por NaT antes de convertir a datetime
    df[FINAL] = pd.to_datetime(df[FINAL].replace('-', pd.NaT), format='%Y-%m-%d %H:%M', errors='coerce')

    # Guardar en excel.
    df[INICIO] = pd.to_datetime(df[INICIO]).dt.strftime('%Y-%m-%d %H:%M')  
    df[FINAL] = pd.to_datetime(df[FINAL]).dt.strftime('%Y-%m-%d %H:%M')    
    df.to_excel('Periods.xlsx', index=False)

    ex.Adjust_Column_Width('Periods.xlsx', 1, 2, 25)
    ex.Adjust_Column_Width('Periods.xlsx', 3, 5, 40)
    ex.Formating_Book('Periods.xlsx')

# Función para mantener la ejecución continua
def Run_Continuously():
    while True:  # Loop indefinitely.
        Run_Main_Logic()  # Execute the main logic.
        time.sleep(Minutes_Period * 60)  # Wait for the specified period.

# Iniciar el ciclo continuo de la lógica.
Run_Continuously() 