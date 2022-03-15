import pandas as pd
import numpy as np
import streamlit as st
from scipy.interpolate import griddata, interp2d
import os

def genRef(torqueDir, torqueMaxPc, torqueMinVal, torqueStepUp, torqueStepDown, torqueDemandPeriodUp, torqueDemandPeriodDown, torqueSkipLast, speedDir, speedMaxTable, speedMaxReq, speedMin, speedStepUp, speedStepDown, speedLimMethod, speedLimThreshold, voltageRef, f):
    torqueDemand = []
    torqueDemandPeriod = []
    speedDemand = []
    speedLimFwd = []
    speedLimRev = []
    
    # Torque 
    torqueMax = torqueMaxPc * torqueDir
    torqueMin = torqueMinVal * torqueDir
    torqueStepUp = torqueStepUp * torqueDir
    torqueStepDown = torqueStepDown * torqueDir

    # Speed
    speedLimFwdThreshold = speedLimThreshold
    speedLimRevThreshold = speedLimThreshold

    speedStepCurrent = speedMin * speedDir

    if speedLimMethod == "Percentage":
        speedLimFwdCurrent = max(speedStepCurrent*speedLimFwdThreshold, 0) 
        speedLimRevCurrent = min(speedStepCurrent*speedLimRevThreshold, 0)

    speedMax = min(abs(speedMaxTable),abs(speedMaxReq)) * speedDir
    
    # Start of Loop
    while abs(speedStepCurrent) <= abs(speedMax):
        
        # Get Torque Max value after percentage gain applied
        torqueMaxAvail = f(voltageRef, speedStepCurrent)
        torqueMaxAvail = torqueMaxAvail[0] * torqueMax
        
        # Every speed step, start torque from minimum torque step
        torqueStepCurrent = torqueMin
        
        if torqueDir > 0:
        # Start torque increment
            while torqueStepCurrent < torqueMaxAvail:
                
                # Store current values
                torqueDemand.append(torqueStepCurrent)
                torqueDemandPeriod.append(torqueDemandPeriodUp)
                speedDemand.append(speedStepCurrent)
                speedLimFwd.append(speedLimFwdCurrent)
                speedLimRev.append(speedLimRevCurrent)

                # Step torque up using requested torque step
                torquePrevStep = torqueStepCurrent
                torqueStepCurrent = torqueStepCurrent + torqueStepUp

            if (torqueStepCurrent >= torqueMaxAvail) and (torqueSkipLast == False):

                torqueStepCurrent = torqueMaxAvail

                # Store current values
                torqueDemand.append(torqueStepCurrent)
                torqueDemandPeriod.append(torqueDemandPeriodUp)
                speedDemand.append(speedStepCurrent)
                speedLimFwd.append(speedLimFwdCurrent)
                speedLimRev.append(speedLimRevCurrent)

                while torqueStepCurrent > torqueMin:

                    torqueStepCurrent = torqueStepCurrent - torqueStepDown

                    if torqueStepCurrent <= torqueMin:

                        torqueStepCurrent = 0

                        # Store current values
                        torqueDemand.append(torqueStepCurrent)
                        torqueDemandPeriod.append(torqueDemandPeriodUp)
                        speedDemand.append(speedStepCurrent)
                        speedLimFwd.append(speedLimFwdCurrent)
                        speedLimRev.append(speedLimRevCurrent)

                    # Store current values
                    torqueDemand.append(torqueStepCurrent)
                    torqueDemandPeriod.append(torqueDemandPeriodUp)
                    speedDemand.append(speedStepCurrent)
                    speedLimFwd.append(speedLimFwdCurrent)
                    speedLimRev.append(speedLimRevCurrent)

            else:
                torqueStepCurrent = torquePrevStep

                while torqueStepCurrent > torqueMin:

                    torqueStepCurrent = torqueStepCurrent - torqueStepDown

                    if torqueStepCurrent <= torqueMin:

                        torqueStepCurrent = 0

                        # Store current values
                        torqueDemand.append(torqueStepCurrent)
                        torqueDemandPeriod.append(torqueDemandPeriodUp)
                        speedDemand.append(speedStepCurrent)
                        speedLimFwd.append(speedLimFwdCurrent)
                        speedLimRev.append(speedLimRevCurrent)

                    # Store current values
                    torqueDemand.append(torqueStepCurrent)
                    torqueDemandPeriod.append(torqueDemandPeriodUp)
                    speedDemand.append(speedStepCurrent)
                    speedLimFwd.append(speedLimFwdCurrent)
                    speedLimRev.append(speedLimRevCurrent)

                if torqueStepCurrent <= torqueMin:

                    torqueStepCurrent = 0

                    # Store current values
                    torqueDemand.append(torqueStepCurrent)
                    torqueDemandPeriod.append(torqueDemandPeriodUp)
                    speedDemand.append(speedStepCurrent)
                    speedLimFwd.append(speedLimFwdCurrent)
                    speedLimRev.append(speedLimRevCurrent)
        
        if torqueDir < 0:
        
        # Start torque increment
            
            while torqueStepCurrent > torqueMaxAvail:
                # Store current values
                torqueDemand.append(torqueStepCurrent)
                torqueDemandPeriod.append(torqueDemandPeriodUp)
                speedDemand.append(speedStepCurrent)
                speedLimFwd.append(speedLimFwdCurrent)
                speedLimRev.append(speedLimRevCurrent)

                # Step torque up using requested torque step
                torquePrevStep = torqueStepCurrent
                torqueStepCurrent = torqueStepCurrent + torqueStepUp

            if (torqueStepCurrent <= torqueMaxAvail) and (torqueSkipLast == False):
                
                torqueStepCurrent = torqueMaxAvail
                
                # Store current values
                torqueDemand.append(torqueStepCurrent)
                torqueDemandPeriod.append(torqueDemandPeriodUp)
                speedDemand.append(speedStepCurrent)
                speedLimFwd.append(speedLimFwdCurrent)
                speedLimRev.append(speedLimRevCurrent)
                
                while torqueStepCurrent < torqueMin:

                    torqueStepCurrent = torqueStepCurrent - torqueStepDown

                    if torqueStepCurrent >= torqueMin:

                        torqueStepCurrent = 0

                        # Store current values
                        torqueDemand.append(torqueStepCurrent)
                        torqueDemandPeriod.append(torqueDemandPeriodUp)
                        speedDemand.append(speedStepCurrent)
                        speedLimFwd.append(speedLimFwdCurrent)
                        speedLimRev.append(speedLimRevCurrent)

                    # Store current values
                    torqueDemand.append(torqueStepCurrent)
                    torqueDemandPeriod.append(torqueDemandPeriodUp)
                    speedDemand.append(speedStepCurrent)
                    speedLimFwd.append(speedLimFwdCurrent)
                    speedLimRev.append(speedLimRevCurrent)
                
            else:
                
                torqueStepCurrent = torquePrevStep

                while torqueStepCurrent < torqueMin:

                    torqueStepCurrent = torqueStepCurrent - torqueStepDown

                    if torqueStepCurrent >= torqueMin:

                        torqueStepCurrent = 0

                        # Store current values
                        torqueDemand.append(torqueStepCurrent)
                        torqueDemandPeriod.append(torqueDemandPeriodUp)
                        speedDemand.append(speedStepCurrent)
                        speedLimFwd.append(speedLimFwdCurrent)
                        speedLimRev.append(speedLimRevCurrent)

                    # Store current values
                    torqueDemand.append(torqueStepCurrent)
                    torqueDemandPeriod.append(torqueDemandPeriodUp)
                    speedDemand.append(speedStepCurrent)
                    speedLimFwd.append(speedLimFwdCurrent)
                    speedLimRev.append(speedLimRevCurrent)
        
        speedStepCurrent = speedStepCurrent + speedStepUp * speedDir
        
        
        if speedLimMethod == "Percentage":
            speedLimFwdCurrent = max(speedStepCurrent*speedLimFwdThreshold, 0) 
            speedLimRevCurrent = min(speedStepCurrent*speedLimRevThreshold, 0)

    ref = pd.DataFrame(data = {"torqueDemand":torqueDemand,"torqueDemandPeriod":torqueDemandPeriod,"speedDemand":speedDemand,"speedLimFwd":speedLimFwd,"speedLimRev":speedLimFwd})

    return ref

