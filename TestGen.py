import os
import numpy as np
import streamlit as st
from src.Profiles import Derwent_Profile, Bowfell_Profile, Oxford_Profile
from src.Generator import Profile_Generator, Reference_Generation, Generate_Torque_Speed
from src.Run import Intialise_and_Run_Test, Intialise_and_Run_Test_Offline, Run_Torque_Speed
from src.Plot import Plot_Profile
from datetime import datetime

# OPEN CMD: streamlit run <filename>.py

page_config = st.set_page_config(
                                page_title              ="Test Generator", 
                                page_icon               ="📈", 
                                #layout                  ='wide', 
                                initial_sidebar_state   ='auto'
                                )
 
# Begin
st.title("📈 Test Generator")

datetime_format = ""
Available_Projects = ["Derwent","Bowfell","Oxford","Other"]
Field_InverterName = Available_Projects[1]
Availble_SampleLetters = ["A","B","C","D","Other"]
Field_InverterSampleLetter = Availble_SampleLetters[1]
Availble_SampleNumber = ["1","2","3","4"]
Field_InverterSampleNumber = Availble_SampleNumber[1]
Test_Name = Field_InverterName

st.write("The tool is used to generate and perform various tests such as; torque steps at various speeds, injecting currents to a eMotor etc.")
if st.checkbox("Use Custom Test Profile", value = False):
    st.file_uploader("Custom Test Profile Upload",type='.py', accept_multiple_files=False)
