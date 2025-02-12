# build-system-playbooks
Repo with the ansible playbooks used for the build system (Software factory)

## ioc_module
Playbooks for deploying ioc apps

## build_system_deployment
Playbooks for deploying the build system itself
1. Only possible to use if admin of build system (need access to git repos and the clusters)
2. Also may need to call the playbook more than once if didn't work the first time, there is a bug haven't fix on core-build-system mongodb deployment