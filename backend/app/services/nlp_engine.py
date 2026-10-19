import re
from typing import Dict, Any, List, Optional

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Puducherry", "Chandigarh"
]

COMMON_DISTRICTS = [
    "Mumbai", "Pune", "Nagpur", "Nashik", "Thane", "Aurangabad", "Solapur", "Kolhapur", "Amravati", "Nanded",
    "Lucknow", "Kanpur", "Varanasi", "Prayagraj", "Agra", "Meerut", "Gorakhpur",
    "Patna", "Gaya", "Muzaffarpur", "Bhagalpur",
    "Ahmedabad", "Surat", "Vadodara", "Rajkot",
    "Bengaluru", "Mysuru", "Hubballi", "Mangaluru",
    "Jaipur", "Jodhpur", "Udaipur", "Kota",
    "Bhopal", "Indore", "Gwalior", "Jabalpur",
    "Chennai", "Coimbatore", "Madurai", "Tiruchirappalli",
    "Hyderabad", "Warangal", "Nizamabad",
    "Kolkata", "Howrah", "Durgapur", "Siliguri"
]

OCCUPATIONS = [
    ("farmer", "Farmer / Shetkari / Kisan"),
    ("kisan", "Farmer / Shetkari / Kisan"),
    ("shetkari", "Farmer / Shetkari / Kisan"),
    ("agriculture", "Farmer / Shetkari / Kisan"),
    ("शेतकरी", "Farmer / Shetkari / Kisan"),
    ("किसान", "Farmer / Shetkari / Kisan"),
    ("daily wage", "Daily Wage Worker / Majdoor"),
    ("labourer", "Daily Wage Worker / Majdoor"),
    ("laborer", "Daily Wage Worker / Majdoor"),
    ("majdoor", "Daily Wage Worker / Majdoor"),
    ("मजदूर", "Daily Wage Worker / Majdoor"),
    ("कामगार", "Daily Wage Worker / Majdoor"),
    ("student", "Student"),
    ("studying", "Student"),
    ("विद्यार्थी", "Student"),
    ("छात्र", "Student"),
    ("small business", "Small Business Owner / Shopkeeper"),
    ("shopkeeper", "Small Business Owner / Shopkeeper"),
    ("merchant", "Small Business Owner / Shopkeeper"),
    ("दुकानदार", "Small Business Owner / Shopkeeper"),
    ("व्यापारी", "Small Business Owner / Shopkeeper"),
    ("business", "Business / Self-Employed"),
    ("self-employed", "Business / Self-Employed"),
    ("self employed", "Business / Self-Employed"),
    ("homemaker", "Homemaker"),
    ("housewife", "Homemaker"),
    ("गृहिणी", "Homemaker"),
    ("unemployed", "Unemployed"),
    ("बेरोजगार", "Unemployed"),
    ("teacher", "Teacher / Educator"),
    ("शिक्षक", "Teacher / Educator"),
    ("driver", "Driver"),
    ("चालक", "Driver"),
    ("ड्रायव्हर", "Driver"),
    ("carpenter", "Artisan / Carpenter"),
    ("सुतार", "Artisan / Carpenter"),
    ("electrician", "Artisan / Electrician"),
    ("artisan", "Artisan / Handicraft Worker"),
    ("कारीगर", "Artisan / Handicraft Worker"),
    ("private", "Private Employee"),
    ("software", "Private Employee (IT / Tech)"),
    ("government", "Government / PSU Employee"),
    ("govt", "Government / PSU Employee"),
    ("सरकारी", "Government / PSU Employee")
]

CATEGORIES = [
    ("sc", "SC (Scheduled Caste)"),
    ("scheduled caste", "SC (Scheduled Caste)"),
    ("अनुसूचित जाती", "SC (Scheduled Caste)"),
    ("st", "ST (Scheduled Tribe)"),
    ("scheduled tribe", "ST (Scheduled Tribe)"),
    ("अनुसूचित जमाती", "ST (Scheduled Tribe)"),
    ("अनुसूचित जनजाति", "ST (Scheduled Tribe)"),
    ("obc", "OBC (Other Backward Class)"),
    ("other backward", "OBC (Other Backward Class)"),
    ("इतर मागास", "OBC (Other Backward Class)"),
    ("अन्य पिछड़ा", "OBC (Other Backward Class)"),
    ("ews", "EWS (Economically Weaker Section)"),
    ("general", "General / Open"),
    ("open", "General / Open"),
    ("खुला", "General / Open"),
    ("सामान्य", "General / Open"),
    ("minority", "Minority (Muslim/Christian/Sikh/Buddhist/Jain/Parsi)"),
    ("अल्पसंख्याक", "Minority (Muslim/Christian/Sikh/Buddhist/Jain/Parsi)")
]

