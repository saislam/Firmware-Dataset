#!/usr/bin/env python3
"""
Firmware Filter

A comprehensive tool to filter and download firmware from the Firmware-Dataset
based on application domain, industry, and vendor.
"""

import os
import csv
import argparse
import requests

# Try to import tqdm, but make it optional
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    print("Warning: tqdm module not found. Progress bars will not be displayed.")
    print("You can install it with: pip install tqdm")

from fw_downloader import download_firmware
from fw_unpacker import unpack_firmware

# Application domain keywords
DOMAIN_KEYWORDS = {
    'wifi': [
        'router', 'access point', 'ap', 'wireless', 'wifi', 'wi-fi',
        'wlan', 'wr', 'wap', '802.11', 'wrt', 'wnr', 'wgr', 'wdr',
        'archer', 'linksys', 'netgear', 'asus', 'tp-link', 'd-link'
    ],
    'iot': [
        'iot', 'internet of things', 'smart device', 'connected device',
        'sensor', 'actuator', 'smart home', 'smart building'
    ],
    'camera': [
        'camera', 'ip camera', 'webcam', 'surveillance', 'cctv',
        'security camera', 'dvr', 'nvr', 'video recorder'
    ],
    'storage': [
        'storage', 'nas', 'network attached storage', 'san', 'raid',
        'disk', 'drive', 'backup'
    ],
    'printer': [
        'printer', 'scanner', 'mfp', 'multifunction', 'copier',
        'fax', 'all-in-one'
    ],
    'voip': [
        'voip', 'voice', 'ip phone', 'sip', 'telephony', 'pbx',
        'call', 'conference'
    ],
    'modem': [
        'modem', 'dsl', 'adsl', 'vdsl', 'cable modem', 'docsis',
        'fiber', 'gpon', 'ont'
    ]
}

# Industry-specific keywords
INDUSTRY_KEYWORDS = {
    'healthcare': ['medical', 'health', 'hospital', 'patient', 'clinic', 'diagnostic'],
    'industrial': ['industrial', 'factory', 'manufacturing', 'automation', 'plc', 'scada', 'iot'],
    'automotive': ['car', 'vehicle', 'automotive', 'telematics', 'obd'],
    'smart_home': ['smart home', 'home automation', 'thermostat', 'doorbell', 'camera', 'security'],
    'networking': ['router', 'switch', 'gateway', 'firewall', 'vpn', 'network'],
    'enterprise': ['enterprise', 'business', 'corporate', 'office'],
    'education': ['education', 'school', 'university', 'campus'],
    'retail': ['pos', 'point of sale', 'retail', 'kiosk', 'payment'],
    'telecom': ['telecom', 'telecommunication', 'cellular', 'mobile', 'base station']
}

def load_firmware_list(csv_file):
    """Load firmware list from CSV file"""
    firmware_list = []

    # Check if the CSV file exists
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found at '{csv_file}'")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Checking if parent directory exists: {os.path.exists(os.path.dirname(csv_file))}")
        return []

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                firmware_list.append(row)
        print(f"Loaded {len(firmware_list)} firmware entries from {csv_file}")
        return firmware_list
    except Exception as e:
        print(f"Error loading firmware list: {e}")
        return []

def load_ftp_list(csv_file):
    """Load FTP server list from CSV file"""
    ftp_list = []

    # Check if the CSV file exists
    if not os.path.exists(csv_file):
        print(f"Error: FTP CSV file not found at '{csv_file}'")
        return []

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ftp_list.append(row)
        print(f"Loaded {len(ftp_list)} FTP server entries from {csv_file}")
        return ftp_list
    except Exception as e:
        print(f"Error loading FTP list: {e}")
        return []

def filter_firmware(firmware_list, domain=None, industry=None, vendor=None, custom_keywords=None):
    """
    Filter firmware list based on domain, industry, vendor, and custom keywords

    Args:
        firmware_list: List of firmware dictionaries
        domain: Application domain (e.g., 'wifi', 'iot')
        industry: Industry vertical (e.g., 'healthcare', 'industrial')
        vendor: Specific vendor name
        custom_keywords: List of additional keywords to filter by

    Returns:
        List of filtered firmware dictionaries
    """
    # Prepare keywords for filtering
    keywords = []

    # Add domain-specific keywords
    if domain and domain in DOMAIN_KEYWORDS:
        keywords.extend(DOMAIN_KEYWORDS[domain])

    # Add industry-specific keywords
    if industry and industry in INDUSTRY_KEYWORDS:
        keywords.extend(INDUSTRY_KEYWORDS[industry])

    # Add custom keywords
    if custom_keywords:
        keywords.extend(custom_keywords)

    # If no keywords provided, return empty list
    if not keywords and not vendor:
        print("No filtering criteria provided")
        return []

    filtered_list = []

    for firmware in firmware_list:
        # Skip if vendor filter is provided and doesn't match
        if vendor and firmware['vendor'].lower() != vendor.lower():
            continue

        # If no keywords (only vendor filter), add to list
        if not keywords:
            filtered_list.append(firmware)
            continue

        # Check if product name contains any keyword
        product = firmware.get('product', '').lower()
        if any(keyword.lower() in product for keyword in keywords):
            filtered_list.append(firmware)
            continue

        # Also check URL for keywords
        url = firmware.get('url', '').lower()
        if any(keyword.lower() in url for keyword in keywords):
            filtered_list.append(firmware)

    return filtered_list

