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


## CoreWizard.py

### Input

<table>
<tr>
<td width="25%"">
-a/--action
</td>
<td width="50%">
Choice:[cmd,template,monitor] cmd=Deploy the corewizard-command.cfg,template=Deploy the corewizard-template.cfg,monitor=Create monitoring object.cfg
</td>
<td width="25%">
Required
</td>
</tr>
<tr>
<td width="25%"">
-H/--hostlist
</td>
<td width="50%">
Double quote encapsulated, comma seperated list of hostname or hostname:address pairs:["hostname1,hostname2:192.168.0.0,hostname3"]
</td>
<td width="25%">
Required
</td>
</tr>
<tr>
<td width="25%"">
-T/--ostype
</td>
<td width="50%">
Choice:[linux,windows] linux=use linux definitions from the object yml, windows=use the windows definitons from the objects yml
</td>
<td width="25%">
Required
</td>
</tr>
<tr>
<td width="25%"">
-o/--overwrite
</td>
<td width="50%">
Boolean:[-o] If included the wizard will overwrite configuration files in the app path of the script. Thise is needed to deploy updates to cmds,templates,objects.
</td>
<td width="25%">
Optional
</td>
</tr>
</table>

### Generate CoreWizard Commands
The "cmd" action, short for generate corewizard commands, takes the object feild values defined in the yml, passes this to the jinja2 template and creates the Nagios Core commands that will be used by the corewizard host and services templates.

* YML
  * corewizard-commands.yml 
* Template:
  * corewizard-commands.j2 
* File Generated
  * corewizard_commands.cfg
#### Command File Content
<table>
  <th>Name</th><th>Description</th>
  <tr>
    <td width="30%">
      check_ncpa
    </td>
    <td width="70%">
      Command definition as taken from NagiosXI for forward compatability.
  </tr>
    <tr>
    <td width="30%">
      check_ncpa_hyperv
    </td>
    <td width="70%">
      Command definition as taken from NagiosXI for forward compatability.
  </tr>
    <tr>
    <td width="30%">
      check_ncpa_core
    </td>
    <td width="70%">
      Modified default command definition that uses Nagios macros to store the token and port used to communicate with NCPA.
  </tr>
</table>

### CoreWizard Templates
The "template" action, short for generate corewizard templates, takes the object feild values defined in the yml, passes this to the jinja2 template and creates the Nagios Core tewmplates that will be used by the hosts and services monitored.
The corewizard templates contain the majority of the settings for the monitored objects generated via the corewizard and are inherited via the use feild in the monitored object cfg.

* Tempate
  * corewizard-generic-host.j2
  * corewizard-generic-service.j2
* YML
  * corewizard-generic-host.yml
  * corewizard-generic-service.yml
* Config Files Created
  * corewizard-generic-host.cfg
  * corewizard-generic-service.cfg

#### CoreWizard Template Content

corewizard-generic-host.cfg
<table>
  <th>Field</th><th>Value</th>
  <tr>
    <td>name</td><td>value</td>
  </tr>
</table>

corewizard-generic-service.cfg
<table>
  <th>Field</th><th>Value</th>
  <tr>
    <td>name</td><td>value</td>
  </tr>
</table>

### Corewizard Objects
The "monitor" action, takes the input provices by the user in the hostlist and based on the type, reads the object feild values defined in the yml, passes this to the jinja2 template and creates the Nagios Core object (<hostname>.cfg) containing the host and services defined in the object yml.

#### CoreWizard Object Content
HOST
<table>
  <th>Field</th><th>Value</th>
  <tr>
    <td>name</td><td>value</td>
  </tr>
</table>

(n)SERVICE
<table>
  <th>Field</th><th>Value</th>
  <tr>
    <td>name</td><td>value</td>
  </tr>
</table>
