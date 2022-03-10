import pandas as pd
import numpy as np
import streamlit as st
from scipy.interpolate import griddata, interp2d
import os

def Reference_Generation(Max_Speed, Requested_Min_Speed, Requested_Max_Speed, Requested_Speed_Step, Speed_Direction, Requested_Min_Torque, Requested_Max_Pc, Requested_Torque_Up_Step, Requested_Torque_Up_Period,Requested_Torque_Down_Period, Torque_Direction, Max_Voltage,Requested_Voltage,f, Speed_Limit_Threshold_Type, Speed_Limit_Threshold, Skip_Max_Torque):
    torques = []
    speeds = []
    speed_limit_fwd = []
    speed_limit_rev = []
    time_torque = []

    Voltage = min(abs(Max_Voltage),abs(Requested_Voltage))

    Current_Speed_Step = Requested_Min_Speed*Speed_Direction

    if Speed_Limit_Threshold_Type == "Percentage":

        Current_Speed_Limit_Fwd = max(Current_Speed_Step*Speed_Limit_Threshold,0)
        Current_Speed_Limit_Rev = min(Current_Speed_Step*Speed_Limit_Threshold,0)
        
    while abs(Current_Speed_Step) <= min(abs(Max_Speed),abs(Requested_Max_Speed)):
        
        Current_Torque_Step = Requested_Min_Torque*Torque_Direction

        Max_Torque_Available = f(Voltage, Current_Speed_Step)
        Requested_Max_Torque = Max_Torque_Available[0] * Requested_Max_Pc
        
        while abs(Current_Torque_Step) < abs(Requested_Max_Torque):

            torques.append(Current_Torque_Step)
            speeds.append(Current_Speed_Step)
            speed_limit_fwd.append(Current_Speed_Limit_Fwd)
            speed_limit_rev.append(Current_Speed_Limit_Rev)
            if Current_Torque_Step >= 0:
                time_torque.append(Requested_Torque_Up_Period)
            else:
                time_torque.append(Requested_Torque_Down_Period)

            Current_Torque_Step = Current_Torque_Step + Requested_Torque_Up_Step*Torque_Direction
        
        if abs(Current_Torque_Step) >= abs(Requested_Max_Torque):
            if Skip_Max_Torque == False:
                Current_Torque_Step = Requested_Max_Torque*Torque_Direction

                torques.append(Current_Torque_Step)
                speeds.append(Current_Speed_Step)
                speed_limit_fwd.append(Current_Speed_Limit_Fwd)
                speed_limit_rev.append(Current_Speed_Limit_Rev)
                if Current_Torque_Step >= 0:
                    time_torque.append(Requested_Torque_Up_Period)
                else:
                    time_torque.append(Requested_Torque_Down_Period)
            
        Current_Speed_Step = Current_Speed_Step + Requested_Speed_Step*Speed_Direction

        if Speed_Limit_Threshold_Type == "Percentage":

            Current_Speed_Limit_Fwd = max(Current_Speed_Step*Speed_Limit_Threshold,0)
            Current_Speed_Limit_Rev = min(Current_Speed_Step*Speed_Limit_Threshold,0)

    if abs(Current_Speed_Step) == min(abs(Max_Speed),abs(Requested_Max_Speed)):

        Max_Torque_Available = f(Requested_Voltage, Current_Speed_Step)
        Requested_Max_Torque = Max_Torque_Available[0] * Requested_Max_Pc

        Current_Speed_Step = Requested_Max_Speed*Speed_Direction
        
        if Speed_Limit_Threshold_Type == "Percentage":
            Current_Speed_Limit_Fwd = max(Current_Speed_Step*Speed_Limit_Threshold,0)
            Current_Speed_Limit_Rev = min(Current_Speed_Step*Speed_Limit_Threshold,0)
            
        torques.append(Current_Torque_Step)
        speeds.append(Current_Speed_Step)
        speed_limit_fwd.append(Current_Speed_Limit_Fwd)
        speed_limit_rev.append(Current_Speed_Limit_Rev)
        if Current_Torque_Step >= 0:
            time_torque.append(Requested_Torque_Up_Period)
        else:
            time_torque.append(Requested_Torque_Down_Period)

    speeds.append(0) 
    torques.append(0)
    speed_limit_fwd.append(0)
    speed_limit_rev.append(0)
    time_torque.append(0)

    return speeds, torques, speed_limit_fwd, speed_limit_rev, time_torque, Voltage  

