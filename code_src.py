"""Circuit Python script for testing debug clip adapters
"""
import board as hw
import digitalio as dg
import time as t

#
#   The test procedure is simple, assert one output and check the correct, single,
# input is also asserted.
#

#
#   Define the output pins, these are on the connection to
# the debug clip.
#
#   These pins are initially set to input direction. As each pin
# is tested, it is set to output, its 'pair' pin is checked for
# the correct level and all others are checked to test for shorts.
#
Gnd_O = dg.DigitalInOut(hw.D13)
Gnd_O.direction = dg.Direction.OUTPUT

Swo_O = dg.DigitalInOut(hw.D12)
Swo_O.direction = dg.Direction.OUTPUT

nReset_O = dg.DigitalInOut(hw.D11)
nReset_O.direction = dg.Direction.OUTPUT

Swdio_O = dg.DigitalInOut(hw.D10)
Swdio_O.direction = dg.Direction.OUTPUT

Swck_O = dg.DigitalInOut(hw.D9)
Swck_O.direction = dg.Direction.OUTPUT

VTRef_O = dg.DigitalInOut(hw.D6)
VTRef_O.direction = dg.Direction.OUTPUT

#
# Define the input pins, these are the connections to the debug probe connector
#

Gnd_I1 = dg.DigitalInOut(hw.A4)
Gnd_I1.direction = dg.Direction.INPUT
Gnd_I1.pull = dg.Pull.DOWN

Gnd_I2 = dg.DigitalInOut(hw.A5)
Gnd_I2.direction = dg.Direction.INPUT
Gnd_I2.pull = dg.Pull.DOWN

Gnd_I3 = dg.DigitalInOut(hw.SCK)
Gnd_I3.direction = dg.Direction.INPUT
Gnd_I3.pull = dg.Pull.DOWN

Swck_I = dg.DigitalInOut(hw.A0)
Swck_I.direction = dg.Direction.INPUT
Swck_I.pull = dg.Pull.DOWN

Swo_I = dg.DigitalInOut(hw.A1)
Swo_I.direction = dg.Direction.INPUT
Swo_I.pull = dg.Pull.DOWN

nReset_I = dg.DigitalInOut(hw.A3)
nReset_I.direction = dg.Direction.INPUT
nReset_I.pull = dg.Pull.DOWN

VTRef_I = dg.DigitalInOut(hw.MOSI)
VTRef_I.direction = dg.Direction.INPUT
VTRef_I.pull = dg.Pull.DOWN

Swdio_I = dg.DigitalInOut(hw.MISO)
Swdio_I.direction = dg.Direction.INPUT
Swdio_I.pull = dg.Pull.DOWN

#
# Define the access indices for the pin states
#
pin_out = 0
pin_in = 1
pin_name = 2

#
#   Define the list of outputs and expected inputs
#
pin_states = [
    [Gnd_O, Gnd_I1, "GND 1"],
    [Gnd_O, Gnd_I2, "GND 2"],
    [Gnd_O, Gnd_I3, "GND 3"],
    [Swdio_O, Swdio_I, "SWDIO"],
    [Swo_O, Swo_I, "SWO"],
    [nReset_O, nReset_I, "nRESET"],
    [Swck_O, Swck_I, "SWCK"],
    [VTRef_O, VTRef_I, "VTRef"],
]

#
#   Define the two status LED pins
#
LED_Red = dg.DigitalInOut(hw.SDA)
LED_Red.direction = dg.Direction.OUTPUT
LED_Red.value = True

LED_Green = dg.DigitalInOut(hw.SCL)
LED_Green.direction = dg.Direction.OUTPUT
LED_Green.value = True

#
#   Define the pin for the Start switch, it is
# active low with external pull-up
#
Start_switch = dg.DigitalInOut(hw.D5)
Start_switch.direction = dg.Direction.INPUT
Start_switch.pull = dg.Pull.UP  # TODO Remove for hardware

#
#   Check the passed output pin is connected to ONLY
# the assigned input pin
#
def test_inputs(output_pin):
    result = True
    #
    # Assert the test output
    #
    output_pin.value = True
    for pin_index in range(len(pin_states)):
        pin_input = pin_states[pin_index][pin_in]
        #
        # Check if the current pin is the output being tested
        #
        if output_pin == pin_states[pin_index][pin_out]:
            if pin_input.value == False:
                result = False
        else:
            if pin_input.value == True:
                result = False
    #
    # Negate the test output
    #
    output_pin.value = False
    return result


while True:
    led_red = False
    error_count = 0
    #
    if Start_switch.value == False:
    #
    # Test the board
    #
        for output_index in range(len(pin_states)):
            led_red = not led_red
            LED_Red.value = led_red
            LED_Green.value = not led_red
            #
            pin_states[output_index][pin_out].direction = dg.Direction.OUTPUT
            if test_inputs(pin_states[output_index][pin_out]) == True:
                print(pin_states[output_index][pin_name] + " passed")
            else:
                print(pin_states[output_index][pin_name] + " failed")
                error_count += 1
            t.sleep(0.2)
        if error_count == 0:
            print("Scan completed correctly")
            LED_Red.value = False
            LED_Green.value = True
        else:
            print(f"Scan of {str(len(pin_states))} pins completed with {str(error_count)}  errors")
            LED_Red.value = True
            LED_Green.value = False
        print()
        print()
        while True:
            t.sleep(0.15)
            if Start_switch.value == False:
                break
    LED_Red.value = True
    LED_Green.value = True
    