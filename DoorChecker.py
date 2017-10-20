#!/usr/bin/env python
from gpiozero import Button
from signal import pause
import time
from datetime import datetime
import subprocess
from string import Template

SLEEP_TIME  = 0.01

NOTIFY_LIST = []
with open('email.conf','r') as notify:
  for word in notify.read().split():
    NOTIFY_LIST.append(word)

ACTPINS = {}
with open('pipins.conf','r') as my_file:
   for line in my_file:
     l_split = line.split()
     ACTPINS[int(l_split[0])] = l_split[1]

def current_date (fmt="%a %d-%m-%Y @ %H:%M:%S"):
    return datetime.strftime(datetime.now(), fmt)

NOTIFY_CMD = {pin: Template("""echo "$date $sensor $state" | mail -s "Pi: $sensor $state" $email""") for pin in ACTPINS}
 
def notify (id, state, sensor_name):
    """Send each of the email addresses in NOTIFY_LIST a message"""
    for email in NOTIFY_LIST:
        shell_cmd = NOTIFY_CMD[id].substitute(date=current_date(),
                                  state=state, sensor=sensor_name, email=email)
        proc = subprocess.Popen(shell_cmd, shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_value, stderr_value = proc.communicate()
        with open('log.txt', 'a') as f:
          f.write('{}\n'.format(shell_cmd))
 
def do_action(button):
  # function to send email etc will only run when opened or closed
  state = 'closed' if button.is_pressed else 'opened'
  notify(button.pin, state, ACTPINS[button.pin])
  print(state)

buttons = {}
for id in ACTPINS:
  buttons[id] = Button(id)
  buttons[id].when_pressed = do_action
  buttons[id].when_released = do_action
  print(id)
  print(buttons)
  print(ACTPINS)
  print(NOTIFY_LIST)

pause()