def download_filtered_firmware(firmware_list, save_path, limit=None):
    """Download firmware from filtered list"""
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Limit the number of downloads if specified
    if limit and limit > 0:
        firmware_list = firmware_list[:limit]

    urls = [item['url'] for item in firmware_list]

    print(f"Downloading {len(urls)} firmware files to {save_path}...")
    download_firmware(urls, save_path)

    return len(urls)

def main():
    parser = argparse.ArgumentParser(description='Filter and download firmware from the Firmware-Dataset')
    parser.add_argument('--domain', help='Application domain (e.g., wifi, iot, camera)')
    parser.add_argument('--industry', help='Industry vertical (e.g., healthcare, industrial)')
    parser.add_argument('--vendor', help='Filter by vendor name (e.g., tp-link, netgear)')
    parser.add_argument('--keyword', action='append', help='Additional keywords to filter by')
    parser.add_argument('--list-domains', action='store_true', help='List available application domains')
    parser.add_argument('--list-industries', action='store_true', help='List available industries')
    parser.add_argument('--list-only', action='store_true', help='Only list matching firmware, don\'t download')
    parser.add_argument('--limit', type=int, default=0, help='Limit the number of firmware to download')
    parser.add_argument('--unpack', action='store_true', help='Unpack downloaded firmware')
    parser.add_argument('--output', default='../fws', help='Output directory for downloaded firmware')
    parser.add_argument('--csv', default='../dat/firmware_download_list.csv', help='Path to firmware download list CSV')
    parser.add_argument('--ftp-csv', default='../dat/firmware_ftp_list.csv', help='Path to firmware FTP list CSV')
    parser.add_argument('--test-csv', action='store_true', help='Test if the CSV files can be accessed')

    args = parser.parse_args()

    # Test CSV file access if requested
    if args.test_csv:
        csv_files = [
            ("Main firmware download list", args.csv),
            ("FTP firmware list", args.ftp_csv)
        ]

        all_success = True

        for desc, csv_path in csv_files:
            print(f"\nTesting access to {desc}: {csv_path}")
            if os.path.exists(csv_path):
                print(f"SUCCESS: CSV file exists at {csv_path}")
                # Try to read the first few lines
                try:
                    with open(csv_path, 'r', encoding='utf-8') as f:
                        header = f.readline().strip()
                        first_line = f.readline().strip() if f.readline() else ""
                    print(f"CSV header: {header}")
                    print(f"First data line: {first_line}")
                    print(f"CSV file can be read successfully.")
                except Exception as e:
                    print(f"ERROR: CSV file exists but cannot be read: {e}")
                    all_success = False
            else:
                print(f"ERROR: CSV file not found at {csv_path}")
                print(f"Current working directory: {os.getcwd()}")
                # Check if the dat directory exists
                dat_dir = os.path.dirname(csv_path)
                if os.path.exists(dat_dir):
                    print(f"The directory {dat_dir} exists. Contents:")
                    for item in os.listdir(dat_dir):
                        print(f"  - {item}")
                else:
                    print(f"The directory {dat_dir} does not exist.")
                all_success = False

        if all_success:
            print("\nSUCCESS: All CSV files can be accessed and read.")
        else:
            print("\nWARNING: Some CSV files could not be accessed or read.")
        return

    # Show available domains if requested
    if args.list_domains:
        print("Available application domains:")
        for domain in DOMAIN_KEYWORDS:
            print(f"- {domain}: {', '.join(DOMAIN_KEYWORDS[domain][:3])}...")
        return

    # Show available industries if requested
    if args.list_industries:
        print("Available industries:")
        for industry in INDUSTRY_KEYWORDS:
            print(f"- {industry}: {', '.join(INDUSTRY_KEYWORDS[industry][:3])}...")
        return

    # Load firmware and FTP lists
    firmware_list = load_firmware_list(args.csv)
    ftp_list = load_ftp_list(args.ftp_csv)

    if not firmware_list and not ftp_list:
        print("Error: Could not load any firmware data.")
        return

    print(f"Total firmware entries available: {len(firmware_list) + len(ftp_list)}")

    # Filter firmware
    filtered_list = filter_firmware(
        firmware_list,
        domain=args.domain,
        industry=args.industry,
        vendor=args.vendor,
        custom_keywords=args.keyword
    )

    # Build filter description for output
    filter_desc = []
    if args.domain:
        filter_desc.append(f"domain '{args.domain}'")
    if args.industry:
        filter_desc.append(f"industry '{args.industry}'")
    if args.vendor:
        filter_desc.append(f"vendor '{args.vendor}'")
    if args.keyword:
        filter_desc.append(f"custom keywords {args.keyword}")

    filter_str = " and ".join(filter_desc) if filter_desc else "no filters"

    print(f"Found {len(filtered_list)} firmware entries matching {filter_str}")

    # Display the filtered list
    if filtered_list:
        print("\nFiltered Firmware List:")
        for i, firmware in enumerate(filtered_list[:20], 1):  # Show first 20 for brevity
            print(f"{i}. Vendor: {firmware['vendor']}, Product: {firmware['product']}, URL: {firmware['url']}")

        if len(filtered_list) > 20:
            print(f"... and {len(filtered_list) - 20} more")

    # Download if not list-only
    if not args.list_only and filtered_list:
        count = download_filtered_firmware(filtered_list, args.output, args.limit)
        print(f"Downloaded {count} firmware files")

        # Unpack if requested
        if args.unpack:
            print("Unpacking downloaded firmware...")
            unpack_firmware(args.output)

if __name__ == '__main__':
    main()
