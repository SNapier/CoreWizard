# CoreWizard
Python to create the commands, templates and Nagios Core object config files needed to stand-up lowest common denominator (LCD) monitoring for hosts and services via Nagios Cross Platform Agent (NCPA).  

## Usage

### Nagios:
1. Requires NagiosCore in proper functioning condition.
2. Requires Install of Nagios Enterprises check_ncpa.py monitoring plugin.
   * Creating Nagios macros to hold the token for the check_ncpa commands is not required but, strongly recommended.
4. Monitoring targets require proper functioning install of NCPA. 

### CoreWizard:
1. Download the CoreWizard as a zip archive to the Nagios server.
2. Extract the content of the zip file to the "/usr/local/nagios/etc/objects/" directory.
3. Install required Python3 libraries
   * os
   * sys
   * argparse
   * yaml
   * jinja2
   
4. Execute "python3 corewizard -a cmd" to reate corewizard commands.
5. Execute "python3 corewizard.py -a templates"
6. Execute "python3 corewizard.py -a monitor -H "<host_name>:<ip/fqdn> -T <linux/windows>"
7. In the case of an error or needing to overwrite any config files you may have already created you have to use the "-o" command flag.
   * DANGER: This will overwrite any object file that is already present in the Nagios Core working directory.