def genEnv(torqueDir, torquePeak, speedDir, speedBreakpoints, voltageRef, f):

    torqueEnv = []
    speedEnv = []
    i = 0

    #torqueMax = torquePeak * torqueDir
    speedMax = max(speedBreakpoints) * speedDir
    envSpeed = np.linspace ( 0, max(speedBreakpoints) * speedDir, 50 )
    
    speedEnv.append(0) 
    torqueEnv.append(0)
    
    speedStepCurrent = 0
    torqueMaxAvail = 0

    for speeds in  envSpeed:

        torqueMaxAvailable = f(voltageRef, speeds)
        torqueMaxAvail = torqueMaxAvailable[0]

        torqueEnv.append(torqueMaxAvail*torqueDir)
        speedEnv.append(speeds)

    speedEnv.append(speedMax) 
    torqueEnv.append(0)


    speedEnv.append(0) 
    torqueEnv.append(0)

    env = pd.DataFrame(data = {"torqueEnv":torqueEnv,"speedEnv":speedEnv})    

    return env

def genProfile(profile, torquePeak, torqueMaxPcIn, torqueMinVal, torqueStepUp, torqueStepDown, torqueDemandPeriodUp, torqueDemandPeriodDown, torqueSkipLast, speedMaxTable, speedMaxReq, speedMin, speedStepUp, speedStepDown, speedLimMethod, speedLimThresholdIn, speedBreakpoints, voltageBreakpoints, voltageRef):

    torqueMaxPc = torqueMaxPcIn / 100
    speedLimThreshold = speedLimThresholdIn / 100

    InitCount = 0

    refInit = pd.DataFrame(data = {"torqueDemand":[],"torqueDemandPeriod":[],"speedDemand":[],"speedLimFwd":[],"speedLimRev":[]})
    
    xx, yy = np.meshgrid(voltageBreakpoints, speedBreakpoints)

    if profile          == "Forward Motoring":
        profileOrder    = ["Q1"]

    elif profile        == "Reverse Generating":
        profileOrder    = ["Q2"]

    elif profile        == "Reverse Motoring":
        profileOrder    = ["Q3"]

    elif profile        == "Forward Generating":
        profileOrder    = ["Q4"]

    elif profile        == "Motoring":
        profileOrder    = ["Q1", "Q3"]

    elif profile        == "Generating":
        profileOrder    = ["Q2", "Q4"]

    elif profile        == "Forward":
        profileOrder    = ["Q1", "Q4"]

    elif profile        == "Reverse":
        profileOrder    = ["Q2", "Q3"]

    elif profile        == "All":
        profileOrder    = ["Q1", "Q2", "Q3","Q4"]

    for quadrant in profileOrder:

        if quadrant == "Q1":
            
            speedDir    = 1
            torqueDir   = 1
            f           = interp2d(xx, yy*speedDir, torquePeak, kind='linear', copy=True, bounds_error=False, fill_value=None)
            ref         = genRef(torqueDir, torqueMaxPc, torqueMinVal, torqueStepUp, torqueStepDown, torqueDemandPeriodUp, torqueDemandPeriodDown, torqueSkipLast, speedDir, speedMaxTable, speedMaxReq, speedMin, speedStepUp, speedStepDown, speedLimMethod, speedLimThreshold, voltageRef, f)

        elif quadrant == "Q2": 
            speedDir    = -1
            torqueDir   = 1
            f           = interp2d(xx, yy*speedDir, torquePeak, kind='linear', copy=True, bounds_error=False, fill_value=None)
            ref         = genRef(torqueDir, torqueMaxPc, torqueMinVal, torqueStepUp, torqueStepDown, torqueDemandPeriodUp, torqueDemandPeriodDown, torqueSkipLast, speedDir, speedMaxTable, speedMaxReq, speedMin, speedStepUp, speedStepDown, speedLimMethod, speedLimThreshold, voltageRef, f)

        elif quadrant == "Q3":
            speedDir    = -1
            torqueDir   = -1
            f           = interp2d(xx, yy*speedDir, torquePeak, kind='linear', copy=True, bounds_error=False, fill_value=None)
            ref         = genRef(torqueDir, torqueMaxPc, torqueMinVal, torqueStepUp, torqueStepDown, torqueDemandPeriodUp, torqueDemandPeriodDown, torqueSkipLast, speedDir, speedMaxTable, speedMaxReq, speedMin, speedStepUp, speedStepDown, speedLimMethod, speedLimThreshold, voltageRef, f)

        elif quadrant == "Q4":
            speedDir    = 1
            torqueDir   = -1
            f           = interp2d(xx, yy*speedDir, torquePeak, kind='linear', copy=True, bounds_error=False, fill_value=None)
            ref         = genRef(torqueDir, torqueMaxPc, torqueMinVal, torqueStepUp, torqueStepDown, torqueDemandPeriodUp, torqueDemandPeriodDown, torqueSkipLast, speedDir, speedMaxTable, speedMaxReq, speedMin, speedStepUp, speedStepDown, speedLimMethod, speedLimThreshold, voltageRef, f)

        if InitCount    == 0:

            ref_out     = pd.concat([refInit,ref], ignore_index =True)
            InitCount   = 1

        else:

            ref_out     = pd.concat([ref_out, ref], ignore_index =True)

    return ref_out