GENDER_MAP = {
    "male": "Male",
    "man": "Male",
    "boy": "Male",
    "purush": "Male",
    "पुरुष": "Male",
    "female": "Female",
    "woman": "Female",
    "girl": "Female",
    "mahila": "Female",
    "stri": "Female",
    "महिला": "Female",
    "स्त्री": "Female",
    "transgender": "Transgender",
    "तृतीयपंथी": "Transgender",
    "other": "Other"
}

EDUCATION_LEVELS = [
    ("post graduate", "Post Graduate (Master's Degree)"),
    ("postgraduate", "Post Graduate (Master's Degree)"),
    ("master", "Post Graduate (Master's Degree)"),
    ("graduate", "Graduate (Bachelor's Degree)"),
    ("graduation", "Graduate (Bachelor's Degree)"),
    ("degree", "Graduate (Bachelor's Degree)"),
    ("पदवीधर", "Graduate (Bachelor's Degree)"),
    ("b.tech", "Graduate (B.Tech / Engineering)"),
    ("b.e.", "Graduate (Engineering)"),
    ("b.sc", "Graduate (B.Sc)"),
    ("b.com", "Graduate (B.Com)"),
    ("b.a.", "Graduate (B.A.)"),
    ("diploma", "Diploma"),
    ("12th pass", "Higher Secondary (12th Pass / HSC)"),
    ("12th", "Higher Secondary (12th Pass / HSC)"),
    ("hsc", "Higher Secondary (12th Pass / HSC)"),
    ("बारावी", "Higher Secondary (12th Pass / HSC)"),
    ("बारहवीं", "Higher Secondary (12th Pass / HSC)"),
    ("barahvi", "Higher Secondary (12th Pass / HSC)"),
    ("10th pass", "Secondary (10th Pass / SSC)"),
    ("10th", "Secondary (10th Pass / SSC)"),
    ("ssc", "Secondary (10th Pass / SSC)"),
    ("दहावी", "Secondary (10th Pass / SSC)"),
    ("दसवीं", "Secondary (10th Pass / SSC)"),
    ("dasvi", "Secondary (10th Pass / SSC)"),
    ("illiterate", "No Formal Education / Illiterate"),
    ("अशिक्षित", "No Formal Education / Illiterate"),
    ("निरक्षर", "No Formal Education / Illiterate"),
    ("primary school", "Primary School")
]

DEVANAGARI_DIGITS_MAP = str.maketrans("०१२३४५६७८९", "0123456789")

def clean_text(text: str) -> str:
    if not text:
        return ""
    # Map Devanagari numerals (०-९) to ASCII digits (0-9) for robust regex pattern matching
    text = text.translate(DEVANAGARI_DIGITS_MAP)
    # Normalize excessive spaces and common speech transcription artifacts
    return " ".join(text.strip().split())

