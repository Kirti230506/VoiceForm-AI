import re
from typing import Dict, Any, List, Optional

FIELD_EXPLANATIONS = {
    "applicant_name": {
        "en": "Enter your full legal name as it appears on official government identity proofs like Aadhaar or PAN card. Do not use nicknames or abbreviations.",
        "hi": "अपना पूरा नाम वही दर्ज करें जो आपके आधार कार्ड या स्कूल छोड़ने के प्रमाण पत्र पर लिखा है। उपनाम या संक्षिप्त नाम न लिखें।",
        "mr": "तुमचे पूर्ण कायदेशीर नाव आधार कार्ड किंवा शाळा सोडल्याच्या दाखल्यावर असल्याप्रमाणेच लिहा. टोपणनाव वापरू नका.",
        "example": "e.g. Ramesh Shankar Patil (First Name, Father's Name, Surname)"
    },
    "aadhaar_number": {
        "en": "Your 12-digit Unique Identification Number issued by UIDAI. It is used to verify your identity and credit subsidies directly to your bank account via DBT.",
        "hi": "यूआईडीएआई द्वारा जारी 12 अंकों का विशिष्ट पहचान नंबर। इसका उपयोग आपकी पहचान सत्यापित करने और सरकारी लाभ सीधे बैंक खाते में भेजने के लिए होता है।",
        "mr": "UIDAI ने दिलेला १२ अंकी आधार क्रमांक. थेट बँक खात्यात सरकारी अनुदान जमा करण्यासाठी हा आवश्यक आहे.",
        "example": "e.g. 5432 8765 1290 (12 digits)"
    },
    "annual_income": {
        "en": "Total combined gross income earned by all family members in your household from all sources (farming, salary, daily wages, small business, rent) in the last financial year.",
        "hi": "पिछले वित्तीय वर्ष में आपके परिवार के सभी सदस्यों द्वारा सभी स्रोतों (खेती, मजदूरी, व्यापार, नौकरी) से अर्जित कुल वार्षिक आय।",
        "mr": "गेल्या आर्थिक वर्षात घरातील सर्व सदस्यांना शेती, नोकरी, मजुरी किंवा व्यवसायातून मिळालेले एकूण वार्षिक उत्पन्न.",
        "example": "e.g. ₹1,20,000 (If monthly family earning is ₹10,000)"
    },
    "social_category": {
        "en": "Your constitutional social category recognized by the Government for affirmative action, reservations, and welfare benefits (General/Open, OBC, SC, ST, EWS).",
        "hi": "सरकारी योजनाओं और आरक्षण के लिए सरकार द्वारा मान्यता प्राप्त आपका वर्ग (सामान्य, ओबीसी, एससी, एसटी, ईडब्ल्यूएस)।",
        "mr": "आरक्षण आणि कल्याणकारी योजनांसाठी मान्यताप्राप्त सामाजिक प्रवर्ग (खुला/General, OBC, SC, ST, EWS).",
        "example": "Select your category as mentioned in your Caste Certificate or School Leaving Certificate."
    },
    "land_area": {
        "en": "The total area of agricultural cultivable land owned by you or your family, typically recorded in Acres or Hectares in your 7/12 extract or Khatauni.",
        "hi": "आपके नाम पर दर्ज कुल कृषि भूमि का क्षेत्रफल (एकड़ या हेक्टेयर में), जो आपके खतौनी या 7/12 नकल में दर्ज है।",
        "mr": "तुमच्या किंवा कुटुंबाच्या नावावर असणारी एकूण शेती जमीन (एकर किंवा हेक्टरमध्ये), जी ७/१२ उताऱ्यामध्ये नमूद आहे.",
        "example": "e.g. 2.5 Acres or 1 Hectare"
    },
    "years_in_state": {
        "en": "The continuous number of years you have been residing in this state. Most state government certificates require a minimum of 15 years continuous domicile.",
        "hi": "आप इस राज्य में कितने वर्षों से लगातार रह रहे हैं। अधिवास प्रमाण पत्र के लिए कम से कम 15 वर्ष का निरंतर निवास आवश्यक है।",
        "mr": "तुम्ही या राज्यात सलग किती वर्षांपासून वास्तव्य करत आहात. अधिवास दाखल्यासाठी किमान १५ वर्षांचे वास्तव्य आवश्यक असते.",
        "example": "e.g. 22 Years (Continuous residence)"
    },
    "bank_ifsc": {
        "en": "An 11-character alphanumeric code identifying your specific bank branch. It is printed on the front page of your bank passbook and cheque leaf.",
        "hi": "आपकी बैंक शाखा का 11 अक्षरों का विशिष्ट कोड। यह बैंक पासबुक के पहले पन्ने या चेक पर छपा होता है।",
        "mr": "तुमच्या बँक शाखेचा ११ अंकी सांकेतांक. हा बँक पासबुकच्या पहिल्या पानावर किंवा धनादेशावर लिहिलेला असतो.",
        "example": "e.g. SBIN0001234 (First 4 letters bank, 5th character '0', last 6 branch)"
    }
}

