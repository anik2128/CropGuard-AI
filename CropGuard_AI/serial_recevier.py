import serial
import json
import time

PORT = "COM7"  # Replace with your ESP32 COM port
BAUD_RATE = 115200

print("CROPGUARD AI - HARDWARE BRIDGE")
print("Connecting to ESP32...")

try:
    esp32 = serial.Serial(PORT, BAUD_RATE, timeout=2)
    time.sleep(2)

    print("ESP32 CONNECTED!")
    print("Receiving live sensor data...")

    while True:
        line = esp32.readline().decode(
            "utf-8", errors="ignore"
        ).strip()

        if not line.startswith("CG,"):
            continue

        try:
            values = line.split(",")

            data = {
                "air_temperature": float(values[1]),
                "humidity": float(values[2]),
                "soil_temperature": float(values[3]),
                "soil_moisture_raw": int(values[4]),
                "timestamp": time.time()
            }

            with open("sensor_data.json", "w") as file:
                json.dump(data, file, indent=4)

            print("LIVE:", data)

        except (ValueError, IndexError):
            print("Invalid sensor packet:", line)

except serial.SerialException as error:
    print("SERIAL ERROR:", error)

except KeyboardInterrupt:
    print("\nCROPGUARD STOPPED")

finally:
    if "esp32" in locals() and esp32.is_open:
        esp32.close()