def extract_name(text: str) -> Optional[Dict[str, Any]]:
    # 1. Pattern: My name is X / I am X / Myself X / Name: X / Applicant is X / Devanagari names
    patterns = [
        r"(?:my name is|i am|myself|this is|name is|applicant name is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})",
        r"(?:my name is|i am|myself|this is|name is|applicant name is)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+){1,3})",
        r"(?:mera naam|maze naav|majhe naav)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+){1,3})",
        r"(?:माझे नाव|माझं नाव|नाव आहे|मेरा नाम|नाम है|नाव|नाम|मी|मैं)\s*[:=]?\s*([^\s,।\n]+(?:\s+[^\s,।\n]+){1,3})"
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()
            # Eliminate common stop words accidentally captured
            stop_words = ["a", "an", "the", "living", "working", "from", "in", "currently", "now", "seeking", "applying", "आहे", "है", "हूँ", "राहतो", "राहते"]
            honorifics = ["shri", "shrimati", "smt", "smt.", "mr", "mr.", "mrs", "mrs.", "ms", "ms.", "dr", "dr.", "श्री", "श्रीमती"]
            words = [w for w in candidate.split() if w.lower() not in stop_words and w.lower() not in honorifics]
            if len(words) >= 1:
                title_cased = " ".join(w.capitalize() for w in words[:3])
                return {"value": title_cased, "confidence": 0.94, "source": match.group(0)}

    # Fallback heuristic: check for capitalized name-like bigrams near beginning
    bigram_match = re.search(r"\b([A-Z][a-z]{2,15}\s+[A-Z][a-z]{2,15})\b", text)
    if bigram_match:
        val = bigram_match.group(1).strip()
        # Ensure not state or district
        if val not in INDIAN_STATES and val not in COMMON_DISTRICTS:
            return {"value": val, "confidence": 0.72, "source": val}

    return None

def extract_age(text: str) -> Optional[Dict[str, Any]]:
    # E.g. "I am 20 years old", "20 years of age", "age is 45", "वय 42", "उम्र 35"
    patterns = [
        r"(?:i am|age is|aged|age)\s*[:=]?\s*(\d{1,3})\s*(?:years|yrs)?",
        r"(\d{1,3})\s*(?:years old|yrs old|year old|saal|varsha)",
        r"(?:वय|आयु|उम्र)\s*[:=]?\s*(\d{1,3})",
        r"(\d{1,3})\s*(?:साल|वर्ष|वर्षे|वय)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                age_val = int(match.group(1))
                if 1 <= age_val <= 115:
                    return {"value": age_val, "confidence": 0.95, "source": match.group(0)}
            except ValueError:
                pass
    return None

def extract_education(text: str) -> Optional[Dict[str, Any]]:
    lower = text.lower()
    for trigger, edu_name in EDUCATION_LEVELS:
        if re.search(rf"\b{re.escape(trigger)}\b", lower, re.IGNORECASE) or trigger in text:
            return {"value": edu_name, "confidence": 0.92, "source": trigger}
    return None

def extract_dob(text: str) -> Optional[Dict[str, Any]]:
    patterns = [
        r"(?:date of birth|dob|born on|जन्म तारीख|जन्म दिनांक)\s*[:=]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        r"\b(\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})\b"
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return {"value": match.group(1), "confidence": 0.90, "source": match.group(0)}
    return None

DEVANAGARI_STATES = {
    "महाराष्ट्र": "Maharashtra", "बिहार": "Bihar", "उत्तर प्रदेश": "Uttar Pradesh",
    "मध्य प्रदेश": "Madhya Pradesh", "गुजरात": "Gujarat", "राजस्थान": "Rajasthan",
    "कर्नाटक": "Karnataka", "पंजाब": "Punjab", "हरियाणा": "Haryana",
    "पश्चिम बंगाल": "West Bengal", "तामिळनाडू": "Tamil Nadu", "तमिलनाडु": "Tamil Nadu",
    "केरळ": "Kerala", "केरल": "Kerala", "आंध्र प्रदेश": "Andhra Pradesh",
    "तेलंगणा": "Telangana", "तेलंगाना": "Telangana", "ओडिशा": "Odisha",
    "झारखंड": "Jharkhand", "छत्तीसगड": "Chhattisgarh", "छत्तीसगढ़": "Chhattisgarh",
    "उत्तराखंड": "Uttarakhand", "हिमाचल प्रदेश": "Himachal Pradesh",
    "आसाम": "Assam", "असम": "Assam", "गोवा": "Goa", "दिल्ली": "Delhi"
}

DEVANAGARI_DISTRICTS = {
    "पुणे": "Pune", "सातारा": "Satara", "सांगली": "Sangli", "कोल्हापूर": "Kolhapur",
    "सोलापूर": "Solapur", "नाशिक": "Nashik", "अहमदनगर": "Ahmednagar",
    "छत्रपती संभाजीनगर": "Chhatrapati Sambhaji Nagar", "औरंगाबाद": "Chhatrapati Sambhaji Nagar",
    "जालना": "Jalna", "नांदेड": "Nanded", "परभणी": "Parbhani", "लातूर": "Latur",
    "बीड": "Beed", "धाराशिव": "Dharashiv", "उस्मानाबाद": "Dharashiv",
    "नागपूर": "Nagpur", "अमरावती": "Amravati", "अकोला": "Akola", "बुलढाणा": "Buldhana",
    "यवतमाळ": "Yavatmal", "वर्धा": "Wardha", "चंद्रपूर": "Chandrapur", "गडचिरोली": "Gadchirli",
    "गोंदिया": "Gondia", "भंडारा": "Bhandara", "मुंबई": "Mumbai", "ठाणे": "Thane",
    "पालघर": "Palghar", "रायगड": "Raigad", "रत्नागिरी": "Ratnagiri", "सिंधुदुर्ग": "Sindhudurg",
    "धुळे": "Dhule", "जळगाव": "Jalgaon", "नंदुरबार": "Nandurbar",
    "पटना": "Patna", "गया": "Gaya", "मुजफ्फरपुर": "Muzaffarpur", "भागलपुर": "Bhagalpur",
    "भोपाल": "Bhopal", "इन्दौर": "Indore", "इंदौर": "Indore", "ग्वालियर": "Gwalior", "जबलपुर": "Jabalpur",
    "लखनऊ": "Lucknow", "कानपुर": "Kanpur", "वाराणसी": "Varanasi", "प्रयागराज": "Prayagraj",
    "आगरा": "Agra", "मेरठ": "Meerut", "गोरखपुर": "Gorakhpur",
    "अहमदाबाद": "Ahmedabad", "सूरत": "Surat", "वडोदरा": "Vadodara", "राजकोट": "Rajkot",
    "जयपुर": "Jaipur", "जोधपुर": "Jodhpur", "उदयपुर": "Udaipur", "कोटा": "Kota"
}

def extract_gender(text: str) -> Optional[Dict[str, Any]]:
    lower = text.lower()
    for trigger, gender in GENDER_MAP.items():
        if re.search(rf"\b{re.escape(trigger)}\b", lower) or trigger in text:
            return {"value": gender, "confidence": 0.94, "source": trigger}
    return None

def extract_phone(text: str) -> Optional[Dict[str, Any]]:
    # Match standard 10 digit Indian phone numbers (+91-9876543210, 98765 43210, etc.)
    match = re.search(r"(?:(?:\+?91[\s-]?)?[6-9]\d{9})\b", text)
    if match:
        raw = match.group(0)
        digits = re.sub(r"\D", "", raw)
        if len(digits) > 10:
            digits = digits[-10:]
        if len(digits) == 10 and digits[0] in "6789":
            return {"value": digits, "confidence": 0.98, "source": match.group(0)}
    return None

def extract_aadhaar(text: str) -> Optional[Dict[str, Any]]:
    # 12 digits: e.g. 1234 5678 9012 or 123456789012
    match = re.search(r"\b(\d{4}[\s-]?\d{4}[\s-]?\d{4})\b", text)
    if match:
        clean_num = re.sub(r"[\s-]", "", match.group(1))
        # Ensure it's not a phone number or pincode
        if len(clean_num) == 12 and not clean_num.startswith("0") and not clean_num.startswith("1"):
            formatted = f"{clean_num[:4]} {clean_num[4:8]} {clean_num[8:]}"
            return {"value": formatted, "confidence": 0.96, "source": match.group(0)}
    return None

def extract_pan(text: str) -> Optional[Dict[str, Any]]:
    # Standard Indian PAN format: 5 uppercase letters + 4 digits + 1 uppercase letter
    match = re.search(r"\b([A-Za-z]{5}\d{4}[A-Za-z]{1})\b", text)
    if match:
        return {"value": match.group(1).upper(), "confidence": 0.99, "source": match.group(0)}
    return None

def extract_email(text: str) -> Optional[Dict[str, Any]]:
    match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
    if match:
        return {"value": match.group(0).lower(), "confidence": 0.99, "source": match.group(0)}
    return None

def extract_pincode(text: str) -> Optional[Dict[str, Any]]:
    # 6-digit Indian PIN code starting with 1-9
    match = re.search(r"(?:pin|pincode|postal code|zip)?\s*[:=]?\s*\b([1-9]\d{5})\b", text, re.IGNORECASE)
    if match:
        return {"value": match.group(1), "confidence": 0.92, "source": match.group(0)}
    return None

def extract_state(text: str) -> Optional[Dict[str, Any]]:
    for dev_st, eng_st in DEVANAGARI_STATES.items():
        if dev_st in text:
            return {"value": eng_st, "confidence": 0.98, "source": dev_st}
    for st in INDIAN_STATES:
        if re.search(rf"\b{re.escape(st)}\b", text, re.IGNORECASE):
            return {"value": st, "confidence": 0.97, "source": st}
    return None

def extract_district(text: str) -> Optional[Dict[str, Any]]:
    for dev_dist, eng_dist in DEVANAGARI_DISTRICTS.items():
        if dev_dist in text:
            return {"value": eng_dist, "confidence": 0.96, "source": dev_dist}
    for dist in COMMON_DISTRICTS:
        if re.search(rf"\b{re.escape(dist)}\b", text, re.IGNORECASE):
            return {"value": dist, "confidence": 0.95, "source": dist}
    # Pattern: district X / dist X / जिल्हा X / जिला X
    match = re.search(r"(?:district|dist|जिल्हा|जिला)\s*[:=]?\s*([A-Za-z\u0900-\u097F]+)", text, re.IGNORECASE)
    if match:
        val = match.group(1).strip()
        if val not in INDIAN_STATES and val not in DEVANAGARI_STATES:
            return {"value": val.capitalize(), "confidence": 0.85, "source": match.group(0)}
    return None

def extract_address(text: str) -> Optional[Dict[str, Any]]:
    # Pattern: live in X / resident of X / address is X
    patterns = [
        r"(?:i live in|residing at|resident of|address is|permanent address is)\s+([^.,;\n]+(?:,\s*[^.,;\n]+)*)",
        r"(?:at village|post)\s+([^.,;\n]+)"
    ]
    for p in patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            addr = match.group(1).strip()
            if len(addr) > 3:
                return {"value": addr.title(), "confidence": 0.82, "source": match.group(0)}
    return None

def extract_occupation(text: str) -> Optional[Dict[str, Any]]:
    lower = text.lower()
    for keyword, standard_name in OCCUPATIONS:
        if re.search(rf"\b{re.escape(keyword)}\b", lower) or keyword in text:
            return {"value": standard_name, "confidence": 0.90, "source": keyword}
    return None

INDIAN_WORD_INCOMES = [
    ("डेढ़ लाख", 150000), ("दीड लाख", 150000), ("dedh lakh", 150000),
    ("ढाई लाख", 250000), ("अडीच लाख", 250000), ("dhai lakh", 250000),
    ("साडेतीन लाख", 350000), ("साढ़े तीन लाख", 350000),
    ("एक लाख", 100000), ("one lakh", 100000),
    ("दोन लाख", 200000), ("दो लाख", 200000), ("two lakh", 200000),
    ("तीन लाख", 300000), ("three lakh", 300000),
    ("चार लाख", 400000), ("four lakh", 400000),
    ("पाच लाख", 500000), ("पाँच लाख", 500000), ("five lakh", 500000),
    ("दहा लाख", 1000000), ("दस लाख", 1000000), ("ten lakh", 1000000),
    ("पन्नास हजार", 50000), ("पचास हजार", 50000), ("fifty thousand", 50000),
    ("साठ हजार", 60000), ("sixty thousand", 60000),
    ("सत्तर हजार", 70000), ("seventy thousand", 70000),
    ("ऐंशी हजार", 80000), ("अस्सी हजार", 80000), ("eighty thousand", 80000),
    ("नव्वद हजार", 90000), ("नब्बे हजार", 90000), ("ninety thousand", 90000)
]

def extract_income(text: str) -> Optional[Dict[str, Any]]:
    # 0. Check Indian word number expressions (e.g. "एक लाख", "डेढ़ लाख", "दीड लाख", "ऐंशी हजार")
    lower = text.lower()
    for phrase, amount in INDIAN_WORD_INCOMES:
        if phrase in lower or phrase in text:
            return {
                "value": amount,
                "formatted": f"₹{amount:,}",
                "confidence": 0.95,
                "source": phrase
            }

    # Matches: "income is 1.5 lakh", "1.5 लाख", "80 thousand", "80 हजार", "salary 50000"
    lakh_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|lac|lacs|लाख)\b", text, re.IGNORECASE)
    if lakh_match:
        try:
            val = float(lakh_match.group(1)) * 100000
            return {
                "value": int(val),
                "formatted": f"₹{int(val):,}",
                "confidence": 0.94,
                "source": lakh_match.group(0)
            }
        except ValueError:
            pass

    thousand_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:thousand|हजार|हज़ार)\b", text, re.IGNORECASE)
    if thousand_match:
        try:
            val = float(thousand_match.group(1)) * 1000
            return {
                "value": int(val),
                "formatted": f"₹{int(val):,}",
                "confidence": 0.93,
                "source": thousand_match.group(0)
            }
        except ValueError:
            pass

    direct_match = re.search(r"(?:income|salary|earning|earns|paisa|आय|उत्पन्न)\s*(?:is|of|आहे|होती|है)?\s*(?:rs\.?|inr|₹|रु\.?|रुपये)?\s*(\d{4,9})", text, re.IGNORECASE)
    if direct_match:
        try:
            val = int(direct_match.group(1))
            return {
                "value": val,
                "formatted": f"₹{val:,}",
                "confidence": 0.92,
                "source": direct_match.group(0)
            }
        except ValueError:
            pass

    # Generic number with "per year" or "annual"
    annual_match = re.search(r"(\d{4,8})\s*(?:per year|annually|annual|per annum|वार्षिक)", text, re.IGNORECASE)
    if annual_match:
        try:
            val = int(annual_match.group(1))
            return {
                "value": val,
                "formatted": f"₹{val:,}",
                "confidence": 0.90,
                "source": annual_match.group(0)
            }
        except ValueError:
            pass

    return None

