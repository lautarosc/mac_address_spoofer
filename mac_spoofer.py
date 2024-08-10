import subprocess
import optparse
import re 

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

    #print('[+] Done! Your new MAC is:', new_mac)

# Find current MAC address
def find_mac_address(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface])

    # Subprocess returns ifconfig_result in bytes format. It can be turned into str format with:
    ifconfig_result = ifconfig_result.decode('utf-8')

    # Search for MAC address with regex
    mac_address_regex = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_regex:
        return mac_address_regex.group(0)
    else:
        print('\n[-] Sorry! Couldn\'t find a MAC address')

# Capture and parse user input
options = user_arguments()

# Show user's MAC address before change
current_mac = find_mac_address(options.interface)
print("\n[+] Your current MAC address is", str(current_mac))

# Attempt to change MAC address
change_mac(options.interface, options.new_mac)

# Check if MAC changed, and inform the user the results either way
def check_mac_change(interface, new_mac):
    current_mac = find_mac_address(options.interface)
    if current_mac == options.new_mac:
        print("\n[+] Done! Your new MAC is:", options.new_mac)
    else:
        print("\n[-] Something went wrong! MAC adress could not be changed. Try again!")

check_mac_change(options.interface, options.new_mac)
