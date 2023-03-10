from kincoservo.controller import ServoController
from time import sleep

control = ServoController('COM1', 1)
control.reset()
control.quick_stop()
# control.homing()

# # control.set_velocitymode(direction="backward")
# # control.set_velocitymode(direction="forward")
# control.set_velocity(1000)
# # print(control.get_velocity())

now_position = control.get_position(radians=False)
print(now_position)
# print()
# print()
control.set_positionmode()
control.set_position(now_position - 250 * 21 * 1 * 10000, radians=False)
# # sleep(1)
control.set_positionmode_Speed(1000)
sleep(1)
control.set_positionmode_Speed(500)
sleep(5)
control.set_positionmode_Speed(100)
sleep(3)
control.set_positionmode_Speed(1000)
sleep(1)
# # control.set_positionmode_Speed(500)
# sleep(1)
# control.set_position(now_position + 21 * 10000, radians=False)
# # print(control.get_position(radians=False))

# while True:
#     # check if the user wants to quit
#     if input("q to quit, anything else to continue: ") == "q":
#         control.quick_stop()
#         control.reset()
#         break
#     else:

#         now_position = control.get_position(radians=False)
#         set_position = now_position - 1000
#         control.set_position(set_position, radians=False)
# control.stop()
