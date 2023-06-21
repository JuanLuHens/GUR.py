# Get Unique Ranges (GUR.py)

## Overview
The "Get Unique Ranges" (GUR.py) application is a tool designed to retrieve the unique ranges of networks where workstations and servers of a domain are located. It helps in the analysis and management of network infrastructure by collecting network information based on user input.

## Prerequisites
Before using the application, ensure that the following prerequisites are met:

- Python 3.x is installed on your system.
- Required Python packages are installed. You can install the required packages by running the following command:
        ```
        pip install -r requirements.txt
        ```

## Usage

Open a terminal or command prompt.
```
git clone https://github.com/JuanLuHens/GUR.py.git
cd GUR.py
python GUR.py -h /--help
```

## Examples
Here are some examples of how to use the application:
```
python GUR.py -u domainuser -p pwduser -d contoso.com -dc 10.10.1.1 -ns 10.10.1.1
```
### Output
```
Rangos unicos:
10.1.15.0/24
10.1.89.0/24
10.10.15.0/24
10.10.89.0/24
Esta informacion queda almacenada en el fichero rangosunicos.txt
```
## Notes
- This application is designed for informational and analysis purposes only. Ensure that you have proper authorization and adhere to legal and ethical guidelines when using this tool.
- The application may require administrative privileges or appropriate access rights to retrieve the network information.

## License
This project is licensed under the [MIT License](LICENSE).