FAQ_KNOWLEDGE_BASE = [
    {
        "keywords": ["income certificate", "validity", "expire"],
        "answer_en": "An Income Certificate issued by the Tahsildar is typically valid for 1 financial year or 3 financial years depending on your state regulations.",
        "answer_hi": "तहसीलदार द्वारा जारी आय प्रमाण पत्र आमतौर पर 1 या 3 वित्तीय वर्षों के लिए मान्य होता है।",
        "answer_mr": "तहसीलदारांनी दिलेला उत्पन्न दाखला सहसा १ आर्थिक वर्ष किंवा ३ आर्थिक वर्षांसाठी वैध असतो."
    },
    {
        "keywords": ["pm kisan", "amount", "installment", "money"],
        "answer_en": "Under PM Kisan Samman Nidhi, eligible farmer families receive ₹6,000 every year in 3 installments of ₹2,000 every four months directly into their Aadhaar-linked bank accounts.",
        "answer_hi": "पीएम किसान सम्मान निधि के तहत पात्र किसानों को हर 4 महीने में ₹2,000 की 3 किस्तों में कुल ₹6,000 प्रति वर्ष मिलते हैं।",
        "answer_mr": "पीएम किसान सन्मान निधी अंतर्गत शेतकऱ्यांना दर चार महिन्यांनी ₹२,००० याप्रमाणे वर्षाला एकूण ₹६,००० थेट बँक खात्यात मिळतात."
    },
    {
        "keywords": ["ayushman", "limit", "hospital", "coverage"],
        "answer_en": "Ayushman Bharat PM-JAY provides up to ₹5 Lakh per family per year for secondary and tertiary care hospitalization in any empaneled government or private hospital across India.",
        "answer_hi": "आयुष्मान भारत योजना प्रति परिवार प्रति वर्ष ₹5 लाख तक का कैशलेस अस्पताल उपचार प्रदान करती है।",
        "answer_mr": "आयुष्मान भारत योजनेतून प्रति कुटुंब दरवर्षी ₹५ लाखांपर्यंतचे मोफत कॅशलेस उपचार मिळतात."
    },
    {
        "keywords": ["documents", "caste certificate", "require"],
        "answer_en": "To apply for a Caste Certificate, you need: 1. Father's / Grandfather's school leaving certificate with caste mention, 2. Aadhaar Card, 3. Ration Card, 4. 15-year domicile proof, 5. Affidavit.",
        "answer_hi": "जाति प्रमाण पत्र के लिए आवश्यक दस्तावेज: 1. पिता या दादाजी का स्कूल छोड़ने का प्रमाण पत्र (जाति उल्लेख सहित), 2. आधार कार्ड, 3. राशन कार्ड, 4. 15 वर्ष का निवास प्रमाण।",
        "answer_mr": "जात प्रमाणपत्रासाठी आवश्यक कागदपत्रे: १. वडील/आजोबांचा शाळा सोडल्याचा दाखला (जात नोंदीसह), २. आधार कार्ड, ३. रेशन कार्ड, ४. १५ वर्षांचा रहिवासी दाखला."
    }
]

