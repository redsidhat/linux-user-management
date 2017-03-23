# Linux System User Managment Console


This is a simple usermanagement webapp creates using python flask. There is no css or js involved. purely python, jinja2 and html.
The core functionalities of this tool is
  - Add a linux user
  - Modify a linux user
  - Delete a linux user

## Prerequisites

Prerequisites to run this app is ass follows. 
- Root access.
    This app require root privilage and should be run as root.
- python 2.7
- python flask module
- python jinja2 module
- port 80 should be free

## Setup
Clone the app run
```sh
python app.py
```
## Working
Access the ip address of the server where the app is running through browser.

## Problems/Improvements
- No authentication to access this makes it critical. Better to bind it to localhost instead of public interface.
- No navigation to pages.
- No validation for strong passwords.
- No validation for home directories.
- No logging. The logs are directly printed to terminal
- No native backround running support
- Web interface looks horrible and shows my embarrassing html/css skills.