else:
    with st.expander("Test Setup", expanded=True):
        # Project
        st.text_input("Test Name", value = "", placeholder="AUTO: <DATETIME>_<PROJECT>_<INVERTER>_<MOTOR>_<VOLTAGE>_<PROFILE>",key = "Test_Name")
        st.text_input("Log Directory", value = os.getcwd()+"\Log", placeholder=os.getcwd(), key = "Logging_Path")
        if st.session_state.Logging_Path =="":
            Logging_Path = os.getcwd()
        else:
            Logging_Path = st.session_state.Logging_Path

        # Inverter
        st.subheader("Inverter")
        TestCol_Inverter,TestCol_InverterSampleLetter,TestCol_InverterSampleNumber = st.columns(3)

        TestCol_Inverter.selectbox("Project",Available_Projects, key = "Requested_Project")

        if st.session_state.Requested_Project == "Other":
            TestCol_Inverter.text_input("", value = "", key = "Requested_Project_Other")
            Field_InverterName = st.session_state.Requested_Project_Other
        else:
            Field_InverterName =  st.session_state.Requested_Project

        if st.session_state.Requested_Project == "Bowfell":
            Voltage_BreakPoints, Speed_BreakPoints, Peak_Torque, Max_Voltage, Max_Speed,Max_Torque = Bowfell_Profile()

        if st.session_state.Requested_Project == "Oxford":
            Voltage_BreakPoints, Speed_BreakPoints, Peak_Torque, Max_Voltage, Max_Speed,Max_Torque = Oxford_Profile()

        if st.session_state.Requested_Project == "Derwent":
            Voltage_BreakPoints, Speed_BreakPoints, Peak_Torque, Max_Voltage, Max_Speed,Max_Torque = Derwent_Profile()

        TestCol_InverterSampleLetter.selectbox("Sample Letter",Availble_SampleLetters, key = "Inverter_SampleLetter")

        if st.session_state.Inverter_SampleLetter == "Other":
            TestCol_InverterSampleLetter.text_input("", value = "", key = "Inverter_SampleLetter_Other")
            Field_InverterSampleLetter = st.session_state.Inverter_SampleLetter_Other
            Inverter_SampleNumber = "_"
        else:
            Field_InverterSampleLetter = st.session_state.Inverter_SampleLetter
            Inverter_SampleNumber = Availble_SampleNumber

        TestCol_InverterSampleNumber.selectbox("Sample Number",Inverter_SampleNumber, key = "Inverter_SampleNumber")
        if st.session_state.Inverter_SampleNumber != "_":
            Field_InverterSampleNumber = st.session_state.Inverter_SampleNumber
        else:
            Field_InverterSampleNumber = "_"
        st.text_area("Inverter Notes", placeholder = "Hardware modifications, Prototype, Customer return etc.", key = "Inverter_Note")

        # Motor
        st.subheader("Motor")
        # IDEA May add serial number ID, attach offset and ke.
        TestCol_Motor, TestCol_MotorSampleLetter, TestCol_MotorSampleNumber = st.columns(3)

        TestCol_Motor.selectbox("Project",["Turntide","Remy","Yasa","Integral Powertrain","Emrax","Other"], key = "Motor_Manufacturer")

        if st.session_state.Motor_Manufacturer == "Other":
            TestCol_Motor.text_input("", value = "", key = "Motor_Manufacturer_Other")

        TestCol_MotorSampleLetter.selectbox("Sample Letter",["A","B","C","D","Other"], key = "Motor_SampleLetter")
        if st.session_state.Motor_Manufacturer == "Other":
            TestCol_MotorSampleLetter.text_input("", value = "", key = "Motor_Sample_Other")

        TestCol_MotorSampleNumber.selectbox("Sample Number",["1","2","3","4","N/A"], key = "Motor_SampleNumber")
        st.text_area("Motor Notes", placeholder = "Hardware modifications, Prototype, Customer return etc.", key = "Motor_Note")

        # Software
        st.subheader("Software")
        SoftCol_Commit, SoftCol_Ke, SoftCol_Offset,  = st.columns(3)
        SoftCol_Commit.text_input("Commit", value = "", key = "Soft_Commit")
        SoftCol_Ke.text_input("Ke", value = "", key = "Soft_Ke")
        SoftCol_Offset.text_input("Offset", value = "", key = "Soft_Offset")

        # Dyno
        st.subheader("Dynamometer")
        Dyno_Location, DynoCol_Ip, DynoCol_Port, DynoCol_Id = st.columns(4)

        Dyno_Location.selectbox("Location",["DX: 340kW","DX: 160kW","DX: 100kW"], key = "Dyno_Location")

        if st.session_state.Dyno_Location == "DX: 340kW":
            Default_Ip =  "192.168.1.2"
            Default_Port = int(502)
            Default_Id = int(0)
            Default_Ixxat_MCU = "HW507598"
            Default_Ixxat_DCDC = "HW484965"
        if st.session_state.Dyno_Location == "DX: 160kW":
            Default_Ip =  "192.168.1.1"
            Default_Port = int(502)
            Default_Id = int(0)
            Default_Ixxat_MCU = "HW123456"
            Default_Ixxat_DCDC = "HW79010"
        if st.session_state.Dyno_Location == "DX: 100kW":
            Default_Ip =  "192.168.1.1"
            Default_Port = int(502)
            Default_Id = int(0)
            Default_Ixxat_MCU = "HW100"
            Default_Ixxat_DCDC = "HW200"

        DynoCol_Ip.text_input("IP Address",value = Default_Ip, key = "Dyno_Ip")
        DynoCol_Port.number_input("Port", min_value = 0, max_value = 5000, value = Default_Port, step = 1, key = "Dyno_Port")
        DynoCol_Id.number_input("ID", min_value = 0, max_value = 64, value = Default_Id, step = 1, key = "Dyno_Id")

        # CAN
        st.subheader("CAN Hardware")
        IxxatCol_DCDC, IxxatCol_MCU = st.columns(2)
        IxxatCol_DCDC.text_input("DCDC Ixxat HWID", value = Default_Ixxat_MCU, key = "CAN_ID_DCDC")
        IxxatCol_MCU.text_input("MCU Ixxat HWID", value = Default_Ixxat_DCDC, key = "CAN_ID_MCU")

    with st.expander("Test Generator", expanded=False):
        st.subheader("Test Type")
        TestCol_1, TestCol_2 = st.columns(2)
        TestCol_1.selectbox("Test Type", ["Torque Speed Sweep","Idq Injection"], key="Requested_Type")

        if st.session_state.Requested_Type == "Torque Speed Sweep":
            Profile_Help = "Q1 Forward Motoring, Q2 Reverse Generating, Q3 Reverse Motoring, Q4 Forward Generating, Forward: [Q1,Q4], Reverse: [Q2,Q3], All: [Q1,Q2,Q3,Q4]"
            TestCol_2.selectbox("Profile",["Forward Motoring","Reverse Generating","Reverse Motoring","Forward Generating","Motoring","Generating","Forward","Reverse","All"], help=Profile_Help,key = "Requested_Profile")

            # DC Link
            st.subheader("DC Link")
            DCDCCol_1,DCDCCol_2,DCDCCol_3 = st.columns(3)
            DCDCCol_1.number_input("DC Link Voltage",  min_value = 0.0, max_value = 500.0, value = 0.0, step = 0.5, help="Project Breakpoints = " + str(Voltage_BreakPoints),key = "Requested_Voltage")
            DCDCCol_2.number_input("DC Link Current (+)",  min_value = 0.0, max_value = 500.0, value = 400.0, step = 0.5 ,key = "Requested_I_Lim_Pos")
            DCDCCol_3.number_input("DC Link Current (-)",  min_value = -500.0, max_value = 0.0, value = -400.0, step = 0.5 ,key = "Requested_I_Lim_Neg")

            # Speed
            st.write("Speed")
            SpeedCol_1,SpeedCol_2,SpeedCol_3 = st.columns(3)
            SpeedCol_1.number_input("Minimum Speed (abs(rpm))", min_value = 0.0, max_value = float(Max_Speed), value = 500.0, step = 0.5, key = "Requested_Min_Speed")
            SpeedCol_2.number_input("Speed Step Size (abs(rpm))", min_value = 0.5, max_value = float(Max_Speed), value = 500.0, step = 0.5, key = "Requested_Speed_Step")
            SpeedCol_3.number_input("Maximum Speed (abs(rpm))", min_value = 0.5, max_value = float(Max_Speed), value = float(Max_Speed), step = 0.5, key = "Requested_Max_Speed")
            SpeedCol_1.selectbox("Speed Limit Threshold",['Percentage','Offset','Value'], disabled = True, key="Requested_Speed_Limit_Type")

            if st.session_state.Requested_Speed_Limit_Type == "Percentage":
                SpeedCol_2.number_input("Percentage of Speed Target ", min_value = 0, max_value = 1000, value = 120, step = 1, key = "Requested_Speed_Limit")
            elif st.session_state.Requested_Speed_Limit_Type == "Offset":
                SpeedCol_2.number_input("Offset", min_value = 0.0, max_value = float(Max_Speed), value = 500.0, step = 0.01, key = "Requested_Speed_Limit")
            elif st.session_state.Requested_Speed_Limit_Type == "Value":
                SpeedCol_2.number_input("Offset", min_value = 0.0, max_value = float(Max_Speed), value = float(Max_Speed), step = 0.01, key = "Requested_Speed_Limit")
            
            # Torque
            st.subheader("Torque")
            TorqueCol_1a,TorqueCol_2a = st.columns(2)
            TorqueCol_1a.number_input("Minimum Torque (abs(Nm))", min_value = 0.0, max_value = float(Max_Torque), value = 0.0, step = 0.5, key = "Requested_Min_Torque")
            TorqueCol_2a.number_input("Maximum Torque (% of Peak)", min_value = 0, max_value = 100, value = 100, step = 1, key = "Requested_Max_Torque")
            
            TorqueCol_1,TorqueCol_2, TorqueCol_3, TorqueCol_4 = st.columns(4)

            TorqueCol_1.selectbox("Step Up Method: ",['Ramp Up','Zero Torque'], key="Requested_Torque_Up_Method", disabled = True)
            if st.session_state.Requested_Torque_Up_Method == "Ramp Up":
                TorqueCol_2.number_input("Step Up Size", min_value = 0.5, max_value = float(Max_Torque), value = 20.0, step = 0.5, key = "Requested_Torque_Up_Step")
                TorqueCol_3.number_input("Step Period (s)", min_value = 0.01, max_value = 5000.0, value = 1.0, step = 0.01, key = "Requested_Torque_Up_Period")
                TorqueCol_4.selectbox("Log", ["Enabled","Disabled"],key = "Log_Up", disabled= True)

            TorqueCol_1.selectbox("Step Down Method: ",['Ramp Down','Zero Torque'], key="Requested_Torque_Down_Method")
            if st.session_state.Requested_Torque_Down_Method == "Ramp Down":
                TorqueCol_2.number_input("Step Down Size", min_value = 0.01, max_value = float(Max_Torque), value = 20.0, step = 0.5, key = "Requested_Torque_Down_Step")
                TorqueCol_3.number_input("Step Period (s)", min_value = 0.01, max_value = 5000.0, value = 1.0, step = 0.01, key = "Requested_Torque_Down_Period")
                TorqueCol_4.selectbox("Log", ["Disabled","Enabled"],key = "Log_Down", disabled= True)
            
            st.checkbox("Skip last Torque demand per speed step", value=False,key = "Skip_Max_Torque")

            # Time
            st.subheader("Time")
            st.number_input("Wait Period (s)", min_value = 0.0, max_value = 5000.0, value = 1.0, step = 0.01, key = "Requested_Wait_Period", disabled = True)

            # Export
            Profile_Speeds, Profile_Torques, Speed_Lim_Fwd, Speed_Lim_Rev, Project_Speeds, Project_Torques, Torque_Time, Profile_Voltage  = Profile_Generator(st.session_state.Requested_Profile, Max_Voltage, st.session_state.Requested_Voltage, st.session_state.Requested_Torque_Up_Step, Max_Speed, st.session_state.Requested_Speed_Step, st.session_state.Requested_Min_Speed, st.session_state.Requested_Max_Speed, st.session_state.Requested_Min_Torque, st.session_state.Requested_Max_Torque, st.session_state.Requested_Torque_Up_Period, st.session_state.Requested_Torque_Down_Period, st.session_state.Requested_Wait_Period, Voltage_BreakPoints, Speed_BreakPoints, Peak_Torque, st.session_state.Requested_Speed_Limit_Type, st.session_state.Requested_Speed_Limit, st.session_state.Skip_Max_Torque)

        elif st.session_state.Requested_Type == "Idq Injection":
            st.info("Under Devleopement")
            st.stop()

        datetime_now = datetime.now()
        format = "%Y_%m_%d_%H_%M_%S_"
        datetime_format = datetime_now.strftime(format)

        if st.session_state.Test_Name == "":
            Test_Name = datetime_format + st.session_state.Requested_Project + "_" + st.session_state.Inverter_SampleLetter + st.session_state.Inverter_SampleNumber +"_" +st.session_state.Motor_Manufacturer + "_" + st.session_state.Motor_SampleLetter + st.session_state.Motor_SampleNumber + "_" + str(int(st.session_state.Requested_Voltage))  +"V_" + st.session_state.Requested_Profile
        else:
            Test_Name = datetime_format + st.session_state.Test_Name

        Internal_Name = "TestScript"
        Internal_Format = ".py"

        Generate_Torque_Speed(Test_Name,os.getcwd() + "\\",Internal_Name,Internal_Format,st.session_state.Logging_Path, st.session_state.CAN_ID_DCDC, st.session_state.CAN_ID_MCU, st.session_state.Dyno_Ip, st.session_state.Dyno_Port, st.session_state.Dyno_Id, Profile_Voltage, Profile_Speeds,Speed_Lim_Fwd, Speed_Lim_Rev, Profile_Torques, Torque_Time)
        
        #Plot
        with st.spinner("Gererating Profile & Plots"):
            Plot_Points, Plot_Timeline  = Plot_Profile(st.session_state.Requested_Project, Profile_Torques, Profile_Speeds, Profile_Voltage, Project_Speeds, Project_Torques, Speed_Lim_Fwd, Speed_Lim_Rev)
            st.subheader("Profile Test Points")
            st.plotly_chart(Plot_Points)
            st.subheader("Profile Timeline")
            st.plotly_chart(Plot_Timeline)  
        
        st.subheader("Export Test")
        st.write("Export test to a file to be shared or stored.")

        Export_Col1, Export_Col2 = st.columns(2)
        Export_Col1.text_input("Export Directory", value = os.getcwd() + "\\Export\\" , placeholder= os.getcwd() + "\\Export\\",key = "Export_Path")
        Export_Col2.selectbox("File Format",[".py",".txt",".csv"], key = "Export_Format")
        st.warning("Under developement: (.csv)")
        if st.button("Export"):
            Generate_Torque_Speed(Test_Name,st.session_state.Export_Path,Test_Name,st.session_state.Export_Format,st.session_state.Logging_Path, st.session_state.CAN_ID_DCDC, st.session_state.CAN_ID_MCU, st.session_state.Dyno_Ip, st.session_state.Dyno_Port, st.session_state.Dyno_Id, Profile_Voltage, Profile_Speeds,Speed_Lim_Fwd, Speed_Lim_Rev, Profile_Torques, Torque_Time)