def extract_guardian_name(text: str) -> Optional[Dict[str, Any]]:
    # E.g. "father's name is Suresh Sharma", "वडिलांचे नाव सुरेश शर्मा आहे", "पतीचे नाव रमेश आहे"
    patterns = [
        r"(?:father's name is|father name is|father is|husband's name is|husband is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})",
        r"(?:father's name|father name|husband's name|husband name)\s*[:=]?\s*([a-zA-Z]+(?:\s+[a-zA-Z]+){1,3})",
        r"(?:पिता का नाम|पिताजी का नाम|पति का नाम)\s*[:=]?\s*([^\s,।\n]+(?:\s+[^\s,।\n]+){1,3})",
        r"(?:वडिलांचे नाव|पतीचे नाव)\s*[:=]?\s*([^\s,।\n]+(?:\s+[^\s,।\n]+){1,3})"
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            cand = m.group(1).strip()
            words = [w for w in cand.split() if w.lower() not in ["आहे", "है", "is", "a", "the", "श्री", "shri"]]
            if words:
                return {"value": " ".join(w.capitalize() for w in words[:3]), "confidence": 0.92, "source": m.group(0)}
    return None

def extract_category(text: str) -> Optional[Dict[str, Any]]:
    lower = text.lower()
    for trigger, cat_name in CATEGORIES:
        if re.search(rf"\b{re.escape(trigger)}\b", lower) or trigger in text:
            return {"value": cat_name, "confidence": 0.91, "source": trigger}
    return None

def extract_land_holding(text: str) -> Optional[Dict[str, Any]]:
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:acres?|acre|hectares?|hectare|guntha|bigha|एकर|हेक्टर)\b", text, re.IGNORECASE)
    if match:
        return {"value": match.group(0), "confidence": 0.93, "source": match.group(0)}
    if re.search(r"\b(marginal farmer|small farmer|landless|अल्पभूधारक|शेतजमीन नाही)\b", text, re.IGNORECASE):
        m = re.search(r"\b(marginal farmer|small farmer|landless|अल्पभूधारक|शेतजमीन नाही)\b", text, re.IGNORECASE)
        return {"value": m.group(1).title(), "confidence": 0.91, "source": m.group(0)}
    return None

