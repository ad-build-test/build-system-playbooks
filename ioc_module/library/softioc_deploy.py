#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module. In order to run this once done, user needs to be logged into the appropiate k8s cluster

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess
import os
import shutil

"""
1) Checkout screeniocs                                    

> cvs co epics/iocCommon/All/dev        
2) If you have screeniocs already then do an update (warning: this deletes local changes and pulls in new ones)

> cvs -P -d update      
3) Update the screenioc, ensure no duplicates, add to top of file the comments of what you changed                                    
4) check in changes

> cvs ci -m "Made changes"    
5) Go to $IOC/facility. And pull in latest changes you made. Done. 

> cvs -qn update       
# This checks which files changed like (git status). "-q" means be somewhat quiet, -n means don’t change anything   
> cvs update <file>                               
# Optional: you can check where the screeniocs are by following symbolic link
> ls -l $IOC/screeniocs
6) Add the actual ioc pointers and startup command at $IOC_COMMON

> cd $IOC
# Make the directory for the sioc if it doesn't exist
> mkdir sioc-b34-mp01 && cd sioc-b34-mp01
# Add in the symbolic link to point to your development piece. If prod, Then make it point to the top level of the project where it sits in like $PHYSICS_TOP or $PYDM
# Make it point to the TOP of your directory
> ln -s /afs/slac.stanford.edu/u/cd/pnispero/mps/central_node_ioc/ iocSpecificRelease
# Add in the startup.cmd. You can copy from one of the templates at $IOC_COMMON/template
> cp ../template/startup.cmd.linuxRT ./startup.cmd
# Edit the startup.cmd to replace <ioc> with your actual ioc_name
7) Add the ioc_data stuff in $IOC_DATA 

> cd $IOC_DATA                               
# Make the directory if not already exists                               
> mkdir sioc-b034-mp01 && cd sioc-b34-mp01                               
# Create these required directories                               
> mkdir archive autosave autosave-req iocInfo restore yaml                        
# if adding yaml, you generally use that for fw, so for this example I copied all the contents in /yaml in previous sioc to new one  
8) Done, If still not working. Try starting it inside laci 

# enter cpu that has sioc                               
> ssh laci@cpu-b34-mp01                               
# Start the sioc, -t makes new terminal                               
> iocConsole.sh -t sioc-b34-mp01                               
# look at error messages if any                               
# Check your code if the epicsEnvSet("IOC", "") is set correctly  
"""
DEPLOYMENT_TMP_FOLDER = "deployment_tmp/" # This is where any files created/checkouted out will exist

def run_ioc():
    # 1) use iocConsole <sioc> / siocRestart <sioc>
    # 2) If neither works, you can enter cpu that has the sioc running, then iocConsole.sh -t <sioc>
    pass
def update_ioc_data():
    # 1) In $IOC_DATA, make directory for ioc if doesn't already exist
    # 2) in the ioc folder, create these directories: archive, autosave, autosave-req, iocInfo, restore, yaml
    pass
def update_ioc_startup():
    # 1) In $IOC, make directory for ioc if doesn't already exist
    # 2) in the ioc folder, add in symbolic link to point to the TOP of your repo (for dev)
    # 3) two options for startup.cmd
        # 3.1) Add in the startup.cmd, use one of the templates at $IOC_COMMON/template
        #      Edit the startup.cmd to replace <ioc> with actual ioc_name
        # 3.2) Add startup.cmd in the component src tree, and make symlink to it from $IOC
    
    pass
def update_screeniocs(ioc_type: str, ioc_name: str, host_user: str, executable_path: str, server_user_node_port: str) -> str:
    Update - we don't want to automate this piece as part of ansible, instead
    screeniocs can be a component, with scripts that An already made to parse and possibly
    update screeniocs.
    may not need this custom ansible, except for the run_ioc part, although could use bash command for that?
    # 1) Checkout screeniocs through cvs
    try:
        cvs_bytes = subprocess.check_output(['cvs', 'co', 'epics/iocCommon/All/dev/screeniocs'])
        cvs_output = cvs_bytes.decode("utf-8")
    except Exception as e:
        print("== SOFTIOC_DEPLOY == **ERROR** - in update_screeniocs(): " + str(e))
    # 2) Update appropriate IOC
    shutil.copy('epics/iocCommon/All/dev/screeniocs', 'ADBS_screeniocs')
        # you are here - just make a copy of the screeniocs and edit that one for prototype purposes
    # 3) Check if entry already exists, actually prompt user in cli for screeniocs info
        # specifically 
        #IOC Type (SIOC, HIOC, VIOC)
#       IOC Name/Alias
#       host user account used to run screen and host where screen is run
#       Executable absolute path
#       For HIOCs, host user account used to run screen, terminal server, and terminal server port number
#                        For SIOCs and VIOCs, full executable path (optional)

    return cvs_output

def deploy_ioc(module_params: dict):
    output = {}
    # NOTE - cant use live output in ansible modules, so just alter output dict
    # But prints will print out if script crashes
    cvs_output = update_screeniocs(module_params["ioc_type"], module_params["ioc_name"], module_params["host_user"],
                                   module_params["executable_path"], module_params["server_user_node_port"])
    update_ioc_startup()
    update_ioc_data()
    run_ioc()
    output["cvs_output"] = cvs_output

    return output

def ansible_run_module():
    """
    This is the default ansible module boilerplate code + some custom args
    In order to run it through a playbook
    """
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        deploy_type=dict(type='str', required=True),
        ioc_type=dict(type='str', required=True),
        ioc_name=dict(type='str', required=True),
        host_user=dict(type='str', required=True),
        executable_path=dict(type='str', required=True),
        server_user_node_port=dict(type='str', required=False),
        output_path=dict(type='str', required=True),
        dev=dict(type='bool', required=False, default=False),
        prod=dict(type='bool', required=False, default=False),
        new=dict(type='bool', required=False, default=False)
    )
    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict( 
        changed=False,
        custom_output=dict
    )
    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    os.chdir(module.params['output_path'])
    result['custom_output'] = deploy_ioc(module.params)
    
    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)
    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True
    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['ioc_name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)
    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    ansible_run_module()


if __name__ == '__main__':
    main()