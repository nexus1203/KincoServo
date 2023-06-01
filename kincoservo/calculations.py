import struct


def value_to_registers(value: int) -> list:
    """Convert a value to Modbus registers (2 bytes each).

    Args:
        value (int): The value to convert.
    Returns:
        list: The value as a list of two Modbus registers.
    """
    # convert to 4 bytes
    bytes_value = struct.pack('<i', int(value))
    # convert to 2 registers
    registers = list(struct.unpack('<HH', bytes_value))
    return registers


def registers_to_value(registers: list) -> int:
    """Convert Modbus registers (2 bytes each) to a value.
        must be only 2 registers in the list.
    Args:
        registers (list): The registers to convert.
    Returns:
        int: The value.    
    """
    # convert the two Modbus registers to a sequence of 4 bytes in little-endian byte order
    data = struct.pack('<HH', *registers)
    # unpack the bytes into a 32-bit integer in little-endian byte order
    value = struct.unpack('<i', data)[0]
    return value


def rpm_to_registers(value, scale_factor=2730.665):
    """
    Convert RPM to Modbus registers (2 bytes each)
    Args:
        value (int): rpm value to convert.
        scale_factor (float): conversion factor for the register to rpm.
    Returns:
        list: register bytes. 
    """
    # Multiply the input value by the scaling factor and convert to integer
    scaled_value = int(value * scale_factor)

    return value_to_registers(scaled_value)


def registers_to_rpm(registers, scale_factor=2730.665):
    """
    Convert Modbus registers (2 bytes each) to RPM
    Args:
        register (list): registers representing the rpm.
        scale_factor (float): conversion factor for the register to rpm.
    Returns:
        int: rpm value. 
    """
    # convert registers to value (integer)
    value = registers_to_value(registers)
    rpm = value / scale_factor
    return rpm


def radians_to_registers(value, encoder_resolution=10000):
    """
    Convert radians to Modbus registers (2 bytes each)
    Args:
        value (float): radians value.
        encoder_resolution (int): encoder count.
    Returns:
        list: register bytes. 
    """

    # convert radians to encoder counts (integer) 360 degrees = 10000 encoder counts
    encoder_counts = int(value * encoder_resolution / (2 * 3.14159))
    return value_to_registers(encoder_counts)


def registers_to_radians(registers, encoder_resolution=10000):
    """
    Convert Modbus registers (2 bytes each) to radians
    Args:
        value (list): register bytes.
        encoder_resolution (int): encoder count.
    Returns:
        float: radians. 
    """
    # convert registers to value (integer)
    value = registers_to_value(registers)
    radians = value * (2 * 3.14159) / encoder_resolution
    return radians