def Determine_Max_Available(Max_Speed, Requested_Speed_Step, Speed_Direction, Torque_Direction, Max_Voltage,Requested_Voltage,f):
    torques = []
    speeds = []
    Voltage = min(abs(Max_Voltage),abs(Requested_Voltage))

    Current_Speed_Step = 0
    speeds.append(Current_Speed_Step) 
    torques.append(0)

    while abs(Current_Speed_Step) <= abs(Max_Speed):

        Max_Torque_Available = f(Voltage, Current_Speed_Step)
        Max_Torque_Available = Max_Torque_Available[0]*Torque_Direction

        torques.append(Max_Torque_Available)
        speeds.append(Current_Speed_Step)

        Current_Speed_Step = Current_Speed_Step + Requested_Speed_Step*Speed_Direction

    if abs(Current_Speed_Step) == abs(Max_Speed):

        Max_Torque_Available = f(Voltage, Current_Speed_Step)
        Max_Torque_Available = Max_Torque_Available[0]*Torque_Direction

        Current_Speed_Step = Max_Speed*Speed_Direction
        
        torques.append(Max_Torque_Available)
        speeds.append(Current_Speed_Step)
    
    speeds.append(Max_Speed*Speed_Direction) 
    torques.append(0)

    speeds.append(0) 
    torques.append(0)

    return speeds, torques, Voltage

def Profile_Generator(Requested_Profile, Max_Voltage, Requested_Voltage, Requested_Torque_Up_Step, Max_Speed, Requested_Speed_Step, Requested_Min_Speed, Requested_Max_Speed, Requested_Min_Torque, Requested_Max_Torque,  Requested_Torque_Up_Period,Requested_Torque_Down_Period,Requested_Wait_Period, Voltage_BreakPoints, Speed_BreakPoints, Peak_Torque, Speed_Limit_Threshold_Type, Speed_Limit_Threshold, Skip_Max_Torque):
    Speed_Ref = []
    Speed_Lim_Fwd = []
    Speed_Lim_Rev = []
    Speed_Max = []
    Torque_Ref = []
    Torque_Max = []
    Torque_Period = []
    Requested_Max_Torque = Requested_Max_Torque / 100
    Speed_Limit_Threshold = Speed_Limit_Threshold / 100

    xx, yy = np.meshgrid(Voltage_BreakPoints, Speed_BreakPoints)

    if Requested_Profile == "Forward Motoring":
        Profile_Order = ["Q1"]
    elif Requested_Profile== "Reverse Generating":
        Profile_Order = ["Q2"]
    elif Requested_Profile == "Reverse Motoring":
        Profile_Order = ["Q3"]
    elif Requested_Profile == "Forward Generating":
        Profile_Order = ["Q4"]
    elif Requested_Profile == "Motoring":
        Profile_Order = ["Q1", "Q3"]
    elif Requested_Profile == "Generating":
        Profile_Order = ["Q2", "Q4"]
    elif Requested_Profile == "Forward":
        Profile_Order = ["Q1", "Q4"]
    elif Requested_Profile == "Reverse":
        Profile_Order = ["Q2", "Q3"]
    elif Requested_Profile == "All":
        Profile_Order = ["Q1", "Q2", "Q3","Q4"]

    for Quadrant in Profile_Order:

        if Quadrant == "Q1":
            
            Speed_Direction = 1
            Torque_Direction = 1
            f = interp2d(xx, yy*Speed_Direction, Peak_Torque, kind='linear', copy=True, bounds_error=False, fill_value=None)
            S, T, S_Lim_Fwd, S_Lim_Rev, Time_Torque, V = Reference_Generation(Max_Speed,Requested_Min_Speed, Requested_Max_Speed, Requested_Speed_Step,Speed_Direction,Requested_Min_Torque,Requested_Max_Torque,Requested_Torque_Up_Step, Requested_Torque_Up_Period,Requested_Torque_Down_Period, Torque_Direction,Max_Voltage,Requested_Voltage,f, Speed_Limit_Threshold_Type, Speed_Limit_Threshold,Skip_Max_Torque)
            S_Max, T_Max, V_Max = Determine_Max_Available(Max_Speed, Requested_Speed_Step,Speed_Direction,Torque_Direction,Max_Voltage,Requested_Voltage,f)

        elif Quadrant == "Q2": 
            Speed_Direction = -1
            Torque_Direction = 1
            f = interp2d(xx, yy*Speed_Direction, Peak_Torque, kind='linear', copy=True, bounds_error=False, fill_value=None)
            S, T, S_Lim_Fwd, S_Lim_Rev, Time_Torque, V  = Reference_Generation(Max_Speed,Requested_Min_Speed, Requested_Max_Speed, Requested_Speed_Step,Speed_Direction,Requested_Min_Torque,Requested_Max_Torque,Requested_Torque_Up_Step, Requested_Torque_Up_Period,Requested_Torque_Down_Period,Torque_Direction,Max_Voltage,Requested_Voltage,f, Speed_Limit_Threshold_Type, Speed_Limit_Threshold,Skip_Max_Torque)      
            S_Max, T_Max, V_Max = Determine_Max_Available(Max_Speed, Requested_Speed_Step,Speed_Direction,Torque_Direction,Max_Voltage,Requested_Voltage,f)

        elif Quadrant == "Q3":
            Speed_Direction = -1
            Torque_Direction = -1
            f = interp2d(xx, yy*Speed_Direction, Peak_Torque, kind='linear', copy=True, bounds_error=False, fill_value=None)
            S, T, S_Lim_Fwd, S_Lim_Rev, Time_Torque, V  = Reference_Generation(Max_Speed,Requested_Min_Speed, Requested_Max_Speed, Requested_Speed_Step,Speed_Direction,Requested_Min_Torque,Requested_Max_Torque,Requested_Torque_Up_Step, Requested_Torque_Up_Period,Requested_Torque_Down_Period,Torque_Direction,Max_Voltage,Requested_Voltage,f, Speed_Limit_Threshold_Type, Speed_Limit_Threshold,Skip_Max_Torque)
            S_Max, T_Max, V_Max = Determine_Max_Available(Max_Speed, Requested_Speed_Step,Speed_Direction,Torque_Direction,Max_Voltage,Requested_Voltage,f)

        elif Quadrant == "Q4":
            Speed_Direction = 1
            Torque_Direction = -1
            f = interp2d(xx, yy*Speed_Direction, Peak_Torque, kind='linear', copy=True, bounds_error=False, fill_value=None)
            S, T, S_Lim_Fwd, S_Lim_Rev, Time_Torque, V  = Reference_Generation(Max_Speed, Requested_Min_Speed, Requested_Max_Speed, Requested_Speed_Step, Speed_Direction, Requested_Min_Torque, Requested_Max_Torque, Requested_Torque_Up_Step, Requested_Torque_Up_Period,Requested_Torque_Down_Period, Torque_Direction,Max_Voltage,Requested_Voltage,f, Speed_Limit_Threshold_Type, Speed_Limit_Threshold,Skip_Max_Torque)
            S_Max, T_Max, V_Max = Determine_Max_Available(Max_Speed, Requested_Speed_Step,Speed_Direction,Torque_Direction,Max_Voltage,Requested_Voltage,f)

        for speed in S:
            Speed_Ref.append(speed)
        for speed in S_Lim_Fwd:
            Speed_Lim_Fwd.append(speed)
        for speed in S_Lim_Rev:
            Speed_Lim_Rev.append(speed)
        for speed in S_Max:
            Speed_Max.append(speed)

        for torque in T:
            Torque_Ref.append(torque)
        for torque in T_Max:
            Torque_Max.append(torque)

        for time in Time_Torque:
            Torque_Period.append(time)

        Voltage_Ref = V
    
    return Speed_Ref, Torque_Ref, Speed_Lim_Fwd, Speed_Lim_Rev, Speed_Max, Torque_Max, Torque_Period, Voltage_Ref

