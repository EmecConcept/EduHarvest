import requests
import json
import time
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==========================================
# 1. CONFIGURATION
# ==========================================
# Available Myschool Subjects:
# "english-language", "mathematics", "physics", "chemistry", "biology", "economics", "government", "literature-in-english", "commerce", "agricultural-science", "geography", "christian-religious-knowledge", "islamic-religious-knowledge", "history", "accounting", "french", "hausa", "igbo", "yoruba"

SUBJECT = "english-language" 

TARGET = 2000
YEARS = list(range(2025, 2009, -1))

BASE_LIST_URL = f"https://myschool.ng/api/web/v1/classroom/{SUBJECT}"
BASE_DETAIL_URL = f"https://myschool.ng/api/web/v1/classroom/{SUBJECT}/"

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def clean_html(raw_html):
    if not raw_html:
        return "No explanation provided."
    return str(raw_html).strip()


def fetch_with_retries(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            if res.status_code == 200:
                return res
            elif res.status_code in [403, 429]: 
                time.sleep((attempt + 1) * 3)
        except requests.RequestException:
            pass
        time.sleep(2 ** attempt)
    return None

# ==========================================
# PHASE 1: EXTRACT BASE QUESTIONS
# ==========================================
print(f"\n[PHASE 1] Extracting {TARGET} {SUBJECT.upper()} Questions...")
all_questions = []

for year in YEARS:
    if len(all_questions) >= TARGET: break
    page = 1
    
    while len(all_questions) < TARGET:
        url = f"{BASE_LIST_URL}?exam_type=jamb&exam_year={year}&page={page}"
        res = fetch_with_retries(url)
        if not res: 
            break
            
        payload = res.json()
        batch = payload.get("data", {}).get("practice_questions", {}).get("data", [])
        
        if not batch: break
        
        for q in batch:
            q["exam_year"] = year
            if len(all_questions) < TARGET:
                all_questions.append(q)
        
        print(f"Secured: {len(all_questions)}/{TARGET} (Year {year}, Page {page})")
        if not payload["data"]["practice_questions"].get("next_page_url"): 
            break
        
        page += 1
        time.sleep(1) 

# ==========================================
# PHASE 2: CONCURRENT EXPLANATION EXTRACTOR
# ==========================================
print(f"\n[PHASE 2] Fetching {len(all_questions)} Explanations via ThreadPool...")
all_explanations = []

def fetch_single_explanation(q):
    if q.get("explanation"):
        return {"id": q["id"], "explanation": clean_html(q["explanation"])}
      
    q_id = q["id"]
    res = fetch_with_retries(f"{BASE_DETAIL_URL}{q_id}")
    if res:
        raw_exp = res.json().get("data", {}).get("question", {}).get("explanation", "")
        return {"id": q_id, "explanation": clean_html(raw_exp)}
    return {"id": q_id, "explanation": "No explanation provided."}

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(fetch_single_explanation, q): q for q in all_questions}
    for i, future in enumerate(as_completed(futures), start=1):
        all_explanations.append(future.result())
        if i % 50 == 0:
            print(f"Processed {i}/{len(all_questions)} explanations...")

# ==========================================
# PHASE 3: PANDAS MERGE & TRANSFORM
# ==========================================
print(f"\n[PHASE 3] Merging datasets

flattened_rows = []
for q in all_questions:
    text = clean_html(q.get("question", ""))
    exam_year = q.get("exam_year", "")
    if exam_year:
        text += f" (JAMB {exam_year})"
      
    if q.get("image"):
        text += f" [View Diagram: https://myschool.ng/storage/classroom/{q['image']}]"
        
    opts = {'a': '', 'b': '', 'c': '', 'd': ''}
    correct_ans = ''
    for opt in q.get("options", []):
        tag = opt["tag"].lower()
        opts[tag] = clean_html(opt["description"])
        if opt["is_correct"] == 1:
            correct_ans = tag.upper()
            
    flattened_rows.append({
        "id": q["id"],
        "text": text,
        "option_a": opts['a'],
        "option_b": opts['b'],
        "option_c": opts['c'],
        "option_d": opts['d'],
        "correct_option": correct_ans
    })

df_questions = pd.DataFrame(flattened_rows)
df_explanations = pd.DataFrame(all_explanations)
df_final = pd.merge(df_questions, df_explanations, on="id", how="left")


final_columns = ["text", "option_a", "option_b", "option_c", "option_d", "correct_option", "explanation"]
df_final = df_final[final_columns]
df_final.fillna("Not provided", inplace=True)

csv_filename = f"{SUBJECT}_raw_cbt.csv"
df_final.to_csv(csv_filename, index=False)
print(f"\n[SUCCESS] Raw Database saved as: {csv_filename}")