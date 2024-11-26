import os, sys, argparse, yaml
from jinja2 import Environment, FileSystemLoader
'''
NAGIOS CORE MONITORING WIZARD
GENERATE NAGIOS CORE OBJECT CONFIGURATIONS FOR LINUX NCPA AGENT
CPU-Utilization
DISK-Utilization
MEMORY-Utilization
PROCESS-Count
USER-Count

'''

cname = "corewizard"
cversion = "0.0.3"
appPath = os.path.dirname(os.path.realpath(__file__))

#GENERATE COREWIZARD TEMPLATES
def generateNagiosTemplate(appPath,template):
    
    #TEMPLATE DATA
    tempdata = {}

    #COREWIZARD TEMPLATE YAML
    tyml = "{}/object_yml/{}.yml".format(appPath,template)
    
    #COREWIZARD JINJA TEMPLATE LOCATION
    #TODO SET APP PATH FOR TEMPLATES
    env = Environment(loader=FileSystemLoader(appPath+"/object_templates/"))
    
    #COREWIZARD NAGIOS FILE TEMPLATE TO PROCESS
    tempj2 = "{}.j2".format(template)
    temp = env.get_template(tempj2)
    
    #GET NAGIOS FILE CONTENT FROM CORE WIZARD TEMPLATE YAML 
    with open(tyml, 'r') as f:
        data_loaded = yaml.safe_load(f)
        tempdata = data_loaded[0]["template"]

    #RENDER TEMPLATE
    rendered = temp.render(tempdata)

    #NAGFILE
    nagfile = "{}.cfg".format(template)

    #CREATE THE NAGIOS COREWIZARD TEMPLATE
    with open(nagfile, mode="wt") as f:
        f.write(rendered)
        f.flush()
        f.close()  

#GENERATE COREWIZARD TEMPLATES
def generateNagiosCommands(appPath,template):
    
    #TEMPLATE DATA
    tempdata = {}
    commands = {}
    commands["cmd"] = {}

    #COREWIZARD TEMPLATE YAML
    tyml = "{}/object_yml/{}.yml".format(appPath,template)
    
    #COREWIZARD JINJA TEMPLATE LOCATION
    #TODO SET APP PATH FOR TEMPLATE
    env = Environment(loader=FileSystemLoader(appPath+"/object_templates/"))
    
    #COREWIZARD NAGIOS FILE TEMPLATE TO PROCESS
    #TODO CHANGE NAME TO *.J2 ONLY
    tempj2 = "{}.j2".format(template)
    temp = env.get_template(tempj2)
    
    #GET NAGIOS FILE CONTENT FROM CORE WIZARD TEMPLATE YAML 
    with open(tyml, 'r') as f:
        data_loaded = yaml.safe_load(f)
        tempdata = data_loaded[0]["commands"]        
        commands["cmd"] = tempdata

    #RENDER TEMPLATE
    rendered = temp.render(commands)
    #NAGFILE
    nagfile = "{}.cfg".format(template)

    #CREATE THE NAGIOS COREWIZARD TEMPLATE
    with open(nagfile, mode="wt") as f:
        f.write(rendered)
        f.flush()
        f.close()

#GENERATE NAGIOS OBJECT CONFIGS
def generateNagiosCfg(appPath,meta,nhd):
    
    #CORWIZARD OBJECTS TEMPLATE
    tyml = "{}/object_yml/corewizard-objects.yml".format(appPath)
    
    #COREWIZARD JINJA TEMPLATE LOCATION
    #TODO SET APP PATH FOR TEMPLATES
    env = Environment(loader=FileSystemLoader(appPath+"/object_templates/"))
    
    #COREWIZARD NAGIOS FILE TEMPLATE TO PROCESS
    tempj2 = "object_template.j2"
    temp = env.get_template(tempj2)
    
    #DICT STUFF FOR BUILDING UNIFIED CONFIG FILE
    cfg = {}
    cfg["services"] = {}
    cfg["host"] = {}
    
    #SET THE HOSTNAME
    cfg["host"]["host_name"] = nhd[0]
    
    #CHECK TO SEE IF WE GOT A SPLIT ADDRESS
    if len(nhd) > 1:
        cfg["host"]["address"] = nhd[1]
    else:
        cfg["host"]["address"] = nhd[0]

    #GET NAGIOS FILE CONTENT FROM CORE WIZARD TEMPLATE YAML 
    with open(tyml, 'r') as f:
        data_loaded = yaml.safe_load(f)

        #GET REQUIRED FIELDS FROM YML
        for item in data_loaded[0][meta.ostype.lower()]["host"]:
            cfg["host"][item] = data_loaded[0][meta.ostype.lower()]["host"][item]
        
        #GET ALL LINUX SERVICES DEFINED FOR THE TYPE IN THE YML
        for service in data_loaded[0][meta.ostype.lower()]["services"]:
            cfg["services"][service] = data_loaded[0][meta.ostype.lower()]["services"][service]
    
    #RENDER TEMPLATE
    rendered = temp.render(cfg)

    #NAGFILE
    nagfile = "{}.cfg".format(nhd[0])

    #CREATE THE NAGIOS COREWIZARD TEMPLATE
    with open(nagfile, mode="wt") as f:
        f.write(rendered)
        f.flush()
        f.close()

