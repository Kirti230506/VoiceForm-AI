from typing import Dict, Any, List, Optional

SCHEMES_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "pm_kisan",
        "title": "PM Kisan Samman Nidhi Yojana",
        "title_hi": "प्रधानमंत्री किसान सम्मान निधि योजना",
        "title_mr": "प्रधानमंत्री किसान सन्मान निधी योजना",
        "category": "Agriculture",
        "ministry": "Ministry of Agriculture & Farmers Welfare, Govt. of India",
        "description": "Financial support of ₹6,000 per year directly to bank accounts of landholding farmer families across the country.",
        "description_hi": "पात्र किसान परिवारों को प्रति वर्ष ₹6,000 की प्रत्यक्ष आर्थिक सहायता।",
        "description_mr": "शेतकरी कुटुंबांना दरवर्षी ₹6,000 ची थेट बँक खात्यात आर्थिक मदत.",
        "benefits": [
            "₹6,000 annual direct benefit transfer in 3 installments of ₹2,000 each",
            "100% central government funded with direct Aadhaar-NPCI credit",
            "Eligible for Kisan Credit Card (KCC) low-interest agricultural loans"
        ],
        "documents_required": [
            "Aadhaar Card of landholder",
            "Agricultural Land Record (7/12 Extract / Khatauni / Jamabandi)",
            "Aadhaar-seeded Bank Account Passbook",
            "Active Mobile Number linked with Aadhaar"
        ],
        "application_info": {
            "portal": "PM Kisan Official Portal (pmkisan.gov.in) or Nearest Common Service Center (CSC)",
            "url": "https://pmkisan.gov.in",
            "associated_form_id": "pm_kisan"
        },
        "rules": {
            "occupations": ["farmer", "kisan", "shetkari", "agriculture"],
            "min_age": 18,
            "max_age": 100,
            "requires_land": True,
            "max_income": 800000
        }
    },
    {
        "id": "ayushman_bharat",
        "title": "Ayushman Bharat PM-JAY Health Protection",
        "title_hi": "आयुष्मान भारत - प्रधानमंत्री जन आरोग्य योजना (PM-JAY)",
        "title_mr": "आयुष्मान भारत - प्रधानमंत्री जन आरोग्य योजना",
        "category": "Healthcare",
        "ministry": "National Health Authority, Ministry of Health & Family Welfare",
        "description": "World's largest government-funded healthcare assurance scheme offering ₹5 Lakh cover per family per year for secondary and tertiary care hospitalization.",
        "description_hi": "प्रति परिवार प्रति वर्ष ₹5 लाख का कैशलेस स्वास्थ्य सुरक्षा कवर।",
        "description_mr": "प्रति कुटुंब दरवर्षी ₹5 लाखांपर्यंतचे मोफत कॅशलेस आरोग्य संरक्षण.",
        "benefits": [
            "Cashless & paperless treatment up to ₹5,00,000 per family per year",
            "Covers 1,949 medical procedures including surgeries, ICU, oncology, and cardiac care",
            "Pre and post-hospitalization expenses covered for 3 and 15 days respectively",
            "Valid across all public and empaneled private hospitals throughout India"
        ],
        "documents_required": [
            "Aadhaar Card / Government Photo ID",
            "Ration Card (Priority / BPL / Antyodaya)",
            "Income Certificate or SECC verification slip",
            "Mobile Number for verification"
        ],
        "application_info": {
            "portal": "Ayushman Bharat PM-JAY Portal (beneficiary.nha.gov.in) or Empaneled Hospital Ayushman Mitra desk",
            "url": "https://beneficiary.nha.gov.in",
            "associated_form_id": "ayushman_bharat"
        },
        "rules": {
            "min_age": 0,
            "max_age": 120,
            "max_income": 300000,
            "target_categories": ["SC (Scheduled Caste)", "ST (Scheduled Tribe)", "OBC (Other Backward Class)", "EWS", "General / Open"]
        }
    },
    {
        "id": "pm_awas_yojana",
        "title": "Pradhan Mantri Awas Yojana (PMAY - Housing for All)",
        "title_hi": "प्रधानमंत्री आवास योजना (PMAY)",
        "title_mr": "प्रधानमंत्री आवास योजना (सर्वांसाठी घरे)",
        "category": "Housing",
        "ministry": "Ministry of Housing & Urban Affairs / Rural Development",
        "description": "Financial assistance to poor and middle-income families to construct or purchase their first permanent pucca house with basic amenities.",
        "description_hi": "बेघर या कच्चे मकान वाले परिवारों को पक्का मकान बनाने हेतु आर्थिक सहायता।",
        "description_mr": "बेघर व कच्च्या घरात राहणाऱ्या कुटुंबांना पक्के घर बांधण्यासाठी आर्थिक अनुदान.",
        "benefits": [
            "Direct subsidy of ₹1,20,000 (Plains) to ₹1,30,000 (Hilly states) in rural areas",
            "Interest subsidy up to ₹2.67 Lakh for Credit Linked Subsidy Scheme (CLSS) in urban areas",
            "Additional 90 days of unskilled wage under MGNREGA for house construction",
            "Direct grant for toilet construction under Swachh Bharat Mission"
        ],
        "documents_required": [
            "Aadhaar Card of all family members",
            "Income Certificate issued by Tahsildar",
            "Proof of Land / Plot ownership or certificate of no existing pucca house",
            "Bank Account Passbook with IFSC",
            "Job Card / Ration Card"
        ],
        "application_info": {
            "portal": "PMAY-Gramin / Urban Portal or Gram Panchayat / Municipal Ward Office",
            "url": "https://pmaymis.gov.in",
            "associated_form_id": "income_certificate"
        },
        "rules": {
            "min_age": 18,
            "max_age": 100,
            "max_income": 300000
        }
    },
    {
        "id": "post_matric_scholarship",
        "title": "Post-Matric Scholarship for SC/ST/OBC Students",
        "title_hi": "एससी/एसटी/ओबीसी छात्रों के लिए पोस्ट-मैट्रिक छात्रवृत्ति",
        "title_mr": "मागासवर्गीय विद्यार्थ्यांसाठी मॅट्रिकोत्तर शिष्यवृत्ती",
        "category": "Education",
        "ministry": "Ministry of Social Justice & Empowerment",
        "description": "Full tuition fee waiver and maintenance allowances for meritorious and deserving backward category students pursuing higher education.",
        "description_hi": "कॉलेज और उच्च शिक्षा के लिए संपूर्ण शिक्षण शुल्क प्रतिपूर्ति एवं छात्रवृत्ति।",
        "description_mr": "महाविद्यालयीन उच्च शिक्षणासाठी संपूर्ण शिक्षण शुल्क प्रतिपूर्ती व निर्वाह भत्ता.",
        "benefits": [
            "100% reimbursement of tuition fees and exam fees in government & recognized colleges",
            "Monthly maintenance allowance up to ₹1,200/month for day scholars and ₹2,500/month for hostellers",
            "Book grant and study tour assistance for professional degree courses"
        ],
        "documents_required": [
            "Caste Certificate & Caste Validity Certificate",
            "Current Year Family Income Certificate (below ₹2.5 Lakh for SC/ST, below ₹1.5 Lakh for OBC)",
            "10th & 12th Marksheets",
            "College Admission Receipt & Fee Structure",
            "Domicile Certificate of State",
            "Aadhaar Card & Bank Passbook"
        ],
        "application_info": {
            "portal": "National Scholarship Portal (scholarships.gov.in) or State MahaDBT portal",
            "url": "https://scholarships.gov.in",
            "associated_form_id": "caste_certificate"
        },
        "rules": {
            "min_age": 15,
            "max_age": 35,
            "occupations": ["student", "studying"],
            "target_categories": ["SC (Scheduled Caste)", "ST (Scheduled Tribe)", "OBC (Other Backward Class)", "EWS"],
            "max_income": 250000
        }
    },
    {
        "id": "pm_ujjwala",
        "title": "Pradhan Mantri Ujjwala Yojana 2.0 (LPG Connection)",
        "title_hi": "प्रधानमंत्री उज्ज्वला योजना 2.0 (मुफ्त गैस कनेक्शन)",
        "title_mr": "प्रधानमंत्री उज्ज्वला योजना (मोफत गॅस कनेक्शन)",
        "category": "Women & Child Welfare",
        "ministry": "Ministry of Petroleum & Natural Gas",
        "description": "Deposit-free LPG connection to adult women belonging to poor households with free first refill cylinder and stove.",
        "description_hi": "गरीब परिवारों की वयस्क महिलाओं को मुफ्त एलपीजी गैस कनेक्शन और चूल्हा।",
        "description_mr": "दारिद्र्यरेषेखालील कुटुंबांतील महिलांना मोफत गॅस जोडणी व शेगडी.",
        "benefits": [
            "Free LPG cylinder connection with zero security deposit",
            "First refill cylinder provided 100% free of cost",
            "Free double-burner LPG gas stove provided at time of installation",
            "Ongoing targeted subsidy of ₹300 per refill directly credited to bank account"
        ],
        "documents_required": [
            "Aadhaar Card of female head of the family",
            "BPL Ration Card containing all family members' names",
            "Bank Account Details (Aadhaar linked)",
            "Declaration of no existing LPG connection in the household"
        ],
        "application_info": {
            "portal": "PM Ujjwala Portal (pmuy.gov.in) or nearest Indane / Bharat Gas / HP Gas distributor",
            "url": "https://www.pmuy.gov.in",
            "associated_form_id": "income_certificate"
        },
        "rules": {
            "min_age": 18,
            "gender": "Female",
            "max_income": 200000
        }
    },
    {
        "id": "senior_pension_scheme",
        "title": "Indira Gandhi National Old Age Pension Scheme (IGNOAPS)",
        "title_hi": "इंदिरा गांधी राष्ट्रीय वृद्धावस्था पेंशन योजना",
        "title_mr": "इंदिरा गांधी राष्ट्रीय वृद्धापकाळ निवृत्तीवेतन योजना",
        "category": "Social Welfare & Pensions",
        "ministry": "Ministry of Rural Development, Govt. of India",
        "description": "Monthly social security pension for impoverished senior citizens living below the poverty line with no regular support.",
        "description_hi": "60 वर्ष से अधिक आयु के बीपीएल बुजुर्गों को मासिक आर्थिक पेंशन सहायता।",
        "description_mr": "६० वर्षांवरील दारिद्र्यरेषेखालील वृद्ध नागरिकांना दरमहा आर्थिक पेन्शन.",
        "benefits": [
            "Monthly pension of ₹1,000 to ₹1,500 transferred directly into pensioner bank account",
            "Increased benefit of ₹2,000/month for super-seniors aged 80 and above",
            "Zero deduction, lifetime social security guarantee"
        ],
        "documents_required": [
            "Age Proof (Aadhaar Card / Voter ID / Birth Certificate showing age 60+)",
            "BPL Card / Antyodaya Ration Card",
            "Income Certificate showing BPL status",
            "Bank Passbook linked with Aadhaar",
            "Passport-size Photographs"
        ],
        "application_info": {
            "portal": "National Social Assistance Programme (nsap.nic.in) or Tahsil Office",
            "url": "https://nsap.nic.in",
            "associated_form_id": "senior_pension"
        },
        "rules": {
            "min_age": 60,
            "max_age": 120,
            "max_income": 100000
        }
    },
    {
        "id": "pm_mudra_yojana",
        "title": "Pradhan Mantri MUDRA Yojana (PMMY Small Business Loan)",
        "title_hi": "प्रधानमंत्री मुद्रा योजना (सूक्ष्म व्यवसाय ऋण)",
        "title_mr": "प्रधानमंत्री मुद्रा योजना (लघु व्यवसाय कर्ज)",
        "category": "Employment & Entrepreneurship",
        "ministry": "Department of Financial Services, Ministry of Finance",
        "description": "Collateral-free institutional loans up to ₹10 Lakh to micro and small non-farm enterprises, shopkeepers, fruit vendors, artisans, and transport operators.",
        "description_hi": "छोटे दुकानदारों और कारीगरों के लिए ₹10 लाख तक का बिना गारंटी बैंक लोन।",
        "description_mr": "लघु व्यावसायिक व कारागिरांसाठी १० लाख रुपयांपर्यंतचे विनातारण कर्ज.",
        "benefits": [
            "Three loan tiers: Shishu (up to ₹50,000), Kishore (₹50,000 to ₹5 Lakh), Tarun (₹5 Lakh to ₹10 Lakh)",
            "No collateral security or third-party guarantee required",
            "Nominal interest rates with MUDRA debit card for working capital overdraft",
            "Zero processing fee for Shishu and Kishore loans"
        ],
        "documents_required": [
            "Aadhaar Card & PAN Card",
            "Business establishment proof or Trade License / Udyam Registration",
            "Last 6 months Bank Statement",
            "Quotation of machinery/items to be purchased or working capital estimate"
        ],
        "application_info": {
            "portal": "UdyamiMitra Portal (udyamimitra.in) or any Public/Private Sector Bank",
            "url": "https://www.mudra.org.in",
            "associated_form_id": "income_certificate"
        },
        "rules": {
            "min_age": 18,
            "max_age": 65,
            "occupations": ["small business", "business", "shopkeeper", "artisan", "driver", "carpenter", "electrician", "self-employed"]
        }
    },
    {
        "id": "sukanya_samriddhi",
        "title": "Sukanya Samriddhi Yojana (Beti Bachao Beti Padhao)",
        "title_hi": "सुकन्या समृद्धि योजना (बालिका समृद्धि खाता)",
        "title_mr": "सुकन्या समृद्धी योजना (मुलींचे भविष्य सुरक्षित करणारी योजना)",
        "category": "Women & Child Welfare",
        "ministry": "Ministry of Finance & Ministry of Women and Child Development",
        "description": "Small-deposit savings scheme backed by Govt. of India for the girl child, offering maximum tax-exempt returns for higher education and marriage.",
        "description_hi": "बालिकाओं के उज्ज्वल भविष्य व उच्च शिक्षा हेतु सरकार समर्थित उच्च ब्याज दर बचत खाता।",
        "description_mr": "मुलींच्या उच्च शिक्षण व विवाहासाठी सर्वोच्च व्याज देणारी सरकारी बचत योजना.",
        "benefits": [
            "High sovereign guaranteed interest rate of 8.2% per annum (compounded annually)",
            "Triple Tax Exemption under Section 80C (Exempt-Exempt-Exempt)",
            "Can be opened with as little as ₹250 initial deposit",
            "Partial withdrawal allowed up to 50% for girl's higher education after age 18"
        ],
        "documents_required": [
            "Birth Certificate of girl child",
            "Aadhaar Card and PAN of Parent / Legal Guardian",
            "Address Proof of Parent",
            "Recent Photographs"
        ],
        "application_info": {
            "portal": "Any Post Office or Commercial Bank branch across India",
            "url": "https://www.indiapost.gov.in",
            "associated_form_id": "domicile_certificate"
        },
        "rules": {
            "min_age": 0,
            "max_age": 10,
            "gender": "Female"
        }
    }
]