def genEnvolope(torquePeak, speedBreakpoints, voltageBreakpoints, voltageRef):
    
    InitCount = 0
    envInit = pd.DataFrame(data = {"torqueEnv":[],"speedEnv":[]})
    
    xx, yy = np.meshgrid(voltageBreakpoints, speedBreakpoints)

    profileOrder    = ["Q1", "Q2", "Q3","Q4"]

    for quadrant in profileOrder:

        if quadrant == "Q1":
            
            speedDir    = 1
            torqueDir   = 1
            f           = interp2d(xx, yy*speedDir, torquePeak, kind='linear', copy=True, bounds_error=False, fill_value=None)
            env         = genEnv(torqueDir, torquePeak, speedDir, speedBreakpoints, voltageRef, f)
            
        elif quadrant == "Q2": 
            speedDir    = -1
            torqueDir   = 1
            f           = interp2d(xx, yy*speedDir, torquePeak, kind='linear', copy=True, bounds_error=False, fill_value=None)
            env         = genEnv(torqueDir, torquePeak, speedDir, speedBreakpoints, voltageRef, f)

        elif quadrant == "Q3":
            speedDir    = -1
            torqueDir   = -1
            f           = interp2d(xx, yy*speedDir, torquePeak, kind='linear', copy=True, bounds_error=False, fill_value=None)
            env         = genEnv(torqueDir, torquePeak, speedDir, speedBreakpoints, voltageRef, f)

        elif quadrant == "Q4":
            speedDir    = 1
            torqueDir   = -1
            f           = interp2d(xx, yy*speedDir, torquePeak, kind='linear', copy=True, bounds_error=False, fill_value=None)
            env         = genEnv(torqueDir, torquePeak, speedDir, speedBreakpoints, voltageRef, f)

        if InitCount    == 0:

            env_out     = pd.concat([envInit, env] , ignore_index = True)
            InitCount   = 1

        else:
            env_out     = pd.concat([env_out, env], ignore_index =True)

    return env_out

