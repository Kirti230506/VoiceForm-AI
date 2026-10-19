from typing import Dict, Any, List, Optional

GOVERNMENT_FORMS: List[Dict[str, Any]] = [
    {
        "id": "income_certificate",
        "title": "Application for Income Certificate",
        "title_hi": "आय प्रमाण पत्र के लिए आवेदन",
        "title_mr": "उत्पन्न दाखल्यासाठी अर्ज",
        "department": "Revenue & Land Reforms Department",
        "category": "Certificates",
        "processing_days": "7-15 Days",
        "fee": "₹25 - ₹50 (Nominal CSC Fee)",
        "description": "Official proof of annual household income issued by the Tahsildar / Sub-Divisional Magistrate for scholarships, fee concessions, and government welfare benefits.",
        "description_hi": "तहसीलदार द्वारा जारी किया जाने वाला आधिकारिक पारिवारिक आय प्रमाण पत्र, छात्रवृत्ति और योजनाओं के लिए आवश्यक।",
        "description_mr": "तहसीलदारांमार्फत वितरित केले जाणारे वार्षिक उत्पन्न प्रमाणपत्र, शिष्यवृत्ती व योजनांसाठी अत्यावश्यक.",
        "sections": [
            {
                "section_id": "personal",
                "title": "Personal Details",
                "title_hi": "व्यक्तिगत विवरण",
                "title_mr": "वैयक्तिक तपशील",
                "fields": [
                    {
                        "id": "applicant_name",
                        "label": "Full Name of Applicant",
                        "label_hi": "आवेदक का पूरा नाम",
                        "label_mr": "अर्जदाराचे पूर्ण नाव",
                        "type": "text",
                        "placeholder": "e.g. Ramesh Shankar Patil",
                        "required": True,
                        "entity_key": "fullName",
                        "help": "Enter full name exactly as printed on your Aadhaar card or School Leaving Certificate."
                    },
                    {
                        "id": "applicant_age",
                        "label": "Age",
                        "label_hi": "आयु (वर्ष)",
                        "label_mr": "वय (वर्षे)",
                        "type": "number",
                        "placeholder": "e.g. 42",
                        "required": True,
                        "entity_key": "age",
                        "help": "Your completed age in years as of today."
                    },
                    {
                        "id": "applicant_gender",
                        "label": "Gender",
                        "label_hi": "लिंग",
                        "label_mr": "लिंग",
                        "type": "select",
                        "options": ["Male", "Female", "Transgender", "Other"],
                        "required": True,
                        "entity_key": "gender",
                        "help": "Select your gender."
                    },
                    {
                        "id": "aadhaar_number",
                        "label": "Aadhaar Number",
                        "label_hi": "आधार कार्ड नंबर",
                        "label_mr": "आधार क्रमांक",
                        "type": "text",
                        "placeholder": "XXXX XXXX XXXX",
                        "required": True,
                        "entity_key": "aadhaar",
                        "help": "12-digit Unique Identification Number printed on Aadhaar card."
                    },
                    {
                        "id": "father_husband_name",
                        "label": "Father's / Husband's Full Name",
                        "label_hi": "पिता / पति का नाम",
                        "label_mr": "वडील / पतीचे नाव",
                        "type": "text",
                        "placeholder": "e.g. Shankar Patil",
                        "required": True,
                        "entity_key": "guardianName",
                        "help": "Full name of the head of the family or father/husband."
                    }
                ]
            },
            {
                "section_id": "contact_address",
                "title": "Contact & Residential Address",
                "title_hi": "संपर्क और आवासीय पता",
                "title_mr": "संपर्क व रहिवासी पत्ता",
                "fields": [
                    {
                        "id": "mobile_number",
                        "label": "Mobile Number",
                        "label_hi": "मोबाइल नंबर",
                        "label_mr": "मोबाईल नंबर",
                        "type": "tel",
                        "placeholder": "9876543210",
                        "required": True,
                        "entity_key": "phone",
                        "help": "10-digit mobile number linked with Aadhaar for receiving OTP and status SMS."
                    },
                    {
                        "id": "email_address",
                        "label": "Email Address (Optional)",
                        "label_hi": "ईमेल पता (वैकल्पिक)",
                        "label_mr": "ईमेल पत्ता (ऐच्छिक)",
                        "type": "email",
                        "placeholder": "applicant@example.com",
                        "required": False,
                        "entity_key": "email",
                        "help": "Your email for digital certificate dispatch."
                    },
                    {
                        "id": "residential_address",
                        "label": "Permanent Address / House No.",
                        "label_hi": "स्थायी पता / मकान संख्या",
                        "label_mr": "कायमचा पत्ता / घर क्रमांक",
                        "type": "textarea",
                        "placeholder": "House No, Street, Village or Colony",
                        "required": True,
                        "entity_key": "address",
                        "help": "Full permanent address as per electricity bill or ration card."
                    },
                    {
                        "id": "district",
                        "label": "District",
                        "label_hi": "जिला",
                        "label_mr": "जिल्हा",
                        "type": "text",
                        "placeholder": "e.g. Pune",
                        "required": True,
                        "entity_key": "district",
                        "help": "Your administrative revenue district."
                    },
                    {
                        "id": "state",
                        "label": "State / UT",
                        "label_hi": "राज्य / केंद्रशासित प्रदेश",
                        "label_mr": "राज्य",
                        "type": "text",
                        "placeholder": "e.g. Maharashtra",
                        "required": True,
                        "entity_key": "state",
                        "help": "State in which your domicile is situated."
                    },
                    {
                        "id": "pincode",
                        "label": "PIN Code",
                        "label_hi": "पिन कोड",
                        "label_mr": "पिन कोड",
                        "type": "text",
                        "placeholder": "e.g. 411001",
                        "required": True,
                        "entity_key": "pincode",
                        "help": "6-digit postal index number."
                    }
                ]
            },
            {
                "section_id": "socio_economic",
                "title": "Income & Occupation Details",
                "title_hi": "आय और व्यवसाय विवरण",
                "title_mr": "उत्पन्न व व्यवसाय तपशील",
                "fields": [
                    {
                        "id": "applicant_occupation",
                        "label": "Primary Occupation",
                        "label_hi": "मुख्य व्यवसाय",
                        "label_mr": "मुख्य व्यवसाय",
                        "type": "text",
                        "placeholder": "Farmer / Laborer / Small Business / Teacher",
                        "required": True,
                        "entity_key": "occupation",
                        "help": "Primary means of livelihood of the main earner."
                    },
                    {
                        "id": "annual_income",
                        "label": "Total Annual Family Income (in ₹)",
                        "label_hi": "कुल वार्षिक पारिवारिक आय (₹ में)",
                        "label_mr": "एकूण वार्षिक कौटुंबिक उत्पन्न (₹)",
                        "type": "number",
                        "placeholder": "e.g. 150000",
                        "required": True,
                        "entity_key": "annualIncome",
                        "help": "Combined yearly income of all family members from all sources (agriculture, salary, business)."
                    },
                    {
                        "id": "income_purpose",
                        "label": "Purpose of Certificate",
                        "label_hi": "प्रमाण पत्र का उद्देश्य",
                        "label_mr": "प्रमाणपत्राचा हेतू",
                        "type": "select",
                        "options": ["Scholarship / Education", "Government Welfare Scheme", "Ration Card Application", "Fee Concession", "Court / Official Work", "Other"],
                        "required": True,
                        "help": "Select why you require this income certificate."
                    },
                    {
                        "id": "social_category",
                        "label": "Social Category / Caste",
                        "label_hi": "सामाजिक श्रेणी / वर्ग",
                        "label_mr": "सामाजिक प्रवर्ग / जात",
                        "type": "select",
                        "options": ["General / Open", "OBC (Other Backward Class)", "SC (Scheduled Caste)", "ST (Scheduled Tribe)", "EWS", "Minority"],
                        "required": True,
                        "entity_key": "socialCategory",
                        "help": "Your constitutional social category as recognized by state government."
                    }
                ]
            }
        ]
    },
    {
        "id": "pm_kisan",
        "title": "PM Kisan Samman Nidhi Registration",
        "title_hi": "प्रधानमंत्री किसान सम्मान निधि पंजीकरण",
        "title_mr": "प्रधानमंत्री किसान सन्मान निधी नोंदणी",
        "department": "Ministry of Agriculture & Farmers Welfare",
        "category": "Agriculture & Welfare",
        "processing_days": "15-30 Days",
        "fee": "Free of Cost (Direct Benefit Transfer)",
        "description": "Financial benefit of ₹6,000 per year in three equal installments of ₹2,000 transferred directly into bank accounts of eligible landholding farmer families.",
        "description_hi": "पात्र किसान परिवारों को प्रति वर्ष ₹6,000 की वित्तीय सहायता सीधे बैंक खाते में।",
        "description_mr": "पात्र शेतकरी कुटुंबांना दरवर्षी ₹6,000 ची थेट बँक खात्यात आर्थिक मदत.",
        "sections": [
            {
                "section_id": "farmer_identity",
                "title": "Farmer Identity & Demographics",
                "title_hi": "किसान पहचान एवं विवरण",
                "title_mr": "शेतकरी ओळख व तपशील",
                "fields": [
                    {
                        "id": "applicant_name",
                        "label": "Farmer Full Name (as per Aadhaar)",
                        "label_hi": "किसान का पूरा नाम (आधार अनुसार)",
                        "label_mr": "शेतकऱ्याचे नाव (आधारप्रमाणे)",
                        "type": "text",
                        "placeholder": "e.g. Ramesh Shankar Patil",
                        "required": True,
                        "entity_key": "fullName",
                        "help": "Must match letter-for-letter with your Aadhaar card."
                    },
                    {
                        "id": "applicant_gender",
                        "label": "Gender",
                        "label_hi": "लिंग",
                        "label_mr": "लिंग",
                        "type": "select",
                        "options": ["Male", "Female", "Other"],
                        "required": True,
                        "entity_key": "gender",
                        "help": "Gender of the landholder."
                    },
                    {
                        "id": "social_category",
                        "label": "Farmer Category",
                        "label_hi": "किसान श्रेणी",
                        "label_mr": "शेतकरी प्रवर्ग",
                        "type": "select",
                        "options": ["General / Open", "OBC", "SC", "ST"],
                        "required": True,
                        "entity_key": "socialCategory",
                        "help": "Caste category for welfare statistics."
                    },
                    {
                        "id": "aadhaar_number",
                        "label": "Aadhaar Number",
                        "label_hi": "आधार नंबर",
                        "label_mr": "आधार क्रमांक",
                        "type": "text",
                        "placeholder": "XXXX XXXX XXXX",
                        "required": True,
                        "entity_key": "aadhaar",
                        "help": "Mandatory 12-digit Aadhaar linked with NPCI bank account."
                    },
                    {
                        "id": "mobile_number",
                        "label": "Mobile Number",
                        "label_hi": "मोबाइल नंबर",
                        "label_mr": "मोबाईल नंबर",
                        "type": "tel",
                        "placeholder": "9876543210",
                        "required": True,
                        "entity_key": "phone",
                        "help": "Aadhaar-linked active mobile number for DBT alerts."
                    }
                ]
            },
            {
                "section_id": "land_details",
                "title": "Agricultural Land & Bank Information",
                "title_hi": "कृषि भूमि एवं बैंक विवरण",
                "title_mr": "शेती जमीन व बँक तपशील",
                "fields": [
                    {
                        "id": "state",
                        "label": "State",
                        "label_hi": "राज्य",
                        "label_mr": "राज्य",
                        "type": "text",
                        "placeholder": "Maharashtra",
                        "required": True,
                        "entity_key": "state",
                        "help": "State where agricultural land is located."
                    },
                    {
                        "id": "district",
                        "label": "District",
                        "label_hi": "जिला",
                        "label_mr": "जिल्हा",
                        "type": "text",
                        "placeholder": "Pune",
                        "required": True,
                        "entity_key": "district",
                        "help": "District where land record exists."
                    },
                    {
                        "id": "land_area",
                        "label": "Total Land Area (Acres / Hectares)",
                        "label_hi": "कुल कृषि भूमि (एकड़ / हेक्टेयर)",
                        "label_mr": "एकूण शेती क्षेत्र (एकर / हेक्टर)",
                        "type": "text",
                        "placeholder": "e.g. 2.5 Acres",
                        "required": True,
                        "entity_key": "landHolding",
                        "help": "Enter cultivable land size mentioned on 7/12 extract or Khatauni."
                    },
                    {
                        "id": "khata_number",
                        "label": "Survey / Khata / Dag Number",
                        "label_hi": "खसरा / खाता संख्या",
                        "label_mr": "गट / खाते क्रमांक",
                        "type": "text",
                        "placeholder": "e.g. 142/3A",
                        "required": True,
                        "help": "Land parcel identification number from revenue record."
                    },
                    {
                        "id": "bank_account",
                        "label": "Bank Account Number (Aadhaar Seeded)",
                        "label_hi": "बैंक खाता संख्या",
                        "label_mr": "बँक खाते क्रमांक",
                        "type": "text",
                        "placeholder": "123456789012",
                        "required": True,
                        "help": "Bank account where PM Kisan installments will be credited via DBT."
                    },
                    {
                        "id": "bank_ifsc",
                        "label": "Bank IFSC Code",
                        "label_hi": "बैंक आईएफएससी कोड",
                        "label_mr": "बँक IFSC कोड",
                        "type": "text",
                        "placeholder": "SBIN0001234",
                        "required": True,
                        "help": "11-character bank branch routing code."
                    }
                ]
            }
        ]
    },
    {
        "id": "ayushman_bharat",
        "title": "Ayushman Bharat PM-JAY Health Card",
        "title_hi": "आयुष्मान भारत स्वास्थ्य कार्ड आवेदन",
        "title_mr": "आयुष्मान भारत आरोग्य कार्ड अर्ज",
        "department": "National Health Authority (NHA)",
        "category": "Healthcare",
        "processing_days": "1-3 Days (Instant Digital Card)",
        "fee": "Free of Cost",
        "description": "Provides cashless health cover of up to ₹5,00,000 per family per year for secondary and tertiary care hospitalization across public and empaneled private hospitals.",
        "description_hi": "प्रति परिवार प्रति वर्ष ₹5 लाख तक का कैशलेस स्वास्थ्य बीमा।",
        "description_mr": "प्रति कुटुंब प्रति वर्ष ₹5 लाखांपर्यंतचे मोफत कॅशलेस उपचार संरक्षण.",
        "sections": [
            {
                "section_id": "beneficiary_info",
                "title": "Beneficiary Details",
                "title_hi": "लाभार्थी विवरण",
                "title_mr": "लाभार्थी तपशील",
                "fields": [
                    {
                        "id": "applicant_name",
                        "label": "Beneficiary Full Name",
                        "label_hi": "लाभार्थी का नाम",
                        "label_mr": "लाभार्थ्याचे नाव",
                        "type": "text",
                        "placeholder": "e.g. Anita Ramesh Patil",
                        "required": True,
                        "entity_key": "fullName",
                        "help": "Name as per Ration Card or Aadhaar."
                    },
                    {
                        "id": "applicant_age",
                        "label": "Age",
                        "label_hi": "आयु",
                        "label_mr": "वय",
                        "type": "number",
                        "placeholder": "38",
                        "required": True,
                        "entity_key": "age",
                        "help": "Current completed age."
                    },
                    {
                        "id": "applicant_gender",
                        "label": "Gender",
                        "label_hi": "लिंग",
                        "label_mr": "लिंग",
                        "type": "select",
                        "options": ["Female", "Male", "Transgender"],
                        "required": True,
                        "entity_key": "gender",
                        "help": "Gender."
                    },
                    {
                        "id": "aadhaar_number",
                        "label": "Aadhaar Number",
                        "label_hi": "आधार संख्या",
                        "label_mr": "आधार क्रमांक",
                        "type": "text",
                        "placeholder": "XXXX XXXX XXXX",
                        "required": True,
                        "entity_key": "aadhaar",
                        "help": "12-digit Aadhaar number for biometrics verification."
                    },
                    {
                        "id": "mobile_number",
                        "label": "Mobile Number",
                        "label_hi": "मोबाइल नंबर",
                        "label_mr": "मोबाईल नंबर",
                        "type": "tel",
                        "placeholder": "9876543210",
                        "required": True,
                        "entity_key": "phone",
                        "help": "Active mobile for OTP."
                    },
                    {
                        "id": "ration_card_number",
                        "label": "Ration Card Number (BPL / Antyodaya / Priority)",
                        "label_hi": "राशन कार्ड नंबर",
                        "label_mr": "रेशन कार्ड क्रमांक",
                        "type": "text",
                        "placeholder": "RC102938475",
                        "required": True,
                        "help": "Family ration card number for SECC deprivation matching."
                    },
                    {
                        "id": "district",
                        "label": "District",
                        "label_hi": "जिला",
                        "label_mr": "जिल्हा",
                        "type": "text",
                        "placeholder": "Pune",
                        "required": True,
                        "entity_key": "district",
                        "help": "Residence district."
                    },
                    {
                        "id": "state",
                        "label": "State",
                        "label_hi": "राज्य",
                        "label_mr": "राज्य",
                        "type": "text",
                        "placeholder": "Maharashtra",
                        "required": True,
                        "entity_key": "state",
                        "help": "Residence state."
                    }
                ]
            }
        ]
    },
    {
        "id": "caste_certificate",
        "title": "Application for Caste Certificate",
        "title_hi": "जाति प्रमाण पत्र के लिए आवेदन",
        "title_mr": "जातीचे प्रमाणपत्र अर्ज",
        "department": "Social Justice & Special Assistance Department",
        "category": "Certificates",
        "processing_days": "15-21 Days",
        "fee": "₹33 (Official Fee)",
        "description": "Essential certification of backward class status (SC / ST / VJNT / OBC / SBC) needed for educational reservation, fee waivers, and government employment.",
        "description_hi": "शैक्षणिक आरक्षण और सरकारी योजनाओं के लिए आवश्यक जाति प्रमाण पत्र।",
        "description_mr": "शैक्षणिक आरक्षण आणि शासकीय योजनांसाठी आवश्यक जात प्रमाणपत्र.",
        "sections": [
            {
                "section_id": "caste_details",
                "title": "Applicant & Caste Lineage",
                "title_hi": "आवेदक और जाति विवरण",
                "title_mr": "अर्जदार व जात तपशील",
                "fields": [
                    {
                        "id": "applicant_name",
                        "label": "Applicant Full Name",
                        "label_hi": "आवेदक का नाम",
                        "label_mr": "अर्जदाराचे नाव",
                        "type": "text",
                        "placeholder": "e.g. Ramesh Shankar Patil",
                        "required": True,
                        "entity_key": "fullName",
                        "help": "Name as per 10th marksheet or School Leaving Certificate."
                    },
                    {
                        "id": "father_name",
                        "label": "Father's Full Name",
                        "label_hi": "पिता का नाम",
                        "label_mr": "वडिलांचे नाव",
                        "type": "text",
                        "placeholder": "Shankar Patil",
                        "required": True,
                        "entity_key": "guardianName",
                        "help": "Father's name is required because caste is inherited patrilineally."
                    },
                    {
                        "id": "social_category",
                        "label": "Category Claimed",
                        "label_hi": "दावा किया गया वर्ग",
                        "label_mr": "मागणी केलेला प्रवर्ग",
                        "type": "select",
                        "options": ["OBC", "SC", "ST", "VJNT", "EWS"],
                        "required": True,
                        "entity_key": "socialCategory",
                        "help": "The reservation category you belong to."
                    },
                    {
                        "id": "sub_caste",
                        "label": "Sub-Caste / पोटजात",
                        "label_hi": "उप-जाति",
                        "label_mr": "पोटजात",
                        "type": "text",
                        "placeholder": "e.g. Maratha-Kunbi / Mali / Mahar / Gond",
                        "required": True,
                        "help": "Specific sub-caste as mentioned in family older school records."
                    },
                    {
                        "id": "mobile_number",
                        "label": "Mobile Number",
                        "label_hi": "मोबाइल नंबर",
                        "label_mr": "मोबाईल नंबर",
                        "type": "tel",
                        "placeholder": "9876543210",
                        "required": True,
                        "entity_key": "phone",
                        "help": "Mobile number for application updates."
                    },
                    {
                        "id": "aadhaar_number",
                        "label": "Aadhaar Number",
                        "label_hi": "आधार नंबर",
                        "label_mr": "आधार क्रमांक",
                        "type": "text",
                        "placeholder": "XXXX XXXX XXXX",
                        "required": True,
                        "entity_key": "aadhaar",
                        "help": "12-digit Aadhaar number."
                    },
                    {
                        "id": "district",
                        "label": "Native District",
                        "label_hi": "मूल जिला",
                        "label_mr": "मूळ जिल्हा",
                        "type": "text",
                        "placeholder": "Pune",
                        "required": True,
                        "entity_key": "district",
                        "help": "District where family originated before reference year."
                    },
                    {
                        "id": "state",
                        "label": "State",
                        "label_hi": "राज्य",
                        "label_mr": "राज्य",
                        "type": "text",
                        "placeholder": "Maharashtra",
                        "required": True,
                        "entity_key": "state",
                        "help": "State of origin."
                    }
                ]
            }
        ]
    },
    {
        "id": "domicile_certificate",
        "title": "Domicile & Nationality Certificate",
        "title_hi": "निवास एवं राष्ट्रीयता प्रमाण पत्र",
        "title_mr": "अधिवास व राष्ट्रीयत्व प्रमाणपत्र",
        "department": "Revenue Department",
        "category": "Certificates",
        "processing_days": "7-10 Days",
        "fee": "₹35",
        "description": "Proof that applicant has been residing in the state continuously for 15+ years; mandatory for state medical/engineering college admissions and state recruitment.",
        "description_hi": "राज्य में 15+ वर्षों से निरंतर निवास का प्रमाण, कॉलेज प्रवेश हेतु अनिवार्य।",
        "description_mr": "राज्यात १५ वर्षांहून अधिक काळ वास्तव्य असल्याचा दाखला; प्रवेशासाठी आवश्यक.",
        "sections": [
            {
                "section_id": "domicile_info",
                "title": "Residence & Applicant Details",
                "title_hi": "निवास और आवेदक विवरण",
                "title_mr": "रहिवासी व अर्जदार तपशील",
                "fields": [
                    {
                        "id": "applicant_name",
                        "label": "Full Name",
                        "label_hi": "पूरा नाम",
                        "label_mr": "पूर्ण नाव",
                        "type": "text",
                        "placeholder": "Ramesh Shankar Patil",
                        "required": True,
                        "entity_key": "fullName",
                        "help": "Applicant full name."
                    },
                    {
                        "id": "applicant_age",
                        "label": "Age",
                        "label_hi": "आयु",
                        "label_mr": "वय",
                        "type": "number",
                        "placeholder": "21",
                        "required": True,
                        "entity_key": "age",
                        "help": "Age in years."
                    },
                    {
                        "id": "years_in_state",
                        "label": "Period of Residence in State (Years)",
                        "label_hi": "राज्य में निवास की अवधि (वर्ष)",
                        "label_mr": "राज्यात वास्तव्याचा कालावधी (वर्षे)",
                        "type": "number",
                        "placeholder": "e.g. 21",
                        "required": True,
                        "help": "Number of continuous years lived in state (minimum 15 years required)."
                    },
                    {
                        "id": "residential_address",
                        "label": "Current Residential Address",
                        "label_hi": "वर्तमान आवासीय पता",
                        "label_mr": "सध्याचा पत्ता",
                        "type": "textarea",
                        "placeholder": "Plot No, Street, City",
                        "required": True,
                        "entity_key": "address",
                        "help": "Full address supported by proof of residence."
                    },
                    {
                        "id": "district",
                        "label": "District",
                        "label_hi": "जिला",
                        "label_mr": "जिल्हा",
                        "type": "text",
                        "placeholder": "Pune",
                        "required": True,
                        "entity_key": "district",
                        "help": "District."
                    },
                    {
                        "id": "mobile_number",
                        "label": "Mobile Number",
                        "label_hi": "मोबाइल नंबर",
                        "label_mr": "मोबाईल नंबर",
                        "type": "tel",
                        "placeholder": "9876543210",
                        "required": True,
                        "entity_key": "phone",
                        "help": "Mobile number."
                    }
                ]
            }
        ]
    },
    {
        "id": "senior_pension",
        "title": "National Social Assistance Old Age Pension",
        "title_hi": "राष्ट्रीय वृद्धावस्था पेंशन योजना",
        "title_mr": "राष्ट्रीय वृद्धापकाळ पेन्शन योजना",
        "department": "Ministry of Rural Development / Social Welfare",
        "category": "Pensions",
        "processing_days": "20-30 Days",
        "fee": "Free of Cost",
        "description": "Monthly financial pension assistance of ₹1,000 to ₹1,500 for senior citizens aged 60+ belonging to BPL households.",
        "description_hi": "60 वर्ष से अधिक आयु के बीपीएल वरिष्ठ नागरिकों के लिए मासिक पेंशन।",
        "description_mr": "६० वर्षांवरील दारिद्र्यरेषेखालील ज्येष्ठ नागरिकांना दरमहा पेन्शन सहाय्य.",
        "sections": [
            {
                "section_id": "senior_details",
                "title": "Senior Citizen Information",
                "title_hi": "वरिष्ठ नागरिक विवरण",
                "title_mr": "ज्येष्ठ नागरिक तपशील",
                "fields": [
                    {
                        "id": "applicant_name",
                        "label": "Full Name",
                        "label_hi": "पूरा नाम",
                        "label_mr": "पूर्ण नाव",
                        "type": "text",
                        "placeholder": "e.g. Yashodabai Patil",
                        "required": True,
                        "entity_key": "fullName",
                        "help": "Elderly applicant full name."
                    },
                    {
                        "id": "applicant_age",
                        "label": "Age (Must be 60+)",
                        "label_hi": "आयु (60+ अनिवार्य)",
                        "label_mr": "वय (६०+ अनिवार्य)",
                        "type": "number",
                        "placeholder": "65",
                        "required": True,
                        "entity_key": "age",
                        "help": "Minimum age is 60 years."
                    },
                    {
                        "id": "applicant_gender",
                        "label": "Gender",
                        "label_hi": "लिंग",
                        "label_mr": "लिंग",
                        "type": "select",
                        "options": ["Female", "Male", "Other"],
                        "required": True,
                        "entity_key": "gender",
                        "help": "Gender."
                    },
                    {
                        "id": "bpl_number",
                        "label": "BPL / Ration Card Number",
                        "label_hi": "बीपीएल राशन कार्ड नंबर",
                        "label_mr": "बीपीएल रेशन कार्ड क्रमांक",
                        "type": "text",
                        "placeholder": "BPL-87654321",
                        "required": True,
                        "help": "Below Poverty Line certificate or yellow/orange ration card."
                    },
                    {
                        "id": "bank_account",
                        "label": "Direct Benefit Bank Account",
                        "label_hi": "बैंक खाता संख्या",
                        "label_mr": "बँक खाते क्रमांक",
                        "type": "text",
                        "placeholder": "Bank account number",
                        "required": True,
                        "help": "Bank account for pension credit."
                    },
                    {
                        "id": "district",
                        "label": "District",
                        "label_hi": "जिला",
                        "label_mr": "जिल्हा",
                        "type": "text",
                        "placeholder": "Pune",
                        "required": True,
                        "entity_key": "district",
                        "help": "District."
                    },
                    {
                        "id": "state",
                        "label": "State",
                        "label_hi": "राज्य",
                        "label_mr": "राज्य",
                        "type": "text",
                        "placeholder": "Maharashtra",
                        "required": True,
                        "entity_key": "state",
                        "help": "State."
                    }
                ]
            }
        ]
    }
]

