# Team Airwise

This is the repository the AIRWISE device, which is an entry to the PA PI Raspberry Pi competition.
Team AIRWISE consists of two pupils at Tynecastle High School, Akshith Bhimanere and Dylan Hill.

## The Airwise device
The AIRWISE device's to meticulously measure the air quality of a room/indoor area, and to correct humidity levels. This is achieved by using a Kitronik Air quality control hat, and reading the air quality values through it. This is an open-source project encouraging others to further build on this project, see the code behind it, and build an AIRWISE themselves   
![AIRWISE Device Image](https://github.com/Team-AIRWISE/AIRWISE/blob/main/images/AIRWISE_logo.jpg)  
# Instructions to Build the AIRWISE device

## Parts List:

- Raspberry Pi
- Kitronik Air Quality Control Hat for Pi
- LED indicator (optional)
- Peltier module (9V)*
- Heat-sink x2*
- Box fan (9V)*
- Micro limit switch
- Jumper wires
- Ultrasonic water atomiser/vaporiser
- Double Relay module
- Parts for case made according to 3D model provided (Recommended to 3D print with PLA filament)

\*Could be scrapped from a mini dehumidifier

## Software Required:

- Pi Imager
- MobaXterm

## Step 1: Preparing the Main Modules

1. **Assembling the Dehumidifier Unit:**
   - Apply thermal paste to one side of the Peltier module and attach the heat-sink, repeat for the other side.
   - Mount the 9V fan to one heat-sink, ensuring proper orientation and airflow direction.

   *Alternative:* Utilize the internals of a mini dehumidifier.

2. **Attaching the Pi to the Air Quality Control Hat:**
   - Attach the ribbon cable to the Pi and fold it at a 45-degree angle.
   - Connect the Hat to the ribbon cable.
   - Solder header pins onto the hat for water level functionality.
   - Insert a TF card flashed with Raspberry Pi OS (not Lite) pre-configured for WiFi and SSH.

## Preparing and Assembling the Humidifier Unit:

- Solder wires to the buttons of the ultrasonic atomiser control board.

## Building the Body/Structure:

- Utilize provided 3D models for fabrication.
- Print/fabricate parts and assemble them together.
- Slide in the mid plate for mounting electronics.

## Mounting and Connecting Electronics:

- Mount the switch into the structure.
- Use M2.5 nuts and bolts to secure the relay and Raspberry Pi on the midplate.
- Connect wiring according to the pictures

## Software:

1. Connect via SSH.
2. Plug in your Pi and wait for boot-up.
3. Open MobaXterm on your computer.
4. Double-click session, click SSH, specify username as 'pi', and enter AIRWISE.local as Remote Host.
5. Start session and turn on serial.

Your AIRWISE device should now be finished in terms of hardware and ready for software configuration.

![AIRWISE Device Image](https://github.com/Team-AIRWISE/AIRWISE/blob/main/images/ribbon.jpg)

---

*Dylan, please insert the picture here or else I will dognap 🟦*