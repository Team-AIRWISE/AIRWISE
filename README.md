# Team Airwise

This is the repository the AIRWISE device, which is an entry to the PA PI Raspberry Pi competition.
Team AIRWISE consists of two pupils at Tynecastle High School, Akshith Bhimanere and Dylan Hill.

## The Airwise device
The AIRWISE device's to meticulously measure the air quality of a room/indoor area, and to correct humidity levels. This is achieved by using a Kitronik Air quality control hat, and reading the air quality values through it. This is an open-source project encouraging others to further build on this project, see the code behind it, and build an AIRWISE themselves 


# Instructions to Build the AIRWISE device

## Parts Required:

1.Kitronik Air Quality Control Hat for Pi  
2.LED indicator (optional)   
3.Peltier module (9V)*   
4.Heat-sink x2*   
5.Box fan (9V)*   
6.Micro limit switch   
7.Jumper wires   
8.Ultrasonic water atomiser/vaporiser   
9.Double Relay module   
10.Parts for case made according to 3d model provided (Recommended to 3print with PLA filament)   
11.Raspberry Pi  

## Software Required:

Pi imager  
MobaXterm

### Preparing the main modules

## Peltier/Dehumidifier

Take your Peltier module and apply thermal paste to one side then firmly attach the heatsink, do the same for the other side. Ensure that:  

A) The side of the heatsink the fan is attached to is the one that gets warm when voltage is applied. If you are not sure, wait till the device is fully assembled, then test.   

B) Also make sure that the fan is blowing into the heatsink as opposed to drawing in, if not, flip the fan so its blowing into the heatsink.  
The peltier module and box fan shall be attached in series (as shown in diagram)

Alternative: 
	You can also do what we have done for our prototype, which is use the internals of a mini dehumidifier, saving costs, however this may be more complex to achieve. 

 