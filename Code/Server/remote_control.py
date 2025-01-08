import time
from Motor import *
import RPi.GPIO as GPIO
from servo import *
from PCA9685 import PCA9685
import socket

class RemoteControl:
    def __init__(self):
        GPIO.setwarnings(False)
        self.trigger_pin = 27
        self.echo_pin = 22
        self.MAX_DISTANCE = 300 # define the maximum measuring distance, unit: cm
        self.timeOut = self.MAX_DISTANCE * 60 # calculate timeout according to the maximum measuring distance
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def open_socket_and_control_car(self):
        self.PWM = Motor()

        # bt_server
        # The address of Raspberry Pi bluetooth adapter on the server. The server might have multiple bluetooth adapters
        hostMACAddress = "D8:3A:DD:70:92:5D"
        port = 1 # Port must be set explicitly (typically 1 for Bluetooth RFCOMM)
        backlog = 1
        size = 1024

        # Create a bluetooth socket
        server_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        server_sock.bind((hostMACAddress, port))
        server_sock.listen(backlog)

        print(f"Listening on {hostMACAddress}, port {port}")

        try:
            client_sock, client_info = server_sock.accept()
            print(f"Accepted connection from {client_info}")

            while True:
                data = client_sock.recv(size)
                if data:
                    message = data.decode("utf-8")

                    match (message):
                        case ('w'):
                            print("Going forward...")
                            self.PWM.setMotorModel(1000, 1000, 1000, 1000)
                            time.sleep(1)
                            self.PWM.setMotorModel(0, 0, 0, 0)
                        case ('a'):
                            print("Turning left...")
                            self.PWM.setMotorModel(-1500, -1500, 2000, 2000)
                            time.sleep(1)
                            self.PWM.setMotorModel(0, 0, 0, 0)
                        case ('d'):
                            print("Turning right...")
                            self.PWM.setMotorModel(2000, 2000, -1500, -1500)
                            time.sleep(1)
                            self.PWM.setMotorModel(0, 0, 0, 0)
                        case ('s'):
                            print("Reversing...")
                            self.PWM.setMotorModel(-1000, -1000, -1000, -1000)
                            time.sleep(1)
                            self.PWM.setMotorModel(0, 0, 0, 0)
                        case _:
                            print("Unrecognized instruction.")

                    print(f"Received: {message}")
                    client_sock.send(data) # Echo back the received data
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print("Closing sockets")
            client_sock.close()
            server_sock.close()

remote_control = RemoteControl()

if __name__ == '__main__':
    remote_control.open_socket_and_control_car()

# import time
# from Motor import *
# import RPi.GPIO as GPIO
# from servo import *
# from PCA9685 import PCA9685


# class Ultrasonic:
#     def __init__(self):
#         GPIO.setwarnings(False)
#         self.trigger_pin = 27
#         self.echo_pin = 22
#         self.MAX_DISTANCE = 300  # define the maximum measuring distance, unit: cm
#         self.timeOut = self.MAX_DISTANCE * 60  # calculate timeout according to the maximum measuring distance
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.trigger_pin, GPIO.OUT)
#         GPIO.setup(self.echo_pin, GPIO.IN)

#     def pulseIn(self, pin, level, timeOut):  # obtain pulse time of a pin under timeOut
#         t0 = time.time()
#         while (GPIO.input(pin) != level):
#             if ((time.time() - t0) > timeOut * 0.000001):
#                 return 0;
#         t0 = time.time()
#         while (GPIO.input(pin) == level):
#             if ((time.time() - t0) > timeOut * 0.000001):
#                 return 0;
#         pulseTime = (time.time() - t0) * 1000000
#         return pulseTime