DISCLAIMER_TEXT = (
    "AI-Based Preliminary Eligibility Check: The recommendations displayed here are computed based on "
    "the information provided by you and standard government scheme criteria. This is NOT an official government "
    "decision or guarantee of approval. Actual benefits require formal application and verification by authorized "
    "government authorities with original documents."
)

def evaluate_scheme_eligibility(user_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates user profile against stored rules and returns recommended schemes,
    eligibility status, unmet criteria, benefits, and required documents.
    """
    age = user_profile.get("age")
    gender = user_profile.get("gender")
    income = user_profile.get("annualIncome")
    if isinstance(income, dict):
        income = income.get("value")
    occupation = str(user_profile.get("occupation") or "").lower()
    category = str(user_profile.get("socialCategory") or "").lower()
    state = user_profile.get("state")
    land = user_profile.get("landHolding")

    matched_schemes = []

    for scheme in SCHEMES_CATALOG:
        rules = scheme.get("rules", {})
        score = 100
        reasons_eligible = []
        criteria_unmet = []

        # 1. Age check
        min_age = rules.get("min_age")
        max_age = rules.get("max_age")
        if age is not None:
            if min_age is not None and age < min_age:
                score -= 40
                criteria_unmet.append(f"Age {age} is below minimum requirement of {min_age} years")
            elif max_age is not None and age > max_age:
                score -= 40
                criteria_unmet.append(f"Age {age} exceeds maximum limit of {max_age} years")
            else:
                reasons_eligible.append(f"Age ({age} yrs) satisfies scheme age criteria")

        # 2. Gender check
        rule_gender = rules.get("gender")
        if rule_gender and gender:
            if rule_gender.lower() != str(gender).lower():
                score -= 45
                criteria_unmet.append(f"Scheme is designated exclusively for {rule_gender} applicants")
            else:
                reasons_eligible.append(f"Gender ({gender}) matches scheme target group")

        # 3. Income check
        max_income = rules.get("max_income")
        if max_income is not None and income is not None:
            if income > max_income:
                score -= 35
                criteria_unmet.append(f"Annual income (₹{income:,}) exceeds ceiling limit of ₹{max_income:,}")
            else:
                reasons_eligible.append(f"Annual income (₹{income:,}) is well within eligible limit of ₹{max_income:,}")

        # 4. Occupation check
        allowed_occupations = rules.get("occupations")
        if allowed_occupations and occupation:
            matches_occ = any(occ in occupation for occ in allowed_occupations)
            if matches_occ:
                score += 10
                reasons_eligible.append(f"Occupation matches target beneficiary profile")
            else:
                score -= 25
                criteria_unmet.append(f"Scheme targets specific occupations: {', '.join(allowed_occupations)}")

        # 5. Land check
        if rules.get("requires_land"):
            if land or "farmer" in occupation or "kisan" in occupation or "shetkari" in occupation:
                reasons_eligible.append("Landholding farmer criterion satisfied")
            else:
                score -= 25
                criteria_unmet.append("Requires cultivable agricultural landholding")

        # Normalize score
        score = max(0, min(100, score))
        
        status = "Highly Eligible" if score >= 80 else ("Likely Eligible" if score >= 60 else "Not Eligible")

        matched_schemes.append({
            "scheme_id": scheme["id"],
            "title": scheme["title"],
            "title_hi": scheme["title_hi"],
            "title_mr": scheme["title_mr"],
            "category": scheme["category"],
            "ministry": scheme["ministry"],
            "description": scheme["description"],
            "description_hi": scheme["description_hi"],
            "description_mr": scheme["description_mr"],
            "eligibility_score": score,
            "status": status,
            "reasons_eligible": reasons_eligible,
            "criteria_unmet": criteria_unmet,
            "benefits": scheme["benefits"],
            "documents_required": scheme["documents_required"],
            "application_info": scheme["application_info"]
        })

    # Sort schemes by eligibility score descending
    matched_schemes.sort(key=lambda s: s["eligibility_score"], reverse=True)

    eligible_count = sum(1 for s in matched_schemes if s["status"] in ["Highly Eligible", "Likely Eligible"])

    return {
        "user_profile_summary": {
            "age": age,
            "gender": gender,
            "income": income,
            "occupation": occupation,
            "category": category,
            "state": state
        },
        "total_schemes_analyzed": len(SCHEMES_CATALOG),
        "eligible_schemes_count": eligible_count,
        "recommended_schemes": matched_schemes,
        "disclaimer": DISCLAIMER_TEXT
    }