with st.expander("Symbols", expanded = False):
    st.error("Logging via CANDI not yet available.")
    st.selectbox("Symbol Set", ["Default", "Placeholder"], key = "Symbol_Set")
    s1, s2 = st.columns(2)
    
    if st.session_state.Symbol_Set == "Default":
        if st.session_state.Requested_Type == "Torque Speed Sweep":
            if st.session_state.Requested_Project == "Derwent":
                VDC = "VDC PlaceHolder"
                IDC = "IDC PlaceHolder"
                Id = "Id PlaceHolder"
                Iq = "Iq PlaceHolder"
                Ud = "Ud PlaceHolder"
                Uq = "Uq PlaceHolder"
                ModIndex =  "ModIndex PlaceHolder"
                TorqueReference = "TorqueReference PlaceHolder"
                TorqueTarget = "TorqueTarget PlaceHolder"
                TorqueEstimated = "TorqueEstimated PlaceHolder"
                TransducerTorque = "TransducerTorque PlaceHolder"
                EncoderSpeed = "EncoderSpeed PlaceHolder"
                TransducerSpeed = "TransducerSpeed PlaceHolder"
                InverterHsTemp =  "InverterHsTemp PlaceHolder"
                InverterIGBTTemp = "InverterIGBTTemp PlaceHolder"
                StatorTemp = "StatorTemp PlaceHolder"  

            elif st.session_state.Requested_Project == "Bowfell":
                VDC = "VDC PlaceHolder"
                IDC = "IDC PlaceHolder"
                Id = "Id PlaceHolder"
                Iq = "Iq PlaceHolder"
                Ud = "Ud PlaceHolder"
                Uq = "Uq PlaceHolder"
                ModIndex =  "ModIndex PlaceHolder"
                TorqueReference = "TorqueReference PlaceHolder"
                TorqueTarget = "TorqueTarget PlaceHolder"
                TorqueEstimated = "TorqueEstimated PlaceHolder"
                TransducerTorque = "TransducerTorque PlaceHolder"
                EncoderSpeed = "EncoderSpeed PlaceHolder"
                TransducerSpeed = "TransducerSpeed PlaceHolder"
                InverterHsTemp =  "InverterHsTemp PlaceHolder"
                InverterIGBTTemp = "InverterIGBTTemp PlaceHolder"
                StatorTemp = "StatorTemp PlaceHolder"  

            elif st.session_state.Requested_Project == "Oxford":
                VDC = "VDC PlaceHolder"
                IDC = "IDC PlaceHolder"
                Id = "Id PlaceHolder"
                Iq = "Iq PlaceHolder"
                Ud = "Ud PlaceHolder"
                Uq = "Uq PlaceHolder"
                ModIndex =  "ModIndex PlaceHolder"
                TorqueReference = "TorqueReference PlaceHolder"
                TorqueTarget = "TorqueTarget PlaceHolder"
                TorqueEstimated = "TorqueEstimated PlaceHolder"
                TransducerTorque = "TransducerTorque PlaceHolder"
                EncoderSpeed = "EncoderSpeed PlaceHolder"
                TransducerSpeed = "TransducerSpeed PlaceHolder"
                InverterHsTemp =  "InverterHsTemp PlaceHolder"
                InverterIGBTTemp = "InverterIGBTTemp PlaceHolder"
                StatorTemp = "StatorTemp PlaceHolder"  

        st.markdown("---")

        st.selectbox("DC Link Voltage: ", [VDC],  key="")
        st.selectbox("DC Link Current: ", [IDC],  key="")
        st.selectbox("Id: ", [Id],  key="")
        st.selectbox("Iq: ", [Iq],  key="")
        st.selectbox("Ud: ", [Ud],  key="")
        st.selectbox("Uq: ", [Uq],  key="")
        st.selectbox("Modulation Index: ", [ModIndex],  key="")
        st.selectbox("Torque Reference: ", [TorqueReference],  key="")
        st.selectbox("Torque Target: ", [TorqueTarget],  key="")
        st.selectbox("Torque Estimated: ", [TorqueEstimated],  key="")
        st.selectbox("Torque Measured: ", [TransducerTorque],  key="")
        st.selectbox("Speed Encoder: ", [EncoderSpeed],  key="")
        st.selectbox("Speed Measured: ", [TransducerSpeed],  key="")
        st.selectbox("Inverter Heatsink Temperature: ", [InverterHsTemp],  key="")
        st.selectbox("Inverter Switch Temperature: ", [InverterIGBTTemp],  key="")
        st.selectbox("Motor Stator Temperature: ", [StatorTemp],  key="")

C1, C2, C3 = st.columns(3)

C2.radio("Execute On Target or Local",('Target', 'Local'), key = "Target_Local")
if st.session_state.Target_Local == "Target":
    C2.checkbox("Run Post Script?", value = False, help="Torque Accuracy for Sweep mode, Idq for Idq Injection", disabled = True)

if C2.button("Confirm and Start Tests"):
    st.success("Test Setup and Configuration Confirmed, Proceeding with test")

    st.success("--- Start of Test ---")
    st.write("Filename and/or Directory Name Saved to : " + Test_Name)

    if st.session_state.Target_Local == "Local":
        Intialise_and_Run_Test_Offline(st.session_state.Logging_Path, st.session_state.CAN_ID_DCDC, st.session_state.CAN_ID_MCU, st.session_state.Dyno_Ip, st.session_state.Dyno_Port, st.session_state.Dyno_Id, Profile_Voltage, Profile_Speeds,Speed_Lim_Fwd, Speed_Lim_Rev, Profile_Torques, st.session_state.Requested_Torque_Up_Period)
    else:
        Intialise_and_Run_Test()
    
    
else:
    st.stop()

# IDEA - console/termianl output via text are