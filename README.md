# Service Maker 

Service Maker is a lightweight program that acts as a CLI to create and
update services for Linux (systemd).

This aims at facilitating the handling of services through a terminal or
a script.

It also writes into the file the entirety of the parameters for each section,
so the user don't have to guess or go to the documentation for a specific
functionnality

## A Simple Example

### Command
```bash
service-maker create --Name "Test" --ExecStart "echo HelloWorld"
```

### Output in /etc/systemd/system/Test

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

I recommend you use pipx to install the software "globally".

If you have poetry (recommended), you can run the ./install.sh script.

