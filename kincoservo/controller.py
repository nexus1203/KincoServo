import minimalmodbus
import serial
from time import perf_counter
from .calculations import (rpm_to_registers, registers_to_rpm,
                           registers_to_value, value_to_registers,
                           registers_to_radians, radians_to_registers)
from .registers import ServoFD1X3 as Servo


class ServoController:

    def __init__(self, port, address):
        self.instrument = minimalmodbus.Instrument(port, address, debug=True)
        self.instrument.serial.baudrate = 115200
        self.instrument.serial.parity = serial.PARITY_NONE
        self.instrument.serial.bytesize = 8
        self.instrument.serial.stopbits = 1
        self.instrument.mode = minimalmodbus.MODE_RTU
        self.instrument.serial.timeout = 0.5
        self.com_delay = 0

        self.opmode = None  # position, velocity

    def reset(self, ):
        """reset the servo to factory settings
        """
        self.instrument.write_register(Servo.CONTROL["Register"],
                                       Servo.CONTROL["Value"]["Reset"],
                                       functioncode=6)
        self.opmode = None

    def set_velocitymode(self, direction='forward'):
        """set the servo to velocity mode

        Args:
            direction (str, optional): forward or backward. Defaults to 'forward'.
        """

        self.instrument.write_register(Servo.CONTROL["Register"],
                                       Servo.CONTROL["Value"]["Stop"],
                                       functioncode=6)
        self.instrument.write_register(Servo.OPMODE["Register"],
                                       Servo.OPMODE["Value"]["Velocity"],
                                       functioncode=6)
        self.instrument.write_register(
            Servo.VelocityDirection["Register"],
            Servo.VelocityDirection["Value"][direction],
            functioncode=6)
        self.instrument.write_registers(
            Servo.VelocityCommand["Register"],
            rpm_to_registers(0),
        )
        self.instrument.write_register(Servo.CONTROL["Register"],
                                       Servo.CONTROL["Value"]["Start"],
                                       functioncode=6)
        self.opmode = 'velocity'
        
    def set_profileacc(self, acc):
      """set the acceleration of the servo

        Args:
            acc (int): acc value (conversion same as rpm)
        """
        self.instrument.write_registers(
            Servo.ProfileAcceleration["Register"],
            rpm_to_registers(acc),
        )

    def set_velocity(self, rpm):
        """set the velocity of the servo

        Args:
            rpm (int): rpm value
        """
        if self.opmode != 'velocity':
            print("Servo is not in velocity mode, setting to velocity mode")
            self.set_velocitymode()

        self.instrument.write_registers(
            Servo.VelocityCommand["Register"],
            rpm_to_registers(rpm),
        )

    def get_velocity(self, ):
        """get the velocity of the servo

        Returns:
            int: rpm value
        """
        return registers_to_rpm(
            self.instrument.read_registers(
                Servo.VelocityFeedback["Register"],
                Servo.VelocityFeedback["read_length"]))

    def set_positionmode(self, ):
        """set the servo to absoute position mode

        Args:
            position (float): position in radians if radians is True, otherwise in encoder counts
            rpm (int): speed in rpm
            radians (bool, optional): Defaults to False.
        """
        self.instrument.write_register(Servo.CONTROL["Register"],
                                       Servo.CONTROL["Value"]["Stop"],
                                       functioncode=6)
        self.instrument.write_register(Servo.CONTROL["Register"],
                                       Servo.CONTROL["Value"]["Start"],
                                       functioncode=6)
        self.instrument.write_register(Servo.OPMODE["Register"],
                                       Servo.OPMODE["Value"]["Position"],
                                       functioncode=6)
        # set the position to current position
        now_pos = self.get_position(radians=False)
        self.instrument.write_registers(
            Servo.PositionCommand["Register"],
            value_to_registers(now_pos),
        )

        # set the position speed to 100
        self.instrument.write_registers(
            Servo.PositionSpeedCommand["Register"],
            rpm_to_registers(100),
        )

        self.instrument.write_register(
            Servo.CONTROL["Register"],
            Servo.CONTROL["Value"]["AbsolutePosition"]["Set1"],
            functioncode=6)
        self.instrument.write_register(
            Servo.CONTROL["Register"],
            Servo.CONTROL["Value"]["AbsolutePosition"]["Set2"],
            functioncode=6)
        self.instrument.write_register(Servo.CONTROL["Register"],
                                       0x103F,
                                       functioncode=6)
        self.instrument.write_register(
            Servo.CONTROL["Register"],
            Servo.CONTROL["Value"]["StartAbsolutePosition"],
            functioncode=6)
        self.opmode = 'position'

    def set_positionmode_Speed(self, rpm):
        # set the position speed to 0
        self.instrument.write_registers(
            Servo.PositionSpeedCommand["Register"],
            rpm_to_registers(rpm),
        )

    def set_position(self, value, radians=True):
        """set the position of the servo in radians

        Args:
            value (float): angle in radians if radians is True, otherwise in encoder counts
            radians (bool, optional): Defaults to True.
        """
        if self.opmode != 'position':
            print("Servo is not in position mode, setting to position mode")
            self.set_positionmode()
        if radians:
            self.instrument.write_registers(
                Servo.PositionCommand["Register"],
                radians_to_registers(value),
            )
        else:
            self.instrument.write_registers(
                Servo.PositionCommand["Register"],
                value_to_registers(value),
            )

    def get_position(self, radians=True):
        """get the position of the servo in radians

        Returns:
            float: angle in radians, or the encoder value
        """
        if radians:
            return registers_to_radians(
                self.instrument.read_registers(
                    Servo.PositionFeedback["Register"],
                    Servo.PositionFeedback["read_length"]))
        else:
            return registers_to_value(
                self.instrument.read_registers(
                    Servo.PositionFeedback["Register"],
                    Servo.PositionFeedback["read_length"]))

    def start_homing(self, ):
        self.instrument.write_register(Servo.CONTROL["Register"],
                                       Servo.CONTROL["Value"]["Stop"],
                                       functioncode=6)
        self.instrument.write_register(
            Servo.CONTROL["Register"],
            Servo.CONTROL["Value"]["Homing"]["Set1"],
            functioncode=6)
        self.instrument.write_register(Servo.OPMODE["Register"],
                                       Servo.OPMODE["Value"]["Home"],
                                       functioncode=6)
        self.instrument.write_register(Servo.HomingMethod["Register"],
                                       Servo.HomingMethod["Value"],
                                       functioncode=6)
        self.instrument.write_registers(Servo.HomingSpeedSwitch["Register"],
                                        rpm_to_registers(50))
        self.instrument.write_registers(Servo.HomingSpeedZero["Register"],
                                        rpm_to_registers(25))
        self.instrument.write_register(
            Servo.CONTROL["Register"],
            Servo.CONTROL["Value"]["Homing"]["Set2"],
            functioncode=6)

    def stop(self, ):
        """stop the servo
        """
        self.instrument.write_register(Servo.CONTROL["Register"],
                                       Servo.CONTROL["Value"]["Stop"],
                                       functioncode=6)
        self.opmode = None

    def quick_stop(self, ):
        """stop the servo
        """
        self.instrument.write_register(Servo.CONTROL["Register"],
                                       Servo.CONTROL["Value"]["QuickStop"],
                                       functioncode=6)
        self.opmode = None
