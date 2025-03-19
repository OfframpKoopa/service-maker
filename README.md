# Service Maker 

Service Maker is a lightweight program that acts as a CLI to create and
update services for Linux (systemd).

This aims at facilitating the handling of services through a terminal or
a script.

It also writes into the file the entirety of the parameters for each section,
so the user don't have to guess or go to the documentation for a specific
functionnality

## A Simple Example

```bash
service-maker create --Name "Test" --ExecStart "echo HelloWorld"
```

## Installation 

I recommend you use pipx to install the software "globally".

If you have poetry (recommended), you can run the ./install.sh script.

