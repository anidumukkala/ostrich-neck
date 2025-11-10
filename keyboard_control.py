from dynamixel_controller import move, cleanup
import keyboard  # pip install keyboard
import time

# CONFIG

HOME_YAW = 2048
HOME_PITCH = 2048
STEP = 50  # change per arrow key press (speed control)
YAW_MIN, YAW_MAX = 0, 4095
PITCH_MIN, PITCH_MAX = 1024, 3072
TIME_SLEEP = 0.01 # update frequency (seconds)


def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))

def main():
    yaw = HOME_YAW
    pitch = HOME_PITCH
    move(yaw, pitch)
    print(f"Moved to home position: yaw={yaw}, pitch={pitch}")
    print("Use arrow keys to control the motors. Press ESC to quit.")

    try:
        while True:
            if keyboard.is_pressed('up'):
                pitch = clamp(pitch + STEP, PITCH_MIN, PITCH_MAX)
                move(yaw, pitch)
                time.sleep(TIME_SLEEP)  # prevent too fast updates
            elif keyboard.is_pressed('down'):
                pitch = clamp(pitch - STEP, PITCH_MIN, PITCH_MAX)
                move(yaw, pitch)
                time.sleep(TIME_SLEEP)
            elif keyboard.is_pressed('right'):
                yaw = clamp(yaw - STEP, YAW_MIN, YAW_MAX)
                move(yaw, pitch)
                time.sleep(TIME_SLEEP)
            elif keyboard.is_pressed('left'):
                yaw = clamp(yaw + STEP, YAW_MIN, YAW_MAX)
                move(yaw, pitch)
                time.sleep(TIME_SLEEP)
            elif keyboard.is_pressed('esc'):
                print("Exiting...")
                break
            time.sleep(0.01)  # small sleep to reduce CPU usage
    finally:
        cleanup()
        print("Motors safely disabled and port closed.")

if __name__ == "__main__":
    main()