#     def get_distance(self):  # get the measurement results of ultrasonic module,with unit: cm
#         distance_cm = [0, 0, 0, 0, 0]
#         for i in range(5):
#             GPIO.output(self.trigger_pin, GPIO.HIGH)  # make trigger_pin output 10us HIGH level
#             time.sleep(0.00001)  # 10us
#             GPIO.output(self.trigger_pin, GPIO.LOW)  # make trigger_pin output LOW level
#             pingTime = self.pulseIn(self.echo_pin, GPIO.HIGH, self.timeOut)  # read plus time of echo_pin
#             distance_cm[i] = pingTime * 340.0 / 2.0 / 10000.0  # calculate distance with sound speed 340m/s
#         distance_cm = sorted(distance_cm)
#         return int(distance_cm[2])

#     def run_motor(self, L, M, R):
#         if (L < 30 and M < 30 and R < 30) or M < 30:
#             self.PWM.setMotorModel(-1000, -1000, -1000, -1000)
#             time.sleep(0.1)
#             if L < R:
#                 self.PWM.setMotorModel(1000, 1000, -1000, -1000)
#             else:
#                 self.PWM.setMotorModel(-1000, -1000, 1000, 1000)
#         elif L < 30 and M < 30:
#             PWM.setMotorModel(1500, 1500, -1500, -1500)
#             time.sleep(0.1)
#         elif R < 30 and M < 30:
#             PWM.setMotorModel(-1500, -1500, 1500, 1500)
#             time.sleep(0.1)
#         elif L < 20:
#             PWM.setMotorModel(1500, 1500, -500, -500)
#             time.sleep(0.1)
#             if L < 10:
#                 PWM.setMotorModel(1500, 1500, -1000, -1000)
#                 time.sleep(0.1)
#         elif R < 20:
#             PWM.setMotorModel(-500, -500, 1500, 1500)
#             time.sleep(0.1)
#             if R < 10:
#                 PWM.setMotorModel(-1000, -1000, 1000, 1000)
#                 time.sleep(0.1)
#         else:
#             self.PWM.setMotorModel(600, 600, 600, 600)
#             time.sleep(0.1)

#     def run(self):
#         self.PWM = Motor()
#         self.pwm_S = Servo()

#         while True:
#             self.pwm_S.setServoPwm("0", 90)
#             time.sleep(0.1)
#             M = self.get_distance()

#             if M < 30:
#                 self.pwm_S.setServoPwm("0", 30)
#                 time.sleep(0.2)
#                 L = self.get_distance()
#                 self.pwm_S.setServoPwm("0", 151)
#                 time.sleep(0.2)
#                 R = self.get_distance()
#                 self.run_motor(L, M, R)
#                 self.pwm_S.setServoPwm("0", 90)
#             else:
#                 self.run_motor(20, M, 20)

#     def run0(self):
#         self.PWM = Motor()
#         self.pwm_S = Servo()

#         for i in range(30, 151, 60):
#             self.pwm_S.setServoPwm('0', i)
#             time.sleep(0.2)
#             if i == 30:
#                 L = self.get_distance()
#             elif i == 90:
#                 M = self.get_distance()
#             else:
#                 R = self.get_distance()
#         while True:
#             for i in range(90, 30, -60):
#                 self.pwm_S.setServoPwm('0', i)
#                 time.sleep(0.2)
#                 if i == 30:
#                     L = self.get_distance()
#                 elif i == 90:
#                     M = self.get_distance()
#                 else:
#                     R = self.get_distance()
#                 self.run_motor(L, M, R)
#             for i in range(30, 151, 60):
#                 self.pwm_S.setServoPwm('0', i)
#                 time.sleep(0.2)
#                 if i == 30:
#                     L = self.get_distance()
#                 elif i == 90:
#                     M = self.get_distance()
#                 else:
#                     R = self.get_distance()
#                 self.run_motor(L, M, R)


# ultrasonic = Ultrasonic()
# # Main program logic follows:
# if __name__ == '__main__':
#     print('Program is starting ... ')
#     try:
#         # ultrasonic.run()
#         ultrasonic.run0()
#     except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
#         PWM.setMotorModel(0, 0, 0, 0)
#         ultrasonic.pwm_S.setServoPwm('0', 90)