def explain_field(field_id: str, lang: str = "en") -> Dict[str, Any]:
    info = FIELD_EXPLANATIONS.get(field_id)
    if not info:
        return {
            "field_id": field_id,
            "explanation": f"Please enter accurate information for {field_id.replace('_', ' ').title()}.",
            "example": "Refer to your official identification documents."
        }
    return {
        "field_id": field_id,
        "explanation": info.get(lang, info.get("en")),
        "example": info.get("example", "")
    }

def validate_form_data(form_id: str, form_data: Dict[str, Any], form_def: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates entered data, flags missing required fields, formats, and returns helpful AI suggestions.
    """
    missing_fields = []
    format_warnings = []
    suggestions = []

    for section in form_def.get("sections", []):
        for field in section.get("fields", []):
            fid = field["id"]
            val = form_data.get(fid)

            # Check required
            if field.get("required") and (val is None or str(val).strip() == ""):
                missing_fields.append({
                    "field_id": fid,
                    "field_label": field["label"],
                    "section_title": section["title"],
                    "help": field.get("help", "This field is mandatory.")
                })

            # Check format rules if present
            if val is not None and str(val).strip() != "":
                str_val = str(val).strip()
                if fid == "aadhaar_number":
                    clean = re.sub(r"[\s-]", "", str_val)
                    if len(clean) != 12 or not clean.isdigit():
                        format_warnings.append({
                            "field_id": fid,
                            "field_label": field["label"],
                            "message": "Aadhaar number must contain exactly 12 digits."
                        })
                elif fid == "mobile_number":
                    clean = re.sub(r"[\s-]", "", str_val)
                    if len(clean) != 10 or not clean.isdigit():
                        format_warnings.append({
                            "field_id": fid,
                            "field_label": field["label"],
                            "message": "Mobile number must be a valid 10-digit number."
                        })
                elif fid == "applicant_age":
                    try:
                        age_int = int(str_val)
                        if form_id == "senior_pension" and age_int < 60:
                            format_warnings.append({
                                "field_id": fid,
                                "field_label": field["label"],
                                "message": "Senior Citizen Pension requires applicant age to be 60 or older."
                            })
                    except ValueError:
                        pass

    # Generate friendly AI feedback
    if missing_fields:
        suggestions.append(f"You have {len(missing_fields)} required fields left to complete. You can speak them using the microphone!")
    else:
        suggestions.append("Great job! All mandatory fields are completed. Please review and verify before submitting.")

    return {
        "is_valid": len(missing_fields) == 0 and len(format_warnings) == 0,
        "missing_fields": missing_fields,
        "format_warnings": format_warnings,
        "suggestions": suggestions
    }

def answer_query(query: str, lang: str = "en") -> Dict[str, Any]:
    cleaned = query.lower()
    for item in FAQ_KNOWLEDGE_BASE:
        if any(kw in cleaned for kw in item["keywords"]):
            ans_key = f"answer_{lang}" if f"answer_{lang}" in item else "answer_en"
            return {
                "query": query,
                "answer": item[ans_key],
                "matched": True
            }
    
    # Generic helpful response
    fallbacks = {
        "en": "VoiceForm AI is here to assist you! You can speak your personal details into the microphone, and the AI will automatically fill your government form and verify your scheme eligibility.",
        "hi": "वॉइसफॉर्म एआई आपकी सहायता के लिए तैयार है! आप माइक्रोफ़ोन में अपनी जानकारी बोल सकते हैं, और एआई आपके फॉर्म को स्वतः भर देगा।",
        "mr": "व्हॉइसफॉर्म एआय तुमच्या मदतीसाठी तयार आहे! तुम्ही मायक्रोफोनमध्ये तुमची माहिती बोलू शकता आणि एआय तुमचा अर्ज आपोआप भरेल."
    }
    return {
        "query": query,
        "answer": fallbacks.get(lang, fallbacks["en"]),
        "matched": False
    }
