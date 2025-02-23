import os
import openai
import logging
from difflib import get_close_matches

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

speciality_list = [
    "Accident & Emergency",
    "Anesthesiology",
    "Blood Bank",
    "Cardiac Surgery",
    "Cardiology",
    "Cardiothoracic & Vascular Surgery",
    "Child Development Centre",
    "Clinical & Aesthetic Dermatology",
    "Clinical Oncology & Radiotherapy",
    "Clinical Pathology",
    "Colorectal & Laparoscopic Surgery",
    "Counsellor",
    "Critical Care",
    "Dental & Maxillofacial Surgery",
    "Dental Surgery & Orthodontics",
    "Dermatology",
    "Dermatology & Venereology",
    "Diabetology & Endocrinology",
    "Diagnostic & Interventional Radiology",
    "Dietetics & Nutrition",
    "ENT",
    "Endocrinology",
    "Epileptologist & Neuromuscular Disorder Specialist",
    "Fertility Centre",
    "Gastroenterology",
    "Gastroenterology & Hepatology",
    "General & Laparoscopic Surgery",
    "General Surgery",
    "Gynecology",
    "Gynecology and Obstetrics",
    "HDU & Internal Medicine",
    "Haematology & Stem Cell Transplant",
    "Heart Failure & Interventional Cardiology",
    "Hematology",
    "Hepatobiliary Surgery",
    "Hepatology & Gastroenterology",
    "Hip Centre",
    "Internal Medicine",
    "Joint Care & Wellness Centre",
    "Lab Medicine",
    "Liver & Pancreatic Diseases",
    "Microbiology & Infection Control",
    "NICU",
    "Neonatology",
    "Nephrology",
    "Neuroanesthesiology",
    "Neurology",
    "Neurosurgery",
    "Nuclear Medicine",
    "Oncology",
    "Oncosurgery",
    "Ophthalmology",
    "Oral & Dental Surgeon",
    "Orthopedics",
    "Paediatric Surgery",
    "Pancreatic and Liver Transplant",
    "Pathology & Laboratory Medicine",
    "Pathology Laboratory",
    "Pediatric Surgery",
    "Pediatrics",
    "Physical Medicine",
    "Plastic Surgery",
    "Psychiatry",
    "Psychologist",
    "Radiology & Imaging",
    "Reconstructive & Cosmetic Surgery",
    "Respiratory Medicine",
    "Rheumatology",
    "Urology"
]

def find_closest_specialty(specialty):
    """
    Find the closest matching specialty from our predefined list
    """
    matches = get_close_matches(specialty.lower(), [s.lower() for s in speciality_list], n=1, cutoff=0.6)
    if matches:
        # Return the original casing from speciality_list
        return next(s for s in speciality_list if s.lower() == matches[0])
    return None

def match_specialization(symptoms):
    """
    Use OpenAI's GPT model to analyze symptoms and recommend medical specializations
    from our predefined list of specialties
    """
    try:
        # Craft a detailed prompt for the model
        available_specialties = ", ".join(speciality_list)
        prompt = f"""You are a medical expert assistant. Based on the following symptoms, 
        recommend the most appropriate medical specialization(s) from this list of available specialties:
        {available_specialties}

        Patient's symptoms: {symptoms}

        Provide only the name of the medical specialization exactly as written in the list above. 
        If multiple specializations are equally relevant, list them in order of priority, separated by semicolons.
        Do not include any explanations or additional text. Only use specializations from the provided list."""

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a medical expert assistant that recommends appropriate medical specializations based on symptoms."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100
        )

        # Extract and clean the response
        suggested_specialties = response.choices[0].message['content'].strip().split(';')
        
        # Validate and match each specialty against our list
        validated_specialties = []
        for specialty in suggested_specialties:
            specialty = specialty.strip()
            if specialty in speciality_list:
                validated_specialties.append(specialty)
            else:
                closest_match = find_closest_specialty(specialty)
                if closest_match:
                    validated_specialties.append(closest_match)
        
        # If no valid specialties found, return Internal Medicine as default
        if not validated_specialties:
            return "Internal Medicine"
            
        return ";".join(validated_specialties)

    except Exception as e:
        logger.error(f"Error in match_specialization: {str(e)}")
        return "Internal Medicine"