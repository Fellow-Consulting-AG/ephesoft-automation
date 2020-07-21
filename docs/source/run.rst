==============
How to run
==============
 
EphesoftAutomated is available as a Docker instance. 
 
Docker is a platform for running containers with prepackaged applications. It’s a system that we are going to use for packaging and deploying different versions and microservices.
 
Install Docker on Windows
-------------------------

`Install Docker Desktop on Windows`_.

.. _Install Docker Desktop on Windows: https://hub.docker.com/editions/community/docker-ce-desktop-windows/

**System Requirements:**

- Windows 10 64-bit: Pro, Enterprise, or Education (Build 16299 or later).
- Hyper-V and Containers Windows features must be enabled.
- The following hardware prerequisites are required to successfully run Client Hyper-V on Windows 10:

    - 64 bit processor with Second Level Address Translation (SLAT)
    - 4GB system RAM
    - BIOS-level hardware virtualization support must be enabled in the BIOS settings. For more information, see Virtualization.

**Installation:**

1. Double-click Docker Desktop Installer.exe to run the installer.

2. When prompted, ensure the Enable Hyper-V Windows Features option is selected on the Configuration page.

3. Follow the instructions on the installation wizard to authorize the installer and proceed with the install.

4. When the installation is successful, click Close to complete the process.

**Start Docker Desktop:**

Docker Desktop does not start automatically after installation. To start Docker Desktop, search for Docker.

.. image:: image/docker-search.png

When the whale icon in the status bar stays steady, Docker Desktop is up-and-running.

.. image:: image/whale-icon.png

Congrats! You are now successfully running Docker Desktop on Windows!

.. image:: image/docker-tutorial.png



How to compare results using EphesoftAutomated Docker instance
--------------------------------------------------------------------
 
.. code-block:: bash

 docker run -v /local_path_to_conf_dir:/ephesoft-automation/conf ephesoftautomation compare -b /ephesoft-automation/conf -c config.yml

 code . . .

- with **docker run** you can run your image as a container 
- **-v** we are mounting our local directory to docker container, so it can use files from this directory
- with **compare** we are adding the configuration files that are missing inside the Docker ecosystem