#MAIN
if __name__ == "__main__" :

    # 5 NEED INPUT
    args = argparse.ArgumentParser(prog=cname+" v:"+cversion, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    args.add_argument(
        "-a","--action",
        required=True,
        default="deploy",
        choices=["cmd", "template", "monitor"],
        help="String(wizard action): The action for the wizard to perform."
    ),
    #HOSTNAME:ADDRESS LIST
    args.add_argument(
        "-H","--hostlist",
        required=False,
        default=None,
        help="String(hostname:hostaddress,): Comma seperated list of hostname:hostaddesss combinations for which to create object cfgs." 
    ),
    #HOST OS TYPE
    args.add_argument(
        "-T","--ostype",
        required=False,
        default=None,
        choices=["linux","windows"],
        help="String(OSType): The target host operating system type."
    ),
    #OVERWRITE
    args.add_argument(
        "-o","--overwrite",
        required=False,
        action="store_true",
        help="boolean(True/False): If set, script wil overwrite any existing cfg files."
    )

    #GIVE 5 INPUT
    meta = args.parse_args()
    
    #TODO ADD NAGIOS WIZARD YAML
    #NAGIOS USER
    #NAGIOS GROUP
    #NAGIOS OBJECTS PATH
    #DEFAULT CONTACT/CONTACT GROUP

    #CREATE TEMPLATES
    if meta.action.lower() == "template":
        
        #TODO ADD COREWIZARD CONFIG YAML
        templates = {"corewizard-generic-service","corewizard-generic-host"}

        #GENERATE ALL NEEDED TEMPLATES
        for template in templates:

            # CLOBBER
            if meta.overwrite:
                print("OVERWRITING EXISTING {} TEMPLATE".format(template.upper()))
                generateNagiosTemplate(appPath,template)
            
            #GUARD
            else:
                #TODO NAGIOS OBJECT PATH FROM YML
                tpath = "{}/{}.cfg".format(appPath,template)
                
                #CHECK FILE EXISTS
                if os.path.exists(tpath):
                    print("Error: FILE {} ALREADY EXISTS, EXITING.".format(tpath))
                    sys.exit()
                
                #NEW FILE
                else:
                    print("GENERATING {} TEMPLATE".format(template.upper()))
                    generateNagiosTemplate(appPath,template)
    
    #CREATE TEMPLATES
    elif meta.action.lower() == "cmd":
        
        #TODO ADD COREWIZARD CONFIG YAML
        templates = {"corewizard_commands"}

        #GENERATE ALL NEEDED TEMPLATES
        for template in templates:

            # CLOBBER
            if meta.overwrite:
                print("OVERWRITING EXISTING {}".format(template.upper()))
                generateNagiosCommands(appPath,template)
            
            #GUARD
            else:
                
                #TODO NAGIOS OBJECT PATH FROM YML
                tpath = "{}/{}.cfg".format(appPath,template)
                
                #CHECK FILE EXISTS
                if os.path.exists(tpath):
                    print("Error: FILE {} ALREADY EXISTS, EXITING.".format(tpath))
                    sys.exit()
                #NEW FILE
                else:
                    print("GENERATING {} ".format(template.upper()))
                    generateNagiosCommands(appPath,template)

    
    #CREATE MONITORING OBJECT CONFIG FILES
    elif meta.action.lower() == "monitor":
        
        #LIST OF HOST OBJECTS
        hostlist = meta.hostlist.split(",")

        #LOOP THROUGH LIST OF HOSTS
        for i in hostlist:
            
            #CHECK TO SEE IF SPLIT ADDRESS
            nhd = i.split(":")
        
            # CLOBBER
            if meta.overwrite:
                print("OVERWRITING {}.cfg ".format(nhd[0]))
                generateNagiosCfg(appPath,meta,nhd)
            
            #GUARD
            else:
                
                #THIS WILL BE NAGIOS WORKING DIRECTORY
                cfgpath = "{}/{}.cfg".format(appPath,nhd[0])
                
                if os.path.exists(cfgpath):
                    print("SKIPPED: \"{}\" File Exists.".format(cfgpath))
                else:
                    print("GENERATING {}.cfg".format(nhd[0]))
                    generateNagiosCfg(appPath,meta,nhd)
    
    #UNKNOWN COMMAND
    else:
        print("THESE ARE NOT THE DROIDS YOU ARE LOOKING FOR!")
        sys.exit()
