# pico-w-mem-keyer
Uses the PicoW as a ham radio memory keyer
The project will have two keyers so far. (We may need to put the keyer for ProjectTouCans in its own repository eventually.)  

The keyer for Project TouCans is now in the air! There are two scripts at the moment for using the keyer.  
The first is a memory keyer: [simple_key.py]([url](https://github.com/hcarter333/pico-w-mem-keyer/blob/main/simple_key.py))
The second is a [keyer]([url](https://github.com/hcarter333/pico-w-mem-keyer/blob/main/mancwmsg.py)) for sending whatever message you like plus a few commands.
Commands:  
'P': reboot the radio by breakign the negative power line for 8 dots  
'F': make the keyer faster by reducing the dot time by 0.005 seconds  
'S': make the keyer slower by reducing hte dot time by 0.005 seconds 

The FT840 auto keyer:  
![image](https://github.com/hcarter333/pico-w-mem-keyer/assets/363004/76c67375-2dab-4599-bb34-cc3faf038c42)

The straight keyer now runs in JavaScript and has a practice mode:

https://github.com/user-attachments/assets/8e504a7b-ddb2-4598-a95f-efc6ba93cd30

