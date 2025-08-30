import sys
from dynamixel_sdk import *  # Uses Dynamixel SDK library

# Control table addresses (XM430-W350 or similar, adjust if needed)
ADDR_TORQUE_ENABLE      = 64
ADDR_GOAL_POSITION      = 116
ADDR_PRESENT_POSITION   = 132
LEN_GOAL_POSITION       = 4
LEN_PRESENT_POSITION    = 4

# Protocol version (2.0 for most new Dynamixels)
PROTOCOL_VERSION        = 2.0

# Port and baudrate (Generally COM for Windows, ttyUSB for Linux)
DEVICENAME              = 'COM5'
BAUDRATE                = 4000000

# Motor IDs (change IDs if needed)
DXL_ID_YAW              = 12
DXL_ID_PITCH            = 13

# Initialize PortHandler & PacketHandler
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# GroupSyncWriter for sending goal positions
groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)

# Intialization
if not portHandler.openPort():
    print("Failed to open port")
    sys.exit(1)

if not portHandler.setBaudRate(BAUDRATE):
    print("Failed to set baudrate")
    sys.exit(1)

# Enable Torque
for motor_id in [DXL_ID_YAW, DXL_ID_PITCH]:
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, motor_id, ADDR_TORQUE_ENABLE, 1)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Error enabling torque for ID {motor_id}: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"Error enabling torque for ID {motor_id}: {packetHandler.getRxPacketError(dxl_error)}")

# Movement function
def move(yaw, pitch):
    """Move motors to given yaw and pitch positions (0-4095)."""
    params_yaw = [DXL_LOBYTE(DXL_LOWORD(yaw)),
                  DXL_HIBYTE(DXL_LOWORD(yaw)),
                  DXL_LOBYTE(DXL_HIWORD(yaw)),
                  DXL_HIBYTE(DXL_HIWORD(yaw))]

    params_pitch = [DXL_LOBYTE(DXL_LOWORD(pitch)),
                    DXL_HIBYTE(DXL_LOWORD(pitch)),
                    DXL_LOBYTE(DXL_HIWORD(pitch)),
                    DXL_HIBYTE(DXL_HIWORD(pitch))]

    groupSyncWrite.addParam(DXL_ID_YAW, params_yaw)
    groupSyncWrite.addParam(DXL_ID_PITCH, params_pitch)

    dxl_comm_result = groupSyncWrite.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("Error sending sync write:", packetHandler.getTxRxResult(dxl_comm_result))

    groupSyncWrite.clearParam()

# Safely depower motors after termination
def cleanup():
    """Disable torque and close port safely."""
    for motor_id in [DXL_ID_YAW, DXL_ID_PITCH]:
        packetHandler.write1ByteTxRx(portHandler, motor_id, ADDR_TORQUE_ENABLE, 0)
    portHandler.closePort()
