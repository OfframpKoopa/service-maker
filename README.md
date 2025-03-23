# Service Maker 

## Description

Service Maker is a lightweight program that acts as a CLI to create and
update services for Linux (systemd).

This aims at facilitating the handling of services through a terminal or
a script (developper tool is currently under development).

It also writes into the file all of the parameters for each section,
so the user don't have to guess or go to the documentation for a specific
functionnality

## Concept

The idea is to basically use the service-maker commands followed by 
the name and values of the directives we want in our service config
file.

for example, the ExecStart directive will be filled if :

- --ExecStart "value here"

is passed.

## Action and meta arguments

Actions are the command that triggers the logical operation that 
the user wants to perform.

There are 2 actions : 

- create
- update 

Meta arguments are arguments or flags that are needed by the service-maker
to function or offer advanced features.

- --name meta argument is MANDATORY for every actions.

Service directive arguments use the same casing  in the CLI they appear in the
configuration file.

Wheras meta arguments are simple lowercase arguments.


NOTE: The casing will be ignored in future versions, as it is one of the 
    thing that makes writing systemd configuration files a pain.

## A Simple Example

### Command
```bash
service-maker create --name "Test" --ExecStart "echo HelloWorld"
```

### Output in /etc/systemd/system/Test.service

```service file
[Unit]
# Description=
# Documentation=
# Requires=
# Wants=
# BindsTo=
# Before=
# After=
# Conflicts=
# ConditionArchitecture=
# ConditionVirtualization=
# ConditionKernelCommandLine=
# ConditionSecurity=
# AssertArchitecture=
# AssertVirtualization=
# AssertKernelCommandLine=
# AssertSecurity=
# OnFailure=
# OnSuccess=
# IgnoreOnIsolate=
# JobTimeoutSec=
# JobTimeoutAction=
# StartLimitIntervalSec=
# StartLimitBurst=
# StartLimitAction=
# RefuseManualStart=
# RefuseManualStop=
[Service]
# Type=
ExecStart=echo HelloWorld
# ExecStartPre=
# ExecStartPost=
# ExecReload=
# ExecStop=
# ExecStopPost=
# RestartSec=
# Restart=
# TimeoutStartSec=
# TimeoutStopSec=
# TimeoutSec=
# WatchdogSec=
# RemainAfterExit=
# PIDFile=
# User=
# Group=
# WorkingDirectory=
# RootDirectory=
# RuntimeDirectory=
# RuntimeDirectoryMode=
# Environment=
# EnvironmentFile=
# StandardOutput=
# StandardError=
# SyslogIdentifier=
# SyslogFacility=
# SyslogLevel=
# LimitCPU=
# LimitFSIZE=
# LimitDATA=
# LimitSTACK=
# LimitCORE=
# LimitRSS=
# LimitNOFILE=
# LimitAS=
# LimitNPROC=
# LimitMEMLOCK=
# LimitLOCKS=
# LimitSIGPENDING=
# LimitMSGQUEUE=
# LimitNICE=
# LimitRTPRIO=
# OOMScoreAdjust=
# IOSchedulingClass=
# IOSchedulingPriority=
# CPUSchedulingPolicy=
# CPUSchedulingPriority=
# CPUAffinity=
# ProtectSystem=
# ProtectHome=
# NoNewPrivileges=
# ReadOnlyPaths=
# ReadWritePaths=
# InaccessiblePaths=
# CapabilityBoundingSet=
[Install]
# WantedBy=
# RequiredBy=
# Also=
# Alias=
```


## Installation 

The command is installed "globally" for the user with pipx.
Poetry is required for handling dependencies.

If poetry is installed, ./install.sh script should be good enough.


The "module" version of this software is not yet available.
I am currently working on a ServiceMaker object that will encapsulate the features
to allow easy integration in a script.