def extract_marital_status(text: str) -> Optional[Dict[str, Any]]:
    lower = text.lower()
    if re.search(r"\b(unmarried|single|अविवाहित)\b", lower) or "अविवाहित" in text:
        return {"value": "Unmarried", "confidence": 0.93, "source": "unmarried"}
    if re.search(r"\b(married|विवाहित)\b", lower) or "विवाहित" in text:
        return {"value": "Married", "confidence": 0.95, "source": "married"}
    if re.search(r"\b(widow|widower|vidhava|विधवा)\b", lower) or "विधवा" in text:
        return {"value": "Widow / Widower", "confidence": 0.96, "source": "widow"}
    if re.search(r"\b(divorced|separated|घटस्फोटित)\b", lower) or "घटस्फोटित" in text:
        return {"value": "Divorced", "confidence": 0.94, "source": "divorced"}
    return None

def extract_disability(text: str) -> Optional[Dict[str, Any]]:
    lower = text.lower()
    if re.search(r"\b(handicapped|disabled|disability|divyang|pwd|दिव्यांग|अपंग)\b", lower) or "दिव्यांग" in text or "अपंग" in text:
        pct_match = re.search(r"(\d{1,3})%\s*(?:disability|disabled)?", lower)
        pct = f" ({pct_match.group(1)}%)" if pct_match else ""
        return {"value": f"Yes{pct}", "confidence": 0.92, "source": "disability/divyang"}
    return None

