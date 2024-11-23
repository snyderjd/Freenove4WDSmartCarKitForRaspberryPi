[200~# IoT Devices Report

### Links to Items
- [CanaKit Raspberry Pi 4 4GB Starter Kit](https://www.amazon.com/dp/B07V5JTMV9?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)
- [Freenove 4WD Smart Car Kit for Raspberry Pi](https://www.amazon.com/dp/B07YD2LT9D?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)
- [18650 Rechargeable Batteries and Charger](https://www.amazon.com/dp/B0CP6V26QX?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)

### Step 1: Set up the Raspberry Pi and Assemble the Car
- Used the Raspberry Pi docs to set up the Pi with the micro SD card
	- Install OS image on the microSD card using the imaging tool
	- Can log in to the Pi either via SSH or VNC
- Assembled the car according to the Freenove tutorial instructions
	- I didn't have any prior experience with small electronics. So it took a little while but it was pretty straightforward

### Step 2: Test the car
- Used some built-in test functions from the Freenove tutorial to test the various components and sensors on the car including:
	- Motors
	- ADC module
	- Infrared line tracking module
	- LEDs
	- Buzzer
	- Servo
	- Ultrasonic module
	- Camera

### Step 3: Obstacle avoidance and other functions
- Testing and tweaking the obstacle avoidance functions. Initially did not work at all and I came across a few problems that I fixed, which helped quite a bit.
	- Realized my servos weren't calibrated properly. I had to unmount the servo assembly, re-run the calibration functions, and re-mount the servos.
	- Realized the vertical servo was mounted facing slightly down. Re-mounted it to face slightly up instead which seemed to help.
	- Played around a little with things like how close to let the car get to objects before turning and how long to let the motors run while turning.
	- One main issue is how much traction the car has. If the car does not have good traction the motors need to run longer for the car to actually turn far enough to turn away from an obstacle. Otherwise the algorithm thinks the car has turned when it actually just spun its wheels without turning much and is still facing the obstacle.
- I'd like to keep working on the obstacle avoidance and mapping problems listed in the appendices
- Interesting and fun to work on problems that involve both hardware and software

### Videos
- Obstacle avoidance demo video
