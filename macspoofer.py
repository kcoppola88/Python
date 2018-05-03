import subprocess
import sys
import platform
import fileinput
import re


def macChanger():
    while True:    
        print("\n")
        s = input("Please enter the host's MAC address without colons or dashes: ").lower() #can enter the MAC faster this way
        if len(s) != 12:
            print("MAC address must be exactly 12 characters. Please enter it again. \n")
            pass
        else:
            if bool(re.match("[0-9a-f]{12}$", s)) == False: #regex is shorter/faster, only matching for 12 hex digits
                print("Make sure MAC is only hex and no colons or dashes. Please enter it again. \n")
                pass
            else:
                s = s[:2] + ":" + s[2:4] + ":" + s[4:6] + ":" + s[6:8] + ":" + s[8:10] + ":" + s[10:12] #builds mac in macchanger accepted format        
                command = subprocess.run(["macchanger","--mac=" + s, "eth0"]) #change mac to known internal mac address
                break
                
def hostChanger():
    while True:
        print("\n")

        with open('/etc/hosts') as f:
            data = f.readline()
        hosts = str(data)

        with open('/etc/hostname') as g:
            moredata = g.readline()
        hostname = str(moredata)

        global originalHostname #global to store original host name for revert function below
        originalHostname = hosts

        print("\n")
        spoof = input("Please enter the host name you want to spoof: ").lower()

        global spoofName #global to store spoof name for revert function below
        spoofName = spoof    

        for line in fileinput.input('/etc/hosts', inplace=True): #edit /etc/hosts file
            if hosts in line:
                line = line.replace(hosts, spoof.strip())
                print(line)    
        
        for line in fileinput.input('/etc/hostname', inplace=True): #edit /etc/hostname file, too
            if hostname in line:
                line = line.replace(hostname, spoof.strip())
                print(line)        
        print("\n")
        command1 = subprocess.run(["/etc/init.d/hostname.sh"]) #forces hostname change without reboot
        command2 = subprocess.run(["service", "networking", "force-reload"])
        command3 = subprocess.run(["service", "network-manager","force-reload"])
        break


def macChangeBack():
    input("Press enter to change MAC address back to original.")
    print("\n")
    command = subprocess.run(["macchanger","-p","eth0"]) #change mac back to true mac address

def hostChangeBack():
    print("\n")
    input("Press enter to change Hostname back to original.")
    print("\n")
    
    for line in fileinput.input('/etc/hosts', inplace=True):
        if spoofName in line:
            line = line.replace(spoofName, originalHostname.strip()) #reverts hostname change from previous function
            print(line)
    for line in fileinput.input('/etc/hostname', inplace=True): #reverts hostname file, too
        if spoofName in line:
            line = line.replace(spoofName, originalHostname.strip())
            print(line)    
    
    command1 = subprocess.run(["/etc/init.d/hostname.sh"]) #resets to original hostname without reboot
    command2 = subprocess.run(["service", "networking", "force-reload"])
    command3 = subprocess.run(["service", "network-manager","force-reload"])
    print("\n")
    

def main():
    if bool("kali" in platform.release().lower()) == True:        
        print("\n")        
        option = input("Would you like to spoof a host? Y/N: ").lower()
        if option == "n":
            print("\n")            
            sys.exit()
        else:
            macChanger()
            hostChanger()
            macChangeBack()
            hostChangeBack()
            print("Everything back to normal. Exiting now...\n")
            sys.exit()
    else:
        print("Sorry, this script only runs on Kali Linux at the moment.")
        sys.exit()

if __name__ == "__main__":
    main()