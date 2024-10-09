import subprocess
import os

def Delete_Scheduled_Task(Task_Name: str) -> None:

    """
    Deletes a scheduled task in Windows Task Scheduler by its name.
    
    :param Task_Name: The name of the task in Task Scheduler to be deleted.

    """

    try:
        # Command to delete the scheduled task using schtasks.
        Command = [
            "schtasks", "/delete", "/tn", Task_Name, "/f"  
            # The /f flag forces the deletion without confirmation.
        ]

        # Run the schtasks command.
        subprocess.run(Command, check=True)
        print(f"Tarea programada '{Task_Name}' eliminada con éxito.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error al eliminar la tarea programada: {e}")

def Create_Scheduled_Task(Script_Path: str, Task_Name: str, Interval: int, 
                          Is_Minute: bool = True) -> None:
    
    """
    Creates a scheduled task in Windows Task Scheduler that runs the given 
    script at a specified interval.
    
    :param Script_Path: The full path to the Python script to be scheduled.
    :param Task_Name: The name of the task in Task Scheduler.
    :param Interval: The interval at which the task will run (in minutes or 
    days).
    :param Is_Minute: A boolean that indicates if the interval is in minutes 
    (True) or days (False).

    """
    try:
        # Get the path to the Python interpreter.
        Python_Executable = os.path.join(os.path.dirname(os.__file__), 'python.exe')
        
        # Determine the schedule type and modifier based on Is_Minute.
        Schedule_Type = "MINUTE" if Is_Minute else "DAILY"
        Modifier = str(Interval)

        # Command to create the scheduled task using schtasks.
        Command = [
            "schtasks", "/create", "/tn", Task_Name,
            "/tr", f'"{Python_Executable} {Script_Path}"',  
            # Task action: run Python with the script.
            "/sc", Schedule_Type,  
            # Schedule type: every specified interval.
            "/mo", Modifier,  
            # Modifier: the interval in minutes or days.
            "/st", "00:00",  
            # Start time in HH:MM format.,
            "/rl", "HIGHEST"  
            # Execute with highest privileges.
        ]

        # Run the schtasks command.
        subprocess.run(Command, check=True)
        print(f"Tarea programada '{Task_Name}' creada con éxito para cada {Interval} {'minutos' if Is_Minute else 'días'}.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error al crear la tarea programada: {e}")

# Ruta completa del script actual.
Script_Full_Path = os.path.abspath(__file__)

# Llamar a la función para crear una tarea programada.
Create_Scheduled_Task(Script_Full_Path, "My_Python_Task", Interval = 15, Is_Minute = True)

Delete_Scheduled_Task('Hola')