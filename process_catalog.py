import os
import re
import math
import glob
import pandas as pd
import easyocr
import cv2

DATA_DIR = 'Data'
CSV_PATH = 'Processed_Catalog.csv'
EXCEL_PATH = 'Processed_Catalog.xlsx'

print("Initializing EasyOCR (CPU)...")
# Set PYTHONUTF8 to handle model download progress bars on Windows
os.environ['PYTHONUTF8'] = '1'
reader = easyocr.Reader(['en'], gpu=False)

def extract_text(file_path):
    if not os.path.exists(file_path):
        return []
    ext = file_path.lower().split('.')[-1]
    
    try:
        if ext in ['jpg', 'jpeg', 'png']:
            img = cv2.imread(file_path)
            if img is None: return []
            return reader.readtext(img, paragraph=False, detail=0)
        
        elif ext in ['mp4', 'mov', 'avi']:
            cap = cv2.VideoCapture(file_path)
            if not cap.isOpened(): return []
            
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if frame_count > 0:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count // 2)
                ret, frame = cap.read()
                if ret:
                    res = reader.readtext(frame, paragraph=False, detail=0)
                    cap.release()
                    return res
            cap.release()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return []

def is_likely_code(text):
    text = text.strip().upper()
    if len(text) < 3 or len(text) > 12: 
        return False
        
    ignore_words = ['PRICE', 'FREE', 'SHIPPING', 'ALL', 'OVER', 'INDIA', 'LENGTH', 'INCH', 'GOLD', 'MICRO', 'MANGALSUTRA', 'COMBO', 'SET', 'PREMIUM', 'QUALITY', 'HANDMADE', 'FORMING', 'EACH', 'WATERPROOF', 'RS', 'OFF']
    if text in ignore_words:
        return False
        
    if any(c.isdigit() for c in text):
        return True
    
    if text.isupper() and " " not in text:
        if text not in ignore_words:
            return True
            
    return False

def get_ocr_code(file_path):
    raw_texts = extract_text(file_path)
    codes = [t.strip() for t in raw_texts if is_likely_code(t)]
    return ", ".join(codes)

def main():
    processed_files = set()
    existing_df = None
    
    if os.path.exists(EXCEL_PATH):
        try:
            existing_df = pd.read_excel(EXCEL_PATH)
            if 'File Name' in existing_df.columns:
                processed_files = set(existing_df['File Name'].dropna().astype(str))
            print(f"Loaded existing catalog. {len(processed_files)} previously processed items found.")
        except Exception as e:
            print(f"Warning: Could not read existing {EXCEL_PATH}. Assuming empty. Error: {e}")
            
    chat_files = glob.glob(os.path.join(DATA_DIR, '*.txt'))
    if not chat_files:
        print(f"No WhatsApp chat .txt files found in {DATA_DIR}/. Please place your chat export there.")
        return
        
    chat_file = chat_files[0]
    safe_name = os.path.basename(chat_file).encode('ascii', 'replace').decode('ascii')
    print(f"Processing chat log: {safe_name}")
    
    with open(chat_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_records = []
    current_file = None
    current_desc_lines = []
    
    # Regex for "10/03/2026, 6:03 pm -" or "10/03/2026, 11:58 am -"
    timestamp_regex = re.compile(r"^\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s[a|p]m\s-")
    
    def process_item(file_name, desc_lines):
        if not file_name:
            return
            
        if str(file_name).strip() in processed_files:
            return # Skip already processed files
            
        desc = "\n".join(desc_lines).strip()
        price_match = re.search(r"Price\s*-\s*(\d+)", desc, re.IGNORECASE)
        
        orig_price = 0.0
        margin = 0.0
        rounded_margin = 0
        our_price = 0
        mod_desc = desc
        
        if price_match:
            orig_price = float(price_match.group(1))
            margin = orig_price * 0.35
            rounded_margin = round(margin)
            our_price = int(orig_price + rounded_margin)
            mod_desc = desc[:price_match.start(1)] + str(our_price) + desc[price_match.end(1):]
            
        media_path = os.path.join(DATA_DIR, file_name)
        ocr_code = get_ocr_code(media_path)
        print(f"Processed new item: {file_name} -> OCR: {ocr_code if ocr_code else 'none'}")
        
        record = {
            "File Name": file_name,
            "Drive Link": "",
            "Code": "",
            "Original Item Description": desc.replace('\n', ' '),
            "original price Rs. (A)": orig_price,
            "35%Margin price Rs": margin,
            "Roud Off (B)": rounded_margin,
            "(Our Price Rs (A +B)": our_price,
            "Modified Item Description": mod_desc.replace('\n', ' '),
            "Extracted Codes (OCR)": ocr_code
        }
        new_records.append(record)

    for line in lines:
        if timestamp_regex.search(line):
            process_item(current_file, current_desc_lines)
            
            current_file = None
            current_desc_lines = []
            
            if "(file attached)" in line:
                match = re.search(r":\s*(IMG-.*?\.jpg|VID-.*?\.mp4)\s*\(file attached\)", line)
                if match:
                    current_file = match.group(1)
        else:
            if current_file:
                curr_line_clean = line.strip()
                if curr_line_clean != "":
                    current_desc_lines.append(curr_line_clean)
                    
    process_item(current_file, current_desc_lines)
    
    if not new_records:
        print("No new records to process. Catalog is up to date!")
        return
        
    print(f"Successfully processed {len(new_records)} new records!")
    new_df = pd.DataFrame(new_records)
    
    if existing_df is not None and not existing_df.empty:
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df
        
    combined_df.to_csv(CSV_PATH, index=False)
    combined_df.to_excel(EXCEL_PATH, index=False)
    print("Catalog successfully updated with new files and OCR codes.")

if __name__ == "__main__":
    main()
