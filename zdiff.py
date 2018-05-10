import os
import time

print "This script allows you to compare a list of current configs with past date configs."
input = raw_input("Enter the input filename (devices hostnames in file must be FQDN with or without the .gz file extension: ")
date = raw_input("Enter the past date to compare with current, for example, 2018/04/24: ")
diffreport = raw_input("Enter the name of the diffreport: ")
single = raw_input("Enter an \"s\" if you want a single consolidated report only, if not just hit enter: ")

with open(input) as p:
    for devices in p:
        os.system('zdiff -u /home/configs/archive/*-01/' + date + '/' + devices.rstrip(".gz\n") + str(".gz") + ' /home/configs/archive/*-01/current/' + devices.rstrip(".gz\n") + str(".gz") + str(" >> tmp_") + devices.rstrip(".gz\n"))
        print "Compared configs for " + devices.rstrip(".gz\n")
results = os.system('ls -la | grep tmp_ | grep -v " 0 " | awk {\'print $9\'} >> ' + str(diffreport))
time.sleep(.5)
with open(diffreport) as r:
    for line in r:
        os.system('cat ' + line.rstrip("\n") + str(" >> ") + line.replace('tmp_', 'diff_'))
print "\nThere was a diff in the following devices: "
os.system('ls -la | grep diff_ | awk {\'print $9\'}')
os.system('more -1000000 diff_* >> ' + str(diffreport))
time.sleep(.5)
os.system('rm tmp_*')
if single  == 's':
    os.system('rm diff_*')
    print ("\nAll changes can be viewed in " + str(diffreport))
else:
    print ("\nAll changes can be viewed in " + str(diffreport) + " or individually by files named diff_<device name> ")
