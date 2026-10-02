import pandas as pd
import re

# ==========================================
# 1. EDIT ONLY THIS SECTION
# ==========================================
SUBJECT = "physics"

# Map out your chapters and the keywords that identify them.
# Write keywords in lowercase. The script will find them automatically.
TOPIC_DICTIONARY = {
    "Chapter 1: Units, Measurements & Vectors": ["dimension", "unit", "units", "vernier", "micrometer", "measurement", "measure", "scalar", "vector", "resultant", "component", "fundamental", "derived", "quantity", "calipers"],
    "Chapter 2: Kinematics (Motion & Gravity)": ["velocity", "acceleration", "accelerate", "accelerating", "speed", "displacement", "distance", "gravity", "gravitational", "gravitation", "projectile", "free fall", "uniform motion", "rest", "moving", "moves", "circular motion", "centripetal", "centrifugal", "trajectory", "rocket", "jet", "time of flight", "maximum height", "linear motion", "kinematics"],
    "Chapter 3: Dynamics (Force, Work, Energy & Power)": ["force", "forces", "momentum", "work", "energy", "power", "friction", "frictional", "newton", "impulse", "equilibrium", "machine", "pulley", "mechanical advantage", "velocity ratio", "efficiency", "tension", "moment", "pivot", "centre of gravity", "balance", "knife edge", "inertia", "collision", "meter rule", "metre rule", "spring balance", "weight", "mass", "statics", "couple", "tyres", "tread"],
    "Chapter 4: Properties of Matter & Fluids": ["density", "upthrust", "archimedes", "flotation", "float", "sink", "sinks", "elasticity", "hooke", "stress", "strain", "surface tension", "viscosity", "pressure", "young's modulus", "kinetic theory", "brownian", "osmosis", "diffusion", "capillarity", "liquid", "gas", "barometer", "manometer", "atmospheric", "altitude", "streamline", "drag", "fluid", "droplet"],
    "Chapter 5: Heat & Thermodynamics": ["temperature", "heat", "thermal", "expansion", "expansivity", "gas law", "boyle", "charles", "thermodynamics", "specific heat", "latent heat", "conduction", "convection", "radiation", "boiling", "melting", "freezing", "thermometer", "thermometric", "celsius", "kelvin", "fahrenheit", "vaporization", "evaporation", "particles", "cloud", "fog", "dew", "humidity", "vapor", "vapour", "ice", "steam", "breeze"],
    "Chapter 6: Waves & Sound": ["wave", "waves", "sound", "frequency", "wavelength", "amplitude", "resonance", "echo", "echoes", "doppler", "pitch", "timbre", "harmonic", "interference", "diffraction", "node", "antinode", "transverse", "longitudinal", "acoustic", "reverberation", "overtone", "vibration", "tuning fork", "string", "auditorium", "pipe", "beats", "pendulum", "period"],
    "Chapter 7: Optics & Light": ["light", "lens", "lenses", "mirror", "mirrors", "reflection", "refraction", "refractive index", "prism", "optical", "eye", "microscope", "telescope", "focal length", "real image", "virtual image", "image", "snell", "camera", "vision", "short-sighted", "long-sighted", "defect", "hypermetropia", "myopia", "dispersion", "spectrum", "eclipse", "shadow", "umbra", "penumbra", "pinhole", "pigment", "color", "colour"],
    "Chapter 8: Electricity": ["electric", "electrical", "current", "voltage", "resistance", "resistor", "ohm", "circuit", "capacitance", "capacitor", "galvanometer", "ammeter", "voltmeter", "charge", "coulomb", "potential difference", "e.m.f", "electrolysis", "faraday", "cell", "battery", "electrolyte", "kirchhoff", "potentiometer", "wheatstone", "resistivity", "conductivity", "solar", "inverter", "electrostatics", "parallel", "series", "accumulator", "electroscope", "insulator", "conductor"],
    "Chapter 9: Magnetism & Electromagnetism": ["magnet", "magnetic", "electromagnetic", "transformer", "induction", "generator", "motor", "flux", "lenz", "alternating current", "a.c", "d.c", "compass", "solenoid", "eddy current", "inductor", "dynamo", "dip", "declination"],
    "Chapter 10: Modern & Nuclear Physics": ["radioactivity", "nuclear", "atom", "atomic", "electron", "proton", "neutron", "isotope", "half-life", "alpha", "beta", "gamma", "x-ray", "photoelectric", "semiconductor", "diode", "cathode", "work function", "photon", "photovoltaic", "emission", "quantum", "planck", "bohr", "binding energy", "fission", "fusion", "transistor", "logic gate", "rectifier", "nuclide", "decay", "radioactive", "modern physics"]
}

# Where questions go if they don't match any keywords above
FALLBACK_CHAPTER = "Chapter 11: General & Miscellaneous Physics"




# ==========================================
# 2. CORE LOGIC (DO NOT EDIT)
# ==========================================
INPUT_CSV = f"{SUBJECT}_raw_cbt.csv"
OUTPUT_CSV = f"{SUBJECT}_final_cbt.csv"

def classify_topic(text):
    """Scans text for keywords using word boundaries to prevent accidental matches."""
    text_lower = str(text).lower()
    
    for chapter_name, keywords in TOPIC_DICTIONARY.items():
        for keyword in keywords:
            # \b ensures we match whole words (e.g., 'art' won't match 'earth')
            pattern = rf"\b{re.escape(keyword)}\b"
            if re.search(pattern, text_lower):
                return chapter_name
                
    return FALLBACK_CHAPTER

if __name__ == "__main__":
    print(f"Loading raw data from: {INPUT_CSV}...")
    
    try:
        df = pd.read_csv(INPUT_CSV)
    except FileNotFoundError:
        print(f"Error: Could not find {INPUT_CSV}. Run your scraper first!")
        exit()

    print("Scanning questions and sorting into chapters...")
    # Apply the classifier
    df['chapter'] = df['text'].apply(classify_topic)

    # note this reordering is specific based on how my client CBT was it's maybe different 

    final_order = ["chapter", "text", "option_a", "option_b", "option_c", "option_d", "correct_option", "explanation"]
    
    # Ensure all required columns exist before reordering
    for col in final_order:
        if col not in df.columns:
            df[col] = "Not provided" if col == "explanation" else ""
            
    df = df[final_order]

    # Extract the numerical chapter value and sort the file mathematically
    df['chapter_num'] = df['chapter'].str.extract(r'Chapter (\d+)').astype(int)
    df = df.sort_values(by="chapter_num").drop(columns=['chapter_num'])

    # Save the final file
    df.to_csv(OUTPUT_CSV, index=False)

    print("\n==========================================")
    print("📊 CHAPTER DISTRIBUTION SUMMARY")
    print("==========================================")
    # Print exactly how many questions landed in each chapter
    chapter_counts = df['chapter'].value_counts()
    for chap, count in chapter_counts.items():
        print(f"{chap}: {count} questions")
        
    print("==========================================")
    print(f"[SUCCESS] Upload-ready file saved to: {OUTPUT_CSV}")

#u can now upload to Ur database 