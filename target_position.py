from dynamixel_controller import move, cleanup

def main():
    print("Enter yaw (0-4095) and pitch (1024-3072) values. Blank line to quit.")
    try:
        while True:
            line = input("yaw pitch = ").strip()
            if line == "":
                break
            try:
                yaw_str, pitch_str = line.split() 
                yaw = int(yaw_str)
                pitch = int(pitch_str)
                move(yaw, pitch)
            except ValueError:
                print("Invalid input. Please enter two integers separated by a space.")
    finally:
        cleanup()
        print("Motors safely disabled and port closed.")

if __name__ == "__main__":
    main()
