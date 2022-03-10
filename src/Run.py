from MunchPy import *
import streamlit as st
import time

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

def Intialise_and_Run_Test_Offline(Logging_Path, DCDC_Ixxat_Id, MCU_Ixxat_Id, Dyno_Ip, Dyno_Port, Dyno_Id, DCDC_V_Target, Speed_Demands,Torque_Demands,Requested_Demanded_Period):
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

    Run_Torque_Speed_Offline(DCDC_I_Lim_Pos, DCDC_I_Lim_Neg, DCDC_V_Target,Speed_Demands, Torque_Demands, Requested_Demanded_Period)

    st.success("Check Console; Test Finished")


def Run_Torque_Speed_Offline(DCDC_I_Lim_Pos, DCDC_I_Lim_Neg, DCDC_V_Target, Speed_Demands, Torque_Demands, Requested_Demanded_Period, Speed_Limit_Threshold):
    st.info("Run_Torque_Speed_Offline()")

    DCDC_setOutputCurrentLimits(DCDC_I_Lim_Pos, DCDC_I_Lim_Neg)
    DCDC_setOutputEnabled(True)
    DCDC_setOutputVoltage(DCDC_V_Target)

    print("Wait while DCDC raises to desired level")
    time.sleep(2)
    DCDC_getOutputVoltage()

    for i in range(0, len(Speed_Demands)):
        MCU_setSpeedLimits(min(Speed_Demands[i]*Speed_Limit_Threshold,0),max(Speed_Demands[i]*Speed_Limit_Threshold,0))
        Dyno_setSpeed(Speed_Demands[i])
        MCU_setTorqueDemand(Torque_Demands[i])
        MCU_getTorque()
        time.sleep(Requested_Demanded_Period)
        i = i+1

    MCU_setTorqueDemand(0)

# For Offline
def DCDC_setOutputCurrentLimits(DCDC_I_Lim_Pos, DCDC_I_Lim_Neg):
    return print("DCDC Current Limit, [+]: " + str(DCDC_I_Lim_Pos) + " A, [-]: " + str(DCDC_I_Lim_Neg) + "A")

def DCDC_setOutputVoltage(DCDC_V_Target):
    return print("DCDC Voltage: " + str(DCDC_V_Target) + " V")

def DCDC_getOutputVoltage():
    return print("DCDC Voltage: Get Output Voltages")

def DCDC_getInputVoltage():
    return print("DCDC Voltage: Get Input Voltages")

def DCDC_setOutputEnabled(BOOL):
    return print("DCDC Output Enable: " + str(BOOL))

def MCU_setSpeedLimits(MCU_Rev_Speed_Lim, MCU_Fwd_Speed_Lim):
    return print("Set MCU Speed Limits, Forward: " + str(MCU_Fwd_Speed_Lim) + " rpm, Reverse: " + str(MCU_Rev_Speed_Lim) + " rpm")

def MCU_setBridgeEnabled(BOOL):
    return print("Set MCU Bridge Enabled: " + str(BOOL))

def MCU_setTorqueDemand(Torque_Demanded):
    return print("MCU Torque Demanded: " + str(Torque_Demanded))

def MCU_getTorque():
    return print("MCU Torque Output: X")

def Dyno_setSpeed(Dyno_Speed):
    return print("Dyno Speed: " + str(Dyno_Speed) + " rpm")