def Generate_Torque_Speed(Test_Name,Export_Path,Export_Name,Export_Format,Logging_Path, DCDC_Ixxat_Id, MCU_Ixxat_Id, Dyno_Ip, Dyno_Port, Dyno_Id, DCDC_V_Target, Speed_Demands,Speed_Lim_Fwd, Speed_Lim_Rev,Torque_Demands,Torque_Time):
    Script = []
    DCDC_I_Lim_Pos = 400
    DCDC_I_Lim_Neg = -400

    Script.append("##### Test Setup ######")
    Script.append("# Name: " + str(Test_Name))
    Script.append("# Log Directory: " + str(st.session_state.Logging_Path))
    Script.append("")
    Script.append("##### Inverter ######")
    Script.append("# Project: " + str(st.session_state.Requested_Project))
    Script.append("# Sample Letter: " + str(st.session_state.Inverter_SampleLetter))
    Script.append("# Sample Number: " + str(st.session_state.Inverter_SampleNumber))
    Script.append("# Notes: " + str(st.session_state.Inverter_Note))
    Script.append("")
    Script.append("##### Motor ######")
    Script.append("# Manufacturer: " + str(st.session_state.Motor_Manufacturer))
    Script.append("# Sample Letter: " + str(st.session_state.Motor_SampleLetter))
    Script.append("# Sample Number: " + str(st.session_state.Motor_SampleNumber))
    Script.append("# Notes: " + str(st.session_state.Motor_Note))
    Script.append("")
    Script.append("##### Software ######")
    Script.append("# Commit: " + str(st.session_state.Soft_Commit))
    Script.append("# Ke: " + str(st.session_state.Soft_Ke))
    Script.append("# Offset: " + str(st.session_state.Soft_Offset))
    Script.append("")
    Script.append("##### Dynamometer ######")
    Script.append("# Location: " + str(st.session_state.Dyno_Location))
    Script.append("# IP Address: " + str(st.session_state.Dyno_Ip))
    Script.append("# Port: " + str(st.session_state.Dyno_Port))
    Script.append("# ID: " + str(st.session_state.Dyno_Id))
    Script.append("")
    Script.append("##### CAN Hardware ######")
    Script.append("# DCDC Ixxat ID: " + str(st.session_state.CAN_ID_DCDC))
    Script.append("# MCU Ixxat ID: " + str(st.session_state.CAN_ID_MCU))
    Script.append("")
    Script.append("##### Test ######")
    Script.append("# Test Type: " + str(st.session_state.Requested_Type))
    Script.append("# Test Profile: " + str(st.session_state.Requested_Profile))
    Script.append("")
    Script.append("##### DCDC ######")
    Script.append("# Target DC Link Voltage: " + str(st.session_state.Requested_Voltage))
    Script.append("# DC Link Current Limit Positive: " + str(st.session_state.Requested_I_Lim_Pos))
    Script.append("# DC Link Current Limit Negative: " + str(st.session_state.Requested_I_Lim_Neg))
    Script.append("")
    Script.append("##### Speed ######")
    Script.append("# Minimum Speed abs(rpm): " + str(st.session_state.Requested_Min_Speed))
    Script.append("# Speed Step Size abs(rpm): " + str(st.session_state.Requested_Speed_Step))
    Script.append("# Maximum speed abs(rpm): " + str(st.session_state.Requested_Max_Speed))
    Script.append("# Speed Limit Type: " + str(st.session_state.Requested_Speed_Limit_Type))
    Script.append("# Value of Speed Limit: " + str(st.session_state.Requested_Speed_Limit))
    Script.append("")
    Script.append("##### Torque ######")
    Script.append("# Minimum Torque abs(Nm): " + str(st.session_state.Requested_Min_Torque))
    Script.append("# Torque Step Size (Nm): " + str(st.session_state.Requested_Torque_Up_Step))
    Script.append("# Maximum Torque (% of peak): " + str(st.session_state.Requested_Max_Torque))
    Script.append("# Skip Last Torque Demand per speed point?: " + str(st.session_state.Skip_Max_Torque))
    Script.append("")
    Script.append("##### Time ######")
    Script.append("# Torque Demand time (s): " + str(st.session_state.Requested_Torque_Up_Period))
    Script.append("# Wait Period (s): " + str(st.session_state.Requested_Wait_Period))
    Script.append("")
    Script.append("#****** START OF TEST SCRIPT ******")

    Script.append("DCDC_I_Lim_Pos = "+str(DCDC_I_Lim_Pos))
    Script.append("DCDC_I_Lim_Neg = "+str(DCDC_I_Lim_Neg))
    Script.append("")
    Script.append("DCDC.setOutputCurrentLimits(DCDC_I_Lim_Pos,DCDC_I_Lim_Neg)")
    Script.append("DCDC.setOutputEnabled(True)")
    Script.append("DCDC.setOutputVoltage("+str(DCDC_V_Target)+")")
    Script.append("")
    Script.append("print(str(Wait while DCDC raises to desired level))")
    Script.append("time.sleep(2)")
    Script.append("DCDC.getOutputVoltage()")
    Script.append("")

    for i in range(0, len(Speed_Demands)):
        Script.append("MCU.setSpeedLimits("+str(min(Speed_Lim_Rev[i],0))+","+str(max(Speed_Lim_Fwd[i],0))+")")
        Script.append("Dyno_setSpeed("+str(Speed_Demands[i])+")")
        Script.append("MCUsetTorqueDemand("+str(Torque_Demands[i])+")")
        Script.append("MCU.getTorque()")
        Script.append("time.sleep("+str(Torque_Time[i])+")")
        i = i+1

    Script.append("MCU.setTorqueDemand(0)")

    File_Name = Export_Path+Export_Name+Export_Format
    if os.path.exists(File_Name):
        f=open(File_Name, 'w')
        f.writelines("%s\n" % i for i in Script)
        f.close()
    else:
        f=open(File_Name, 'w')
        f.writelines("%s\n" % i for i in Script)
        f.close()