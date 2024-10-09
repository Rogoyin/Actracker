def Modify_Own_File(Target_Code: str, New_Code: str) -> None:

    with open(__file__, "r") as File:
        Lines = File.readlines()
    
    with open(__file__, "w") as File:
        for Line in Lines:
            if Target_Code in Line:
                Line = Line.replace(Target_Code, New_Code)
            File.write(Line)


Alarm_Duration = 8
User_Alarm_Duration = input("Ingresá la duración de la alarma:")
Modify_Own_File("Alarm_Duration = 8", f"Alarm_Duration = {User_Alarm_Duration}")