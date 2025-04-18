# Firmware Filter Tool

This directory contains a tool for filtering and downloading firmware from the Firmware-Dataset based on application domain (like WiFi), industry, and vendor.

## Overview

`firmware_filter.py` is a comprehensive tool that allows you to:

- Filter firmware by application domain (WiFi, IoT, cameras, etc.)
- Filter by industry vertical (healthcare, industrial, smart home, etc.)
- Filter by vendor (TP-Link, Netgear, D-Link, etc.)
- Add custom keywords for more specific filtering
- Download and optionally unpack the filtered firmware

## Usage Examples

### Test CSV File Access

```bash
# Test if the CSV file can be accessed
python firmware_filter.py --test-csv

# Test with a specific CSV file
python firmware_filter.py --test-csv --csv /path/to/your/firmware_list.csv
```

### List Available Domains and Industries

```bash
# List available application domains
python firmware_filter.py --list-domains

# List available industries
python firmware_filter.py --list-industries
```

### Download WiFi Firmware

```bash
# List WiFi firmware from TP-Link (without downloading)
python firmware_filter.py --domain wifi --vendor tp-link --list-only

# Download up to 5 WiFi firmware files from TP-Link
python firmware_filter.py --domain wifi --vendor tp-link --limit 5

# Download and unpack WiFi firmware
python firmware_filter.py --domain wifi --vendor tp-link --limit 5 --unpack
```

### Filter by Industry

```bash
# List smart home firmware (without downloading)
python firmware_filter.py --industry smart_home --list-only

# Download industrial firmware from Siemens
python firmware_filter.py --industry industrial --vendor siemens
```

### Combine Filters

```bash
# Find WiFi devices for healthcare industry
python firmware_filter.py --domain wifi --industry healthcare --list-only

# Download enterprise WiFi devices from Cisco
python firmware_filter.py --domain wifi --industry enterprise --vendor cisco
```

### Use Custom Keywords

```bash
# Filter using custom keywords
python firmware_filter.py --keyword "mesh" --keyword "wifi6" --list-only
```



## Output Directory

By default, firmware files are downloaded to the `../fws` directory. You can change this with the `--output` parameter.

## CSV Source

The script uses two CSV files as data sources:
- `../dat/firmware_download_list.csv` - Main firmware download links (HTTP/HTTPS)
- `../dat/firmware_ftp_list.csv` - FTP server links for firmware

You can specify different CSV files with the `--csv` and `--ftp-csv` parameters.

## Requirements

- Python 3.6+
- Required packages: requests (tqdm is optional for progress bars)
- The script depends on the existing `fw_downloader.py` and `fw_unpacker.py` modules from the Firmware-Dataset project

## Available Filters

### Application Domains

The tool supports filtering by these application domains:
- wifi - WiFi routers, access points, and wireless devices
- iot - Internet of Things devices
- camera - IP cameras, surveillance systems
- storage - NAS devices, storage systems
- printer - Printers, scanners, MFPs
- voip - VoIP phones and systems
- modem - DSL, cable, and fiber modems

### Industries

The tool supports filtering by these industry verticals:
- healthcare - Medical devices and healthcare systems
- industrial - Industrial automation and control systems
- automotive - Vehicle and automotive systems
- smart_home - Home automation and smart home devices
- networking - Enterprise networking equipment
- enterprise - Business and corporate systems
- education - Educational technology
- retail - Point of sale and retail systems
- telecom - Telecommunications infrastructure
