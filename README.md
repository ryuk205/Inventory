# Automate Catalog Processing

This project contains automated scripts to parse WhatsApp chat export archives, build a structured product catalog with automatically calculated modified prices (35% margin), and use EasyOCR to extract alphanumeric product codes from associated images and videos.

## Features

- **Automated ZIP Extraction**: You simply provide the exported `.zip` file from WhatsApp. The script will automatically extract the logs and media to prepare for processing.
- **Automated Chat Parsing**: Extracts original product descriptions and dynamically recalculates a new selling price with a 35% margin, rounded smartly.
- **OCR Code Extraction**: Uses EasyOCR to scan images and mid-frames of videos, aggressively filtering out common text to isolate real product codes.
- **Smart Resumption & Deduplication**: The script reads your existing `Processed_Catalog.xlsx` to skip historically processed items, and additionally tracks chat log anomalies to guarantee a 100% duplicate-free output table.
- **Cloud Ready**: A Jupyter Notebook (`process_catalog_colab.ipynb`) is included for seamless zero-setup execution entirely inside Google Colab (using your Google Drive).

## Project Structure

- `process_catalog.py`: The single execution script for running locally on a PC.
- `process_catalog_colab.ipynb`: The notebook equivalent meant exclusively for Google Colab execution.
- `Whatsapp_chats_export/`: Directory where you should place your WhatsApp `.zip` file.
- `Data/`: A temporary workspace where the archive is automatically extracted.
- `Processed_Catalog.csv` & `Processed_Catalog.xlsx`: The generated output data sheets.

## Quick Setup

Detailed operational manuals are provided in `instructions.md` or `instructions.txt`. At a glance:
1. Place your WhatsApp Export `.zip` file into the `Whatsapp_chats_export/` folder.
2. Run the script! It handles extraction, scanning, calculating, and exporting perfectly autonomously.

*(Note: Install local dependencies via `pip install -r requirements.txt` before running locally).*
