import machine
import time
import random


leds = [
    machine.Pin(19, machine.Pin.OUT), 
    machine.Pin(18, machine.Pin.OUT), 
    machine.Pin(17, machine.Pin.OUT)
]

buttons = [
    machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP), 
    machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP), 
    machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
]

buzzer = machine.PWM(machine.Pin(16))

game_sequence = []

NOTES = {
    'G4': 392, 'A4': 440, 'AS4': 466, 'B4': 494, 'C5': 523, 'CS5': 554, 
    'D5': 587, 'DS5': 622, 'E5': 659, 'F5': 698, 'FS5': 740, 'G5': 784, 
    'A5': 880, 'B5': 988, '0': 0
}

def play_tone(freq, duration):
    if freq > 0:
        buzzer.freq(freq)
        buzzer.duty_u16(4000)
    time.sleep(duration)
    buzzer.duty_u16(0)
    time.sleep(0.03)

def rick_roll_animation():
    melody = [
        ('A4', 0.15), ('B4', 0.15), ('D5', 0.15), ('B4', 0.15), # Ne-ver gon-na
        ('FS5', 0.35), ('FS5', 0.35), ('E5', 0.6),              # give you up
        ('0', 0.1),
        ('A4', 0.15), ('B4', 0.15), ('D5', 0.15), ('B4', 0.15), # Ne-ver gon-na
        ('E5', 0.35), ('E5', 0.35), ('D5', 0.3), ('CS5', 0.15), ('B4', 0.3), # let you down
        ('0', 0.1),
        ('A4', 0.15), ('B4', 0.15), ('D5', 0.15), ('B4', 0.15), # Ne-ver gon-na
        ('D5', 0.4), ('E5', 0.2), ('CS5', 0.3), ('B4', 0.2), ('A4', 0.3), # run a-round and
        ('A4', 0.2), ('E5', 0.4), ('D5', 0.6)                   # de-sert you
    ]
    
    print(" NEVER GONNA GIVE YOU UP! ")
    for note, duration in melody:
        if note == '0':
            time.sleep(duration)
        else:
            play_tone(NOTES[note], duration)

def flash_led_and_beep(index, speed=0.4):
    leds[index].value(1)
    buzzer.freq(700 + (index * 150))
    buzzer.duty_u16(3000)
    time.sleep(0.15)
    buzzer.duty_u16(0)
    time.sleep(speed - 0.15)
    leds[index].value(0)
    time.sleep(0.05)

def lose_sequence():
    print(" RICKROLLED!")
    for led in leds: led.value(1)
    rick_roll_animation()
    for led in leds: led.value(0)

def wait_for_player_input():
    while True:
        for i in range(3):
            if buttons[i].value() == 0: 
                leds[i].value(1)
                buzzer.freq(700 + (i * 150))
                buzzer.duty_u16(3000)
                while buttons[i].value() == 0:
                    time.sleep(0.01)
                buzzer.duty_u16(0)
                leds[i].value(0)
                time.sleep(0.1)
                return i

print("--- SIMON SAYS GAME START ---")
time.sleep(1)

while True:
    game_sequence.append(random.randint(0, 2))
    time.sleep(0.4)
    
    for step in game_sequence:
        flash_led_and_beep(step)
    
    for step in game_sequence:
        if wait_for_player_input() != step:
            lose_sequence()
            game_sequence = [] 
            time.sleep(1)
            print("\n--- NEW GAME ---")
            break
    else:
        print("Round cleared!")
        time.sleep(1.5)
