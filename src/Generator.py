import pandas as pd
import numpy as np
import streamlit as st
from scipy.interpolate import griddata, interp2d

def Reference_Generation(Max_Speed, Requested_Min_Speed, Requested_Max_Speed, Requested_Speed_Step, Speed_Direction, Requested_Min_Torque, Requested_Max_Pc, Requested_Torque_Step, Torque_Direction, Max_Voltage,Requested_Voltage,f, Speed_Limit_Threshold_Type, Speed_Limit_Threshold):
    torques = []
    speeds = []
    speed_limit_fwd = []
    speed_limit_rev = []

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

            Current_Torque_Step = Current_Torque_Step + Requested_Torque_Step*Torque_Direction
        
        if abs(Current_Torque_Step) >= abs(Requested_Max_Torque):

            Current_Torque_Step = Requested_Max_Torque*Torque_Direction

            torques.append(Current_Torque_Step)
            speeds.append(Current_Speed_Step)
            speed_limit_fwd.append(Current_Speed_Limit_Fwd)
            speed_limit_rev.append(Current_Speed_Limit_Rev)
            
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

    speeds.append(0) 
    torques.append(0)
    speed_limit_fwd.append(0)
    speed_limit_rev.append(0)
    
    return speeds, torques, speed_limit_fwd, speed_limit_rev, Voltage  

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

def Profile_Generator(Requested_Profile, Max_Voltage, Requested_Voltage, Requested_Torque_Step, Max_Speed, Requested_Speed_Step, Requested_Min_Speed, Requested_Max_Speed, Requested_Min_Torque, Requested_Max_Torque, Requested_Demanded_Period, Requested_Wait_Period, Voltage_BreakPoints, Speed_BreakPoints, Peak_Torque, Speed_Limit_Threshold_Type, Speed_Limit_Threshold):
    Speed_Ref = []
    Speed_Lim_Fwd = []
    Speed_Lim_Rev = []
    Speed_Max = []
    Torque_Ref = []
    Torque_Max = []
    Requested_Max_Torque = Requested_Max_Torque / 100
    Speed_Limit_Threshold = Speed_Limit_Threshold / 100

    xx, yy = np.meshgrid(Voltage_BreakPoints, Speed_BreakPoints)

    if Requested_Profile == "Q1: Forward Motoring":
        Profile_Order = ["Q1"]
    elif Requested_Profile== "Q2: Reverse Generating":
        Profile_Order = ["Q2"]
    elif Requested_Profile == "Q3: Reverse Motoring":
        Profile_Order = ["Q3"]
    elif Requested_Profile == "Q4: Forward Generating":
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
            S, T, S_Lim_Fwd, S_Lim_Rev, V = Reference_Generation(Max_Speed,Requested_Min_Speed, Requested_Max_Speed, Requested_Speed_Step,Speed_Direction,Requested_Min_Torque,Requested_Max_Torque,Requested_Torque_Step,Torque_Direction,Max_Voltage,Requested_Voltage,f, Speed_Limit_Threshold_Type, Speed_Limit_Threshold)
            S_Max, T_Max, V_Max = Determine_Max_Available(Max_Speed, Requested_Speed_Step,Speed_Direction,Torque_Direction,Max_Voltage,Requested_Voltage,f)

        elif Quadrant == "Q2": 
            Speed_Direction = -1
            Torque_Direction = 1
            f = interp2d(xx, yy*Speed_Direction, Peak_Torque, kind='linear', copy=True, bounds_error=False, fill_value=None)
            S, T, S_Lim_Fwd, S_Lim_Rev, V = Reference_Generation(Max_Speed,Requested_Min_Speed, Requested_Max_Speed, Requested_Speed_Step,Speed_Direction,Requested_Min_Torque,Requested_Max_Torque,Requested_Torque_Step,Torque_Direction,Max_Voltage,Requested_Voltage,f, Speed_Limit_Threshold_Type, Speed_Limit_Threshold)      
            S_Max, T_Max, V_Max = Determine_Max_Available(Max_Speed, Requested_Speed_Step,Speed_Direction,Torque_Direction,Max_Voltage,Requested_Voltage,f)

        elif Quadrant == "Q3":
            Speed_Direction = -1
            Torque_Direction = -1
            f = interp2d(xx, yy*Speed_Direction, Peak_Torque, kind='linear', copy=True, bounds_error=False, fill_value=None)
            S, T, S_Lim_Fwd, S_Lim_Rev, V = Reference_Generation(Max_Speed,Requested_Min_Speed, Requested_Max_Speed, Requested_Speed_Step,Speed_Direction,Requested_Min_Torque,Requested_Max_Torque,Requested_Torque_Step,Torque_Direction,Max_Voltage,Requested_Voltage,f, Speed_Limit_Threshold_Type, Speed_Limit_Threshold)
            S_Max, T_Max, V_Max = Determine_Max_Available(Max_Speed, Requested_Speed_Step,Speed_Direction,Torque_Direction,Max_Voltage,Requested_Voltage,f)

        elif Quadrant == "Q4":
            Speed_Direction = 1
            Torque_Direction = -1
            f = interp2d(xx, yy*Speed_Direction, Peak_Torque, kind='linear', copy=True, bounds_error=False, fill_value=None)
            S, T, S_Lim_Fwd, S_Lim_Rev, V = Reference_Generation(Max_Speed, Requested_Min_Speed, Requested_Max_Speed, Requested_Speed_Step, Speed_Direction, Requested_Min_Torque, Requested_Max_Torque, Requested_Torque_Step, Torque_Direction,Max_Voltage,Requested_Voltage,f, Speed_Limit_Threshold_Type, Speed_Limit_Threshold)
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

        Voltage_Ref = V
    
    return Speed_Ref, Torque_Ref, Speed_Lim_Fwd, Speed_Lim_Rev, Speed_Max, Torque_Max, Voltage_Ref