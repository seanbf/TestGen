from MunchPy import *
import streamlit as st
import time
import os

def Run_Torque_Speed(dcdc, mcu, dyno, DCDC_I_Lim_Pos, DCDC_I_Lim_Neg, DCDC_V_Target):
        

        dcdc.setOutputCurrentLimits(DCDC_I_Lim_Pos,DCDC_I_Lim_Neg)
        dcdc.setOutputEnabled(True)
        dcdc.setOutputVoltage(DCDC_V_Target)

        time.sleep(1)
        
        mcu.setSpeedLimits(1000, 1000)

        if mcu.setBridgeEnabled(True):
            mcu.setTorqueDemand(5)

        st.write(mcu.getTorque())

        time.sleep(1)

        mcu.setTorqueDemand(0)

        if mcu.setBridgeEnabled(False):
            st.write("MCU Disabled")
        else:
            st.write("MCU Issue")

def Intialise_and_Run_Test(Intialise_Test_Offline, Logging_Path, DCDC_Ixxat_Id, MCU_Ixxat_Id, Dyno_Ip, Dyno_Port, Dyno_Id, DCDC_I_Lim_Pos, DCDC_I_Lim_Neg, DCDC_V_Target):
    st.info("Intialise Munch Placeholder")
    # Create instance - Always Needed
    munchInterop = MunchInterop.getInstance()
    if munchInterop is not None:
        munchInterop.initialise(Logging_Path, True)
        
        try:
            dcdc_Can_Device = CANDevice.getSpecific(munchInterop, DCDC_Ixxat_Id )
            mcu_Can_Device = CANDevice.getSpecific(munchInterop, MCU_Ixxat_Id )        
            dyno = NidecDyno(munchInterop, Dyno_Ip, Dyno_Port, Dyno_Id)
            dcdc = ParallelDCDC(munchInterop, dcdc_Can_Device)
            mcu = Derwent(munchInterop, mcu_Can_Device)
            
            if st.button("KL30 Enabled, Run Test"):
                Intialise_Test_Offline(dcdc, mcu, dyno,DCDC_I_Lim_Pos, DCDC_I_Lim_Neg, DCDC_V_Target)
            
        finally:    
            munchInterop.terminate()

def Intialise_and_Run_Test_Offline(Export_Name,Export_Format,Logging_Path, DCDC_Ixxat_Id, MCU_Ixxat_Id, Dyno_Ip, Dyno_Port, Dyno_Id, DCDC_V_Target, Speed_Demands,Speed_Lim_Fwd, Speed_Lim_Rev,Torque_Demands,Requested_Demanded_Period):
    st.info("Intialise_and_Run_Test_Offline()")
    st.write(Logging_Path)

    DCDCCan = "Get Device @ DCDC Ixxat ID: " + str(DCDC_Ixxat_Id)
    MCUCan  = "Get Device @ MCU Ixxat ID: " + str(MCU_Ixxat_Id)        
    Dyno    = "Dyno Ip: " + str(Dyno_Ip) + " Dyno Port: " + str(Dyno_Port) + " Dyno Id: " + str(Dyno_Id)
    DCDC    = "DCDC "
    MCU     = "MCU "

    DCDC_I_Lim_Pos = 400
    DCDC_I_Lim_Neg = -400

    # temp
    Generate_Torque_Speed_Script(Export_Name,Export_Format,DCDC_I_Lim_Pos, DCDC_I_Lim_Neg, DCDC_V_Target,Speed_Demands,Speed_Lim_Fwd, Speed_Lim_Rev, Torque_Demands, Requested_Demanded_Period)
    st.success("Check Console; Test Finished")