def get_all_forms() -> List[Dict[str, Any]]:
    return [
        {
            "id": f["id"],
            "title": f["title"],
            "title_hi": f["title_hi"],
            "title_mr": f["title_mr"],
            "department": f["department"],
            "category": f["category"],
            "processing_days": f["processing_days"],
            "fee": f["fee"],
            "description": f["description"],
            "description_hi": f["description_hi"],
            "description_mr": f["description_mr"],
            "total_fields": sum(len(s["fields"]) for s in f["sections"])
        }
        for f in GOVERNMENT_FORMS
    ]

def get_form_by_id(form_id: str) -> Optional[Dict[str, Any]]:
    for form in GOVERNMENT_FORMS:
        if form["id"] == form_id:
            return form
    return None

def auto_fill_form(form_id: str, extracted_entities: Dict[str, Any], existing_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Intelligently maps extracted entities to the form fields,
    filling fields that have matches and reporting what was mapped.
    """
    form = get_form_by_id(form_id)
    if not form:
        return {}

    filled_data = dict(existing_data or {})
    mapped_fields_info = {}

    for section in form["sections"]:
        for field in section["fields"]:
            field_id = field["id"]
            entity_key = field.get("entity_key")

            # Check if this field can be filled from extracted entities
            if entity_key and entity_key in extracted_entities:
                entity_info = extracted_entities[entity_key]
                entity_val = entity_info.get("value")
                
                # Format or convert if needed
                if field["type"] == "number" and isinstance(entity_val, (int, float)):
                    filled_data[field_id] = entity_val
                elif field["type"] == "select":
                    # Best match for select options
                    matched_opt = None
                    str_val = str(entity_val).lower()
                    for opt in field.get("options", []):
                        if opt.lower() in str_val or str_val in opt.lower():
                            matched_opt = opt
                            break
                    filled_data[field_id] = matched_opt if matched_opt else entity_val
                else:
                    filled_data[field_id] = entity_val

                mapped_fields_info[field_id] = {
                    "field_label": field["label"],
                    "value": filled_data[field_id],
                    "confidence": entity_info.get("confidence", 0.9),
                    "source": entity_info.get("source", "")
                }

    return {
        "form_id": form_id,
        "form_data": filled_data,
        "mapped_fields": mapped_fields_info,
        "mapped_count": len(mapped_fields_info)
    }
