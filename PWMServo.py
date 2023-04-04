from machine import Pin, PWM
import time
import network
import BlynkLib


#set PWM
pwm = PWM(Pin(15)) 
pwm.freq(50) #20ms PWM period


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('SSID','Password')
 
BLYNK_AUTH = "YOUR BLYNK-AUTH-TOKEN"
 
# connect the network       
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    time.sleep(1)
 
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    ip=wlan.ifconfig()[0]
    print('IP: ', ip)
    
 
"Connection to Blynk"
# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)
 
# Register virtual pin handler
@blynk.on("V0") #virtual pin V0
def v0_write_handler(value): #read the value
    if int(value[0]) == 1:
        print("ON")
        print("Left")
        pwm.duty_ns(1000000) #dutyCycle 1ms
        time.sleep(1)
        print("Middle")
        pwm.duty_ns(1500000) #dutyCycle 1.5ms
        time.sleep(1)
        print("Right")
        pwm.duty_ns(2000000) #dutyCycle 2ms
        time.sleep(1)
        print("Middle")
        pwm.duty_ns(1500000) #dutyCycle 1.5ms
        time.sleep(1)
    else:
        print("OFF")
        pwm.deinit()
        time.sleep(1)
        
while True:
    blynk.run()