def genTorqueSpeed(Test_Name,Export_Path,Export_Name,Export_Format,Logging_Path, DCDC_Ixxat_Id, MCU_Ixxat_Id, Dyno_Ip, Dyno_Port, Dyno_Id, DCDC_V_Target, Speed_Demands,Speed_Lim_Fwd, Speed_Lim_Rev,Torque_Demands,Torque_Time):
    Script = []
    DCDC_I_Lim_Pos = 400
    DCDC_I_Lim_Neg = -400

    Script.append("###### Test Setup ######")
    Script.append("# Name: " + str(Test_Name))
    Script.append("# Log Directory: " + str(st.session_state.Logging_Path))
    Script.append("")
    Script.append("###### Inverter ######")
    Script.append("# Project: " + str(st.session_state.Requested_Project))
    Script.append("# Sample Letter: " + str(st.session_state.Inverter_SampleLetter))
    Script.append("# Sample Number: " + str(st.session_state.Inverter_SampleNumber))
    Script.append("# Notes: " + str(st.session_state.Inverter_Note))
    Script.append("")
    Script.append("###### Motor ######")
    Script.append("# Manufacturer: " + str(st.session_state.Motor_Manufacturer))
    Script.append("# Sample Letter: " + str(st.session_state.Motor_SampleLetter))
    Script.append("# Sample Number: " + str(st.session_state.Motor_SampleNumber))
    Script.append("# Notes: " + str(st.session_state.Motor_Note))
    Script.append("")
    Script.append("###### Software ######")
    Script.append("# Commit: " + str(st.session_state.Soft_Commit))
    Script.append("# Ke: " + str(st.session_state.Soft_Ke))
    Script.append("# Offset: " + str(st.session_state.Soft_Offset))
    Script.append("")
    Script.append("###### Dynamometer ######")
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
    Script.append("###### DCDC ######")
    Script.append("# Target DC Link Voltage: " + str(st.session_state.Requested_Voltage))
    Script.append("# DC Link Current Limit Positive: " + str(st.session_state.Requested_I_Lim_Pos))
    Script.append("# DC Link Current Limit Negative: " + str(st.session_state.Requested_I_Lim_Neg))
    Script.append("")
    Script.append("###### Speed ######")
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
    Script.append("###### Time ######")
    Script.append("# Torque Demand time (s): " + str(st.session_state.Requested_Torque_Up_Period))
    Script.append("# Wait Period (s): " + str(st.session_state.Requested_Wait_Period))
    Script.append("")
    Script.append("#****** START OF TEST SCRIPT ******")
    Script.append("")
    Script.append("Speed_Demands = " + str(Speed_Demands))
    Script.append("")
    Script.append("Torque_Demands = " + str(Torque_Demands))
    Script.append("")
    Script.append("Speed_Limits_Forward = " + str(Speed_Lim_Fwd))
    Script.append("")
    Script.append("Speed_Limits_Reverse = " + str(Speed_Lim_Rev))
    Script.append("")
    Script.append("Torque_Demand_Time = " + str(Torque_Time))
    Script.append("")
    Script.append("DCDC_I_Limit_Pos = "+str(DCDC_I_Lim_Pos))
    Script.append("DCDC_I_Limit_Neg = "+str(DCDC_I_Lim_Neg))
    Script.append("")
    Script.append("DCDC_V_Target = " + str(DCDC_V_Target))
    Script.append("")
    Script.append("DCDC.setOutputCurrentLimits(DCDC_I_Lim_Pos,DCDC_I_Lim_Neg)")
    Script.append("DCDC.setOutputEnabled(True)")
    Script.append("DCDC.setOutputVoltage(DCDC_V_Target)")
    Script.append("")
    Script.append("print(str(Wait while DCDC raises to desired level))")
    Script.append("time.sleep(2)")
    Script.append("DCDC.getOutputVoltage()")
    Script.append("")

    Script.append("for i in range(0, len(Speed_Demands)")
    Script.append("\tMCU.setSpeedLimits(min(Speed_Limits_Forward[i],0),max(Speed_Limits_Forward_Reverse[i],0)")
    Script.append("\tDyno_setSpeed(Speed_Demands[i])")
    Script.append("\tMCUsetTorqueDemand(Torque_Demands[i])")
    Script.append("\tMCU.getTorque()")
    Script.append("\ttime.sleep(Torque_Demand_Time[i])")
    Script.append("\ti = i+1")

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
