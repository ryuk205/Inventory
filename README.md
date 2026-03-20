# Automate Catalog Processing

This project contains an automated script to parse WhatsApp chat exports, build a product catalog with modified prices (35% margin), and use OCR to extract product codes from associated images and videos.

## Features

- **Automated Chat Parsing**: Extracts product descriptions and automatically calculates a new price with a 35% margin.
- **OCR Code Extraction**: Uses EasyOCR to scan media files (images and the middle frame of videos) and extracts alphanumeric product codes automatically.
- **Smart Resumption**: The script reads the existing `Processed_Catalog.xlsx` and only processes *new* items, saving significant time on subsequent runs.
- **Auto-Detection**: Automatically finds the WhatsApp chat export (`.txt` file) in the `Data/` folder.

## Prerequisites

- Python 3.x installed on your system.

## Installation

1. Clone or download this project.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: The script uses `easyocr` with `gpu=False` to ensure compatibility across all systems, including CPU-only machines.*

## Setup

1. Place your exported WhatsApp chat text file (e.g., `WhatsApp Chat with ... .txt`) into the `Data/` directory.
2. Place all corresponding media files (e.g., `IMG-***.jpg`, `VID-***.mp4`) into the same `Data/` directory.

*Your directory structure should look like this:*
```text
Automate/
├── Data/
│   ├── WhatsApp Chat with...txt
│   ├── IMG-20260310-WA0002.jpg
│   └── VID-20260310-WA0003.mp4
├── process_catalog.py
└── requirements.txt
```

## Running the Script

To process your catalog, simply run the combined script:

```bash
python process_catalog.py
```

### What to Expect:
1. The script checks for an existing `Processed_Catalog.xlsx` to identify what has already been processed.
2. It processes only the **new** items found in the chat log that aren't in the catalog.
3. It performs OCR on the new media files to extract the product codes.
4. It outputs two updated catalog files:
   - `Processed_Catalog.csv`
   - `Processed_Catalog.xlsx`

You can run this script sequentially as many times as you want. Future runs will append new data dynamically without overwriting or reprocessing old data!
