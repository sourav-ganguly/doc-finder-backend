import requests
import random
from faker import Faker

# Initialize Faker for generating realistic names
fake = Faker()

# Constants
BASE_URL = "https://doc-finder-backend.onrender.com/doctors/"
LOCATIONS = ["Dhaka", "Barisal", "Chittagong", "Sylhet", "Rajshahi", "Khulna"]
SPECIALITIES = [
    "Cardiologist",
    "Neurologist",
    "Dermatologist",
    "Pediatrician",
    "Orthopedist",
    "Psychiatrist",
    "Gynecologist",
    "Ophthalmologist",
    "ENT Specialist",
    "Dentist"
]

def generate_phone():
    # Generate Bangladesh format phone number
    return f"+880 {random.randint(1300000000, 1999999999)}"

def add_doctor():
    doctor_data = {
        "name": f"Dr. {fake.name()}",
        "speciality": random.choice(SPECIALITIES),
        "phone_number": generate_phone(),
        "location": random.choice(LOCATIONS)
    }
    
    try:
        response = requests.post(
            BASE_URL,
            json=doctor_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print(f"Successfully added doctor: {doctor_data['name']}")
        else:
            print(f"Failed to add doctor: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")

def main():
    print("Starting to add 100 doctors...")
    for i in range(100):
        print(f"\nAdding doctor {i+1}/100")
        add_doctor()
    print("\nCompleted adding doctors!")

if __name__ == "__main__":
    main() 