import random
import time
from datetime import datetime

# Room Temperature Monitor
# Note: Readings are simulated, not measured by a sensor.

temperature = 25.0

print("=" * 40)
print("     ROOM TEMPERATURE MONITOR")
print("=" * 40)
print("Mode: Simulation")
print("Update interval: 2 seconds")
print("Press Ctrl+C to stop monitoring.")
print("=" * 40)

try:
    while True:
        # Simulate a small change in temperature
        temperature += random.uniform(-0.4, 0.4)

        # Keep the temperature within our simulation limits
        temperature = max(15.0, min(temperature, 40.0))

        # Get the current time
        current_time = datetime.now().strftime("%H:%M:%S")

        # Classify the temperature
        if temperature < 20:
            status = "Cool"
        elif temperature <= 28:
            status = "Comfortable"
        else:
            status = "Hot"

        # Display the reading
        print(
            f"[{current_time}] "
            f"Temperature: {temperature:.1f} C | "
            f"Status: {status}"
        )

        # Wait two seconds before the next reading
        time.sleep(2)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")
    print("Thank you for using the monitor!")
