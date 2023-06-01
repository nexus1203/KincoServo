# this file consist of all the Kinco FD1x3 servo registers used in the project


class ServoFD1X3:
    CONTROL = {
        "R/W": "W",
        "Register": 0x3100,
        "functioncode": 6,
        "Value": {
            "Stop": 0x0006,
            "Start": 0x000F,
            "Reset": 0x0080,
            "QuickStop": 0x000B,
            "AbsolutePosition": {
                "Set1": 0x002F,
                "Set2": 0x003F
            },
            "StartAbsolutePosition": 0x103F,
            "Homing": {
                "Set1": 0x000F,
                "Set2": 0x001F
            }
        }
    }

    STATUS = {"R/W": "R", "Register": 0x3000, "functioncode": 3}

    OPMODE = {
        "R/W": "W",
        "Register": 0x3500,
        "functioncode": 6,
        "Value": {
            "Position": 1,
            "Velocity": 3,
            "Torque": 4,
            "Home": 6,
        }
    }

    VelocityDirection = {
        "R/W": "W",
        "Register": 0x4700,
        "functioncode": 6,
        "Value": {
            "forward": 0,
            "backward": 1
        }
    }

    VelocityCommand = {"R/W": "W", "Register": 0x6F00, "functioncode": 10}

    VelocityFeedback = {"R/W": "R", "Register": 0x3B00, "read_length": 2}

    PositionCommand = {"R/W": "W", "Register": 0x4000, "functioncode": 10}

    PositionSpeedCommand = {"R/W": "W", "Register": 0x4A00, "functioncode": 10}

    PositionFeedback = {"R/W": "R", "Register": 0x3700, "read_length": 2}
    
    ProfileAcceleration = { "R/W": "W", "Register": 0x4B00, "functioncode": 6}

    HomingMethod = {
        "R/W": "W",
        "Register": 0x4D00,
        "Value": 19,  # to the home switch
        "functioncode": 6,
    }

    HomingModes = {}

    HomingSpeedSwitch = {
        "R/W": "W",
        "Register": 0x5010,
        "functioncode": 10,
    }

    HomingSpeedZero = {
        "R/W": "W",
        "Register": 0x5020,
        "functioncode": 10,
    }
