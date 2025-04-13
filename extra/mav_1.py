from pymavlink import mavutil
from time import sleep  # Import the sleep function

# Connect to Pixhawk via USB on Windows
master = mavutil.mavlink_connection('com12', baud=57600)

try:
    # Arm the vehicle
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,  # Confirmation
        1,  # Arm (1) or Disarm (0)
        0, 0, 0, 0, 0, 0
    )

    # Wait for a moment
    print("Waiting for 5 seconds...")
    master.wait_heartbeat()
    sleep(5)  # Use the sleep function from the time module

    # Disarm the vehicle
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,  # Confirmation
        0,  # Arm (1) or Disarm (0)
        0, 0, 0, 0, 0, 0
    )

    print("Vehicle disarmed.")

except KeyboardInterrupt:
    print("Script terminated by user.")
finally:
    master.close()
