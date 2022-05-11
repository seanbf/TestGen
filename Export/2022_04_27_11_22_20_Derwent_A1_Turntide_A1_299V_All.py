###### Test Setup ######
# Name: 2022_04_27_11_22_20_Derwent_A1_Turntide_A1_299V_All
# Log Directory: C:\Users\sean.freedman\Desktop\TestGen\Log

###### Inverter ######
# Project: Derwent
# Sample Letter: A
# Sample Number: 1
# Notes: 

###### Motor ######
# Manufacturer: Turntide
# Sample Letter: A
# Sample Number: 1
# Notes: 

###### Software ######
# Commit: 
# Ke: 
# Offset: 

###### Dynamometer ######
# Location: DX: 340kW
# IP Address: 192.168.1.2
# Port: 502
# ID: 0

##### CAN Hardware ######
# DCDC Ixxat ID: HW507598
# MCU Ixxat ID: HW484965

##### Test ######
# Test Type: Torque Speed Sweep
# Test Profile: All

###### DCDC ######
# Target DC Link Voltage: 299.5
# DC Link Current Limit Positive: 400.0
# DC Link Current Limit Negative: -400.0

###### Speed ######
# Minimum Speed abs(rpm): 500.0
# Speed Step Size abs(rpm): 500.0
# Maximum speed abs(rpm): 500.0
# Speed Limit Type: Percentage
# Value of Speed Limit: 120

##### Torque ######
# Minimum Torque abs(Nm): 0.0
# Torque Step Size (Nm): 50.0
# Maximum Torque (% of peak): 100
# Skip Last Torque Demand per speed point?: True

###### Time ######
# Torque Demand time (s): 1.0
# Wait Period (s): 1.0

#****** START OF TEST SCRIPT ******

Speed_Demands = [500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, -500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0]

Torque_Demands = [0.0, 50.0, 100.0, 150.0, 200.0, 250.0, 200.0, 150.0, 100.0, 50.0, 0.0, 0.0, 0.0, 0.0, 50.0, 100.0, 150.0, 200.0, 250.0, 200.0, 150.0, 100.0, 50.0, 0.0, 0.0, 0.0, -0.0, -50.0, -100.0, -150.0, -200.0, -250.0, -200.0, -150.0, -100.0, -50.0, 0.0, 0.0, -0.0, -50.0, -100.0, -150.0, -200.0, -250.0, -200.0, -150.0, -100.0, -50.0, 0.0, 0.0]

Speed_Limits_Forward = [600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0]

Speed_Limits_Reverse = [600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0, 600.0]

Torque_Demand_Time = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

DCDC_I_Limit_Pos = 400
DCDC_I_Limit_Neg = -400

DCDC_V_Target = 299.5

DCDC.setOutputCurrentLimits(DCDC_I_Lim_Pos,DCDC_I_Lim_Neg)
DCDC.setOutputEnabled(True)
timeout = time.time() + 10
while(DCDC.getOutputVoltage() < 299.5and (time.time() < timeout):
	time.sleep(0.1)

munchLoggingPath = .
munchInterop = MunchInterop.getInstance()
if munchInterop is not None:
	munchInterop.initialise(munchLoggingPath, True)
	time.sleep(0.5)
	try:
		dcdcCanDevice = CANDevice.getSpecific(munchInterop, HW507598
		mcuCanDevice = CANDevice.getSpecific(munchInterop, HW484965
		for i in range(0, len(Speed_Demands)
			MCU.setSpeedLimits(min(Speed_Limits_Forward[i],0),max(Speed_Limits_Forward_Reverse[i],0)
			Dyno_setSpeed(Speed_Demands[i])
			MCUsetTorqueDemand(Torque_Demands[i])
			MCU.getTorque()
			time.sleep(Torque_Demand_Time[i])
			i = i+1
			MCU.setTorqueDemand(0)