def extract_all_entities(text: str) -> Dict[str, Any]:
    cleaned = clean_text(text)
    entities: Dict[str, Any] = {}

    extractors = [
        ("fullName", extract_name),
        ("guardianName", extract_guardian_name),
        ("age", extract_age),
        ("dob", extract_dob),
        ("gender", extract_gender),
        ("education", extract_education),
        ("phone", extract_phone),
        ("aadhaar", extract_aadhaar),
        ("pan", extract_pan),
        ("email", extract_email),
        ("state", extract_state),
        ("district", extract_district),
        ("address", extract_address),
        ("pincode", extract_pincode),
        ("occupation", extract_occupation),
        ("annualIncome", extract_income),
        ("socialCategory", extract_category),
        ("landHolding", extract_land_holding),
        ("maritalStatus", extract_marital_status),
        ("disability", extract_disability)
    ]

    for key, fn in extractors:
        res = fn(cleaned)
        if res:
            entities[key] = res

    # Standardized Form Extraction Schema (null for missing as per Master Prompt requirement 7)
    structured_fields = {
        "full_name": entities.get("fullName", {}).get("value") if "fullName" in entities else None,
        "date_of_birth": entities.get("dob", {}).get("value") if "dob" in entities else None,
        "age": entities.get("age", {}).get("value") if "age" in entities else None,
        "gender": entities.get("gender", {}).get("value") if "gender" in entities else None,
        "education": entities.get("education", {}).get("value") if "education" in entities else None,
        "occupation": entities.get("occupation", {}).get("value") if "occupation" in entities else None,
        "annual_income": entities.get("annualIncome", {}).get("value") if "annualIncome" in entities else None,
        "address": entities.get("address", {}).get("value") if "address" in entities else None,
        "district": entities.get("district", {}).get("value") if "district" in entities else None,
        "state": entities.get("state", {}).get("value") if "state" in entities else None,
        "pincode": entities.get("pincode", {}).get("value") if "pincode" in entities else None,
        "phone": entities.get("phone", {}).get("value") if "phone" in entities else None,
        "aadhaar": entities.get("aadhaar", {}).get("value") if "aadhaar" in entities else None,
        "social_category": entities.get("socialCategory", {}).get("value") if "socialCategory" in entities else None
    }

    # Derive form intent if user mentions it
    intent = None
    lower = cleaned.lower()
    if "pm kisan" in lower or "kisan samman" in lower:
        intent = "pm_kisan"
    elif "income certificate" in lower or "aay praman" in lower or "utpann" in lower:
        intent = "income_certificate"
    elif "caste certificate" in lower or "jati praman" in lower or "jaaticha" in lower:
        intent = "caste_certificate"
    elif "domicile" in lower or "residence certificate" in lower or "adivas" in lower:
        intent = "domicile_certificate"
    elif "ayushman" in lower or "pm-jay" in lower or "health card" in lower:
        intent = "ayushman_bharat"
    elif "pension" in lower or "old age" in lower or "vriddhavastha" in lower:
        intent = "senior_pension"

    needs_confirmation = any(
        e.get("confidence", 1.0) < 0.85 for e in entities.values()
    ) or len(entities) < 2

    return {
        "raw_text": cleaned,
        "entities": entities,
        "entities_count": len(entities),
        "structured_fields": structured_fields,
        "needs_confirmation": needs_confirmation,
        "detected_intent": intent
    }
