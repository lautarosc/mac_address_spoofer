import subprocess
import optparse 

# Function to capture and parse user input 
def user_arguments():
    
    # Parser object
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='Use this command to select which interface you want to change (i.e.: eth0, wlan, etc)')
    parser.add_option('-m', '--mac', dest='new_mac', help='Use this command to choose your new MAC address')
    (options, arguments) = parser.parse_args()

    # If the user doesn't enter an interface or MAC address, the script will show an error
    if not options.interface:
        parser.error('[-] Please enter an interface to continue. You can use --help for more information')
    elif not options.new_mac:
        parser.error('[-] Please enter a MAC address to continue. You can use --help for more information')
    return options

# Function to change the MAC address, with the user input captured
def change_mac(interface, new_mac):
    
    # Turn interface down
    subprocess.call(['ifconfig', interface, 'down'])

    # Change MAC
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])

    # Turn interface on 
    subprocess.call(['ifconfig', interface, 'up'])

    print('[+] Done! Your new MAC is:', new_mac)


# Capture and parse user input
options = user_arguments()

# Execute MAC change with captured user input
change_mac(options.interface, options.new_mac)
