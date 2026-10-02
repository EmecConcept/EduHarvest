# EduHarvest 🌾

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458)
![Scraping](https://img.shields.io/badge/Web_Scraping-BeautifulSoup-brightgreen)
![Regex](https://img.shields.io/badge/Regex-Data%20Extraction-black)


An automated web scraping and data pipeline built with Python, designed to harvest, clean, and categorize **authentic, official past questions** from online CBT examination archives (covering UTME/JAMB exams spanning over two decades).

Unlike randomly generated quizzes or user-contributed questions, **EduHarvest** preserves real past exam papers, retaining diagram references, formatting structures, and mathematical notations for use in modern educational applications.

---

## 🚀 Key Features

* **Authentic Past Exam Archives:** Mines real historical examination papers year-by-year, appending the exact exam year to each question.
* **Math & Scientific Formula Preservation:** Extracts raw HTML rather than stripping it, preserving embedded LaTeX notation, complex fractions, and HTML table layouts for accurate frontend rendering (e.g., via MathJax).
* **Diagram Extraction & URL Sanitization:** Detects missing or broken image assets in physics/geometry questions and reconstructs clean, usable URLs.
* **High-Speed Threading:** Utilizes Python's `ThreadPoolExecutor` to fetch hundreds of question explanations concurrently, bypassing network bottlenecks.
* **Regex-Powered Topic Classification:** Automatically scans question text against a robust dictionary of subject-specific keywords to categorize raw data into academic chapters.

---

## 🛠️ The Pipeline Architecture

The extraction process is split into two modular scripts to ensure data integrity.

### 1. The Extractor (`scraper.py`)
Connects to the API, paginates through historical years, and builds the initial dataset. 
* **Phase 1:** Pulls the base questions, options, and correct answers.
* **Phase 2:** Spawns concurrent threads to fetch detailed explanations for every single question.
* **Phase 3:** Flattens the nested JSON responses into a structured Pandas DataFrame and exports `{subject}_raw_cbt.csv`.

### 2. The Classifier (`topic_classifier.py`)
Acts as the transformation layer. It reads the raw CSV and uses Regex word-boundary matching to assign each question to a specific academic chapter based on a predefined `TOPIC_DICTIONARY`. It then sorts the entire dataset chronologically by chapter and exports a production-ready `{subject}_final_cbt.csv`.

---

## ⚙️ Setup & Usage

### Prerequisites
You will need Python installed along with a few standard data libraries:
`pip install pandas requests beautifulsoup4`

### Step 1: Run the Scraper
1. Open `scraper.py`.
2. Edit the configuration block at the top to set your desired `SUBJECT` and `TARGET` (number of questions).
3. Run the script:
`python scraper.py`

### Step 2: Classify the Data
1. Open `topic_classifier.py`.
2. Ensure the `SUBJECT` variable matches the one you just scraped.
3. Define your `TOPIC_DICTIONARY` if you are scraping a new subject.
4. Run the script:
`python topic_classifier.py`
*(This generates `{subject}_final_cbt.csv`, ready for database injection).*

---

## 🖥️ Frontend Rendering Notes (For Web/Mobile Apps)
Because this pipeline intentionally preserves raw HTML to protect complex math and physics formatting, ensure your frontend application handles the text properly:
* Inject the explanation strings directly into the DOM (e.g., `innerHTML` in React/JS or `|safe` in Django).
* Apply `white-space: normal;` in your CSS to collapse the native developer formatting (invisible line breaks) while maintaining HTML table structures.
* Run MathJax over the rendered DOM to typeset the preserved LaTeX strings.

---

## 🤝 Let's Connect / Hire Me
I am a Backend Developer and Data Engineer specializing in Python, Django, and automated web scraping pipelines. If you need a custom scraping tool, a CBT application, or scalable backend infrastructure, let's talk.

* **Email:** e08132m@gmail.com
* **WhatsApp:** [Click here to chat](https://wa.me/2349042741758)
* **LinkedIn:** https://www.linkedin.com/in/chukwunonso-enwerem-7364b1365
