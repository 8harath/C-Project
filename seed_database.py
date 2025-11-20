from app import create_app
from models import db
from models.user import User
from models.medicine import Medicine
from models.alternative_medicine import AlternativeMedicine
from datetime import date, timedelta
import random

def seed_users():
    """Create default users"""
    # Check if users already exist
    if User.query.first():
        print("Users already exist. Skipping user creation.")
        return

    admin = User(
        username='admin',
        email='admin@warehouse.com',
        password='admin123',
        role='Admin'
    )

    staff = User(
        username='staff',
        email='staff@warehouse.com',
        password='staff123',
        role='Staff'
    )

    db.session.add(admin)
    db.session.add(staff)
    db.session.commit()

    print("✓ Default users created:")
    print("  - Admin: username='admin', password='admin123'")
    print("  - Staff: username='staff', password='staff123'")

def seed_medicines():
    """Create 100 medicine records"""
    if Medicine.query.first():
        print("Medicines already exist. Skipping medicine creation.")
        return

    medicines_data = [
        # Allergy (11 medicines)
        {"name": "Cetirizine 10mg", "desc": "Antihistamine for allergy relief", "mfr": "Cipla Ltd", "cat": "Allergy", "price": 45.00},
        {"name": "Loratadine 10mg", "desc": "Non-drowsy allergy medication", "mfr": "Sun Pharma", "cat": "Allergy", "price": 50.00},
        {"name": "Fexofenadine 120mg", "desc": "Long-acting antihistamine", "mfr": "Sanofi", "cat": "Allergy", "price": 85.00},
        {"name": "Levocetirizine 5mg", "desc": "Advanced antihistamine", "mfr": "Dr. Reddy's", "cat": "Allergy", "price": 55.00},
        {"name": "Desloratadine 5mg", "desc": "Once-daily allergy relief", "mfr": "Glenmark", "cat": "Allergy", "price": 70.00},
        {"name": "Diphenhydramine 25mg", "desc": "First-generation antihistamine", "mfr": "Johnson & Johnson", "cat": "Allergy", "price": 40.00},
        {"name": "Chlorpheniramine 4mg", "desc": "Classic allergy medication", "mfr": "Pfizer", "cat": "Allergy", "price": 35.00},
        {"name": "Hydroxyzine 25mg", "desc": "Antihistamine for itching", "mfr": "Lupin", "cat": "Allergy", "price": 60.00},
        {"name": "Montelukast 10mg", "desc": "Leukotriene receptor antagonist", "mfr": "Ranbaxy", "cat": "Allergy", "price": 95.00},
        {"name": "Beclomethasone Nasal Spray", "desc": "Corticosteroid for allergic rhinitis", "mfr": "GSK", "cat": "Allergy", "price": 120.00},
        {"name": "Budesonide Nasal Spray", "desc": "Steroid nasal spray", "mfr": "AstraZeneca", "cat": "Allergy", "price": 150.00},

        # Cold and Mild Flu (11 medicines)
        {"name": "Paracetamol 500mg", "desc": "Pain and fever relief", "mfr": "Micro Labs", "cat": "Cold and Mild Flu", "price": 20.00},
        {"name": "Phenylephrine 10mg", "desc": "Nasal decongestant", "mfr": "Cipla Ltd", "cat": "Cold and Mild Flu", "price": 45.00},
        {"name": "Pseudoephedrine 60mg", "desc": "Decongestant for cold", "mfr": "Sun Pharma", "cat": "Cold and Mild Flu", "price": 55.00},
        {"name": "Guaifenesin 200mg", "desc": "Expectorant", "mfr": "Dr. Reddy's", "cat": "Cold and Mild Flu", "price": 40.00},
        {"name": "Acetaminophen Combo", "desc": "Multi-symptom cold relief", "mfr": "Johnson & Johnson", "cat": "Cold and Mild Flu", "price": 75.00},
        {"name": "Ambroxol 30mg", "desc": "Mucolytic agent", "mfr": "Boehringer Ingelheim", "cat": "Cold and Mild Flu", "price": 50.00},
        {"name": "Bromhexine 8mg", "desc": "Cough suppressant", "mfr": "Sanofi", "cat": "Cold and Mild Flu", "price": 45.00},
        {"name": "Cetirizine+Phenylephrine", "desc": "Combined cold relief", "mfr": "Cipla Ltd", "cat": "Cold and Mild Flu", "price": 65.00},
        {"name": "Dextromethorphan Combo", "desc": "Cough and cold relief", "mfr": "Pfizer", "cat": "Cold and Mild Flu", "price": 70.00},
        {"name": "Zinc Supplements 50mg", "desc": "Immune support", "mfr": "Nature's Bounty", "cat": "Cold and Mild Flu", "price": 180.00},
        {"name": "Vitamin C 1000mg", "desc": "Immune booster", "mfr": "HealthKart", "cat": "Cold and Mild Flu", "price": 200.00},

        # Cough (11 medicines)
        {"name": "Dextromethorphan 15mg", "desc": "Cough suppressant", "mfr": "Pfizer", "cat": "Cough", "price": 55.00},
        {"name": "Codeine Phosphate 10mg", "desc": "Opioid cough suppressant", "mfr": "GSK", "cat": "Cough", "price": 85.00},
        {"name": "Guaifenesin Syrup", "desc": "Expectorant syrup", "mfr": "Sun Pharma", "cat": "Cough", "price": 90.00},
        {"name": "Ambroxol Syrup", "desc": "Mucolytic syrup", "mfr": "Cipla Ltd", "cat": "Cough", "price": 80.00},
        {"name": "Bromhexine Syrup", "desc": "Cough relief syrup", "mfr": "Sanofi", "cat": "Cough", "price": 75.00},
        {"name": "Honey-based Cough Syrup", "desc": "Natural cough relief", "mfr": "Dabur", "cat": "Cough", "price": 110.00},
        {"name": "Terbutaline 2.5mg", "desc": "Bronchodilator", "mfr": "AstraZeneca", "cat": "Cough", "price": 65.00},
        {"name": "Salbutamol 4mg", "desc": "Beta-2 agonist", "mfr": "GSK", "cat": "Cough", "price": 70.00},
        {"name": "Levosalbutamol 2mg", "desc": "Bronchodilator", "mfr": "Cipla Ltd", "cat": "Cough", "price": 75.00},
        {"name": "Theophylline 200mg", "desc": "Bronchodilator", "mfr": "Sun Pharma", "cat": "Cough", "price": 80.00},
        {"name": "Chlorpheniramine Syrup", "desc": "Antihistamine syrup", "mfr": "Pfizer", "cat": "Cough", "price": 60.00},

        # Dermatology (11 medicines)
        {"name": "Betamethasone Cream", "desc": "Corticosteroid for skin", "mfr": "GSK", "cat": "Dermatology", "price": 95.00},
        {"name": "Hydrocortisone 1% Cream", "desc": "Mild steroid cream", "mfr": "Johnson & Johnson", "cat": "Dermatology", "price": 85.00},
        {"name": "Clotrimazole Cream", "desc": "Antifungal cream", "mfr": "Bayer", "cat": "Dermatology", "price": 75.00},
        {"name": "Ketoconazole 2% Cream", "desc": "Antifungal medication", "mfr": "Cipla Ltd", "cat": "Dermatology", "price": 90.00},
        {"name": "Mupirocin Ointment", "desc": "Antibiotic ointment", "mfr": "GSK", "cat": "Dermatology", "price": 120.00},
        {"name": "Fusidic Acid Cream", "desc": "Topical antibiotic", "mfr": "Leo Pharma", "cat": "Dermatology", "price": 135.00},
        {"name": "Benzoyl Peroxide 5%", "desc": "Acne treatment", "mfr": "Galderma", "cat": "Dermatology", "price": 180.00},
        {"name": "Tretinoin 0.05% Cream", "desc": "Retinoid for acne", "mfr": "Johnson & Johnson", "cat": "Dermatology", "price": 250.00},
        {"name": "Calamine Lotion", "desc": "Soothing lotion", "mfr": "Himalaya", "cat": "Dermatology", "price": 65.00},
        {"name": "Povidone-Iodine 10%", "desc": "Antiseptic solution", "mfr": "Win-Medicare", "cat": "Dermatology", "price": 55.00},
        {"name": "Silver Sulfadiazine Cream", "desc": "Burn treatment", "mfr": "Sun Pharma", "cat": "Dermatology", "price": 140.00},

        # Eye/ENT (11 medicines)
        {"name": "Moxifloxacin Eye Drops", "desc": "Antibiotic eye drops", "mfr": "Alcon", "cat": "Eye/ENT", "price": 180.00},
        {"name": "Ofloxacin Eye Drops", "desc": "Antibiotic for eyes", "mfr": "Cipla Ltd", "cat": "Eye/ENT", "price": 120.00},
        {"name": "Ciprofloxacin Ear Drops", "desc": "Antibiotic ear drops", "mfr": "Sun Pharma", "cat": "Eye/ENT", "price": 95.00},
        {"name": "Chloramphenicol Eye Drops", "desc": "Broad-spectrum antibiotic", "mfr": "Pfizer", "cat": "Eye/ENT", "price": 65.00},
        {"name": "Timolol Eye Drops", "desc": "Glaucoma treatment", "mfr": "Bausch & Lomb", "cat": "Eye/ENT", "price": 240.00},
        {"name": "Latanoprost Eye Drops", "desc": "Prostaglandin for glaucoma", "mfr": "Pfizer", "cat": "Eye/ENT", "price": 350.00},
        {"name": "Tropicamide Eye Drops", "desc": "Mydriatic agent", "mfr": "Alcon", "cat": "Eye/ENT", "price": 150.00},
        {"name": "Phenylephrine Eye Drops", "desc": "Decongestant drops", "mfr": "Bausch & Lomb", "cat": "Eye/ENT", "price": 85.00},
        {"name": "Sodium Chloride Drops", "desc": "Saline drops", "mfr": "Cipla Ltd", "cat": "Eye/ENT", "price": 45.00},
        {"name": "Artificial Tears", "desc": "Lubricating eye drops", "mfr": "Allergan", "cat": "Eye/ENT", "price": 190.00},
        {"name": "Wax Softener Drops", "desc": "Earwax removal", "mfr": "Sun Pharma", "cat": "Eye/ENT", "price": 70.00},

        # Fever (11 medicines)
        {"name": "Paracetamol 650mg", "desc": "Fever reducer", "mfr": "Micro Labs", "cat": "Fever", "price": 25.00},
        {"name": "Ibuprofen 400mg", "desc": "NSAID for fever", "mfr": "Abbott", "cat": "Fever", "price": 30.00},
        {"name": "Mefenamic Acid 250mg", "desc": "Pain and fever relief", "mfr": "Pfizer", "cat": "Fever", "price": 40.00},
        {"name": "Diclofenac 50mg", "desc": "Anti-inflammatory", "mfr": "Novartis", "cat": "Fever", "price": 35.00},
        {"name": "Aspirin 325mg", "desc": "Antipyretic and analgesic", "mfr": "Bayer", "cat": "Fever", "price": 28.00},
        {"name": "Nimesulide 100mg", "desc": "COX-2 inhibitor", "mfr": "Panacea Biotec", "cat": "Fever", "price": 45.00},
        {"name": "Dolo 650", "desc": "Paracetamol brand", "mfr": "Micro Labs", "cat": "Fever", "price": 30.00},
        {"name": "Crocin 650", "desc": "Paracetamol brand", "mfr": "GSK", "cat": "Fever", "price": 30.00},
        {"name": "Calpol 500", "desc": "Paracetamol brand", "mfr": "GSK", "cat": "Fever", "price": 25.00},
        {"name": "Ibuprofen Suspension", "desc": "Pediatric fever relief", "mfr": "Abbott", "cat": "Fever", "price": 110.00},
        {"name": "Paracetamol Suspension", "desc": "Pediatric paracetamol", "mfr": "Micro Labs", "cat": "Fever", "price": 85.00},

        # Pain Relief (12 medicines)
        {"name": "Ibuprofen 600mg", "desc": "Strong pain reliever", "mfr": "Abbott", "cat": "Pain Relief", "price": 40.00},
        {"name": "Diclofenac 75mg", "desc": "Strong anti-inflammatory", "mfr": "Novartis", "cat": "Pain Relief", "price": 45.00},
        {"name": "Aceclofenac 100mg", "desc": "NSAID for pain", "mfr": "Ipca Labs", "cat": "Pain Relief", "price": 50.00},
        {"name": "Piroxicam 20mg", "desc": "Long-acting NSAID", "mfr": "Pfizer", "cat": "Pain Relief", "price": 55.00},
        {"name": "Tramadol 50mg", "desc": "Opioid analgesic", "mfr": "Sun Pharma", "cat": "Pain Relief", "price": 85.00},
        {"name": "Ketorolac 10mg", "desc": "Potent NSAID", "mfr": "Dr. Reddy's", "cat": "Pain Relief", "price": 65.00},
        {"name": "Etoricoxib 90mg", "desc": "COX-2 selective inhibitor", "mfr": "MSD", "cat": "Pain Relief", "price": 95.00},
        {"name": "Naproxen 500mg", "desc": "Long-acting pain relief", "mfr": "Cipla Ltd", "cat": "Pain Relief", "price": 60.00},
        {"name": "Indomethacin 25mg", "desc": "NSAID for inflammation", "mfr": "Zydus", "cat": "Pain Relief", "price": 45.00},
        {"name": "Paracetamol+Ibuprofen", "desc": "Combined pain relief", "mfr": "Abbott", "cat": "Pain Relief", "price": 55.00},
        {"name": "Diclofenac Gel", "desc": "Topical pain relief", "mfr": "Novartis", "cat": "Pain Relief", "price": 180.00},
        {"name": "Capsaicin Cream", "desc": "Topical analgesic", "mfr": "Himalaya", "cat": "Pain Relief", "price": 220.00},

        # Vitamins (11 medicines)
        {"name": "Vitamin D3 60000 IU", "desc": "Bone health supplement", "mfr": "Mankind", "cat": "Vitamins", "price": 45.00},
        {"name": "Vitamin B Complex", "desc": "B-vitamins combination", "mfr": "HealthKart", "cat": "Vitamins", "price": 180.00},
        {"name": "Vitamin C 500mg", "desc": "Antioxidant supplement", "mfr": "Nature's Bounty", "cat": "Vitamins", "price": 150.00},
        {"name": "Multivitamin Tablets", "desc": "Complete nutrition", "mfr": "Centrum", "cat": "Vitamins", "price": 350.00},
        {"name": "Calcium+Vitamin D3", "desc": "Bone health combo", "mfr": "Cipla Ltd", "cat": "Vitamins", "price": 220.00},
        {"name": "Iron+Folic Acid", "desc": "Hemoglobin booster", "mfr": "Sun Pharma", "cat": "Vitamins", "price": 95.00},
        {"name": "Vitamin E 400 IU", "desc": "Skin health vitamin", "mfr": "Nature's Bounty", "cat": "Vitamins", "price": 280.00},
        {"name": "Vitamin A 10000 IU", "desc": "Vision health", "mfr": "HealthKart", "cat": "Vitamins", "price": 160.00},
        {"name": "Omega-3 Fish Oil", "desc": "Heart health supplement", "mfr": "Nutrilite", "cat": "Vitamins", "price": 450.00},
        {"name": "Biotin 10mg", "desc": "Hair and nail health", "mfr": "HealthKart", "cat": "Vitamins", "price": 380.00},
        {"name": "Zinc 50mg", "desc": "Immune support", "mfr": "Nature's Bounty", "cat": "Vitamins", "price": 190.00},

        # Women Hygiene (11 medicines)
        {"name": "Clotrimazole Pessaries", "desc": "Vaginal antifungal", "mfr": "Bayer", "cat": "Women Hygiene", "price": 120.00},
        {"name": "Metronidazole Vaginal Gel", "desc": "Bacterial vaginosis treatment", "mfr": "Sun Pharma", "cat": "Women Hygiene", "price": 180.00},
        {"name": "Fluconazole 150mg", "desc": "Oral antifungal", "mfr": "Pfizer", "cat": "Women Hygiene", "price": 45.00},
        {"name": "Mefenamic Acid 500mg", "desc": "Menstrual pain relief", "mfr": "Pfizer", "cat": "Women Hygiene", "price": 55.00},
        {"name": "Tranexamic Acid 500mg", "desc": "Heavy bleeding treatment", "mfr": "Cipla Ltd", "cat": "Women Hygiene", "price": 140.00},
        {"name": "Norethisterone 5mg", "desc": "Menstrual regulation", "mfr": "Zydus", "cat": "Women Hygiene", "price": 85.00},
        {"name": "Iron Supplements", "desc": "Anemia prevention", "mfr": "Sun Pharma", "cat": "Women Hygiene", "price": 110.00},
        {"name": "Folic Acid 5mg", "desc": "Prenatal supplement", "mfr": "Abbott", "cat": "Women Hygiene", "price": 60.00},
        {"name": "Calcium 500mg", "desc": "Bone health for women", "mfr": "Cipla Ltd", "cat": "Women Hygiene", "price": 180.00},
        {"name": "Cranberry Supplements", "desc": "UTI prevention", "mfr": "HealthKart", "cat": "Women Hygiene", "price": 350.00},
        {"name": "Probiotic Capsules", "desc": "Vaginal health", "mfr": "Culturelle", "cat": "Women Hygiene", "price": 450.00},
    ]

    medicines = []
    base_barcode = 8901234500000

    for i, med_data in enumerate(medicines_data):
        # Random stock between 50-200
        stock = random.randint(50, 200)

        # Random expiry date between 6 months to 3 years
        days_until_expiry = random.randint(180, 1095)
        expiry = date.today() + timedelta(days=days_until_expiry)

        # Barcode
        barcode = str(base_barcode + i)

        medicine = Medicine(
            name=med_data["name"],
            description=med_data["desc"],
            manufacturer=med_data["mfr"],
            category=med_data["cat"],
            quantity=stock,
            price=med_data["price"],
            expiry_date=expiry,
            stock=stock,
            reorder_level=random.randint(10, 30),
            barcode=barcode
        )
        medicines.append(medicine)

    db.session.bulk_save_objects(medicines)
    db.session.commit()

    print(f"✓ Created {len(medicines)} medicines across 9 categories")

def seed_alternatives():
    """Create alternative medicine mappings"""
    # Get all medicines
    all_medicines = Medicine.query.all()

    # Create dictionary by category
    by_category = {}
    for med in all_medicines:
        if med.category not in by_category:
            by_category[med.category] = []
        by_category[med.category].append(med)

    alternatives = []

    # Create alternatives within same category
    for category, meds in by_category.items():
        if len(meds) < 2:
            continue

        # For each medicine, add 3-5 alternatives from same category
        for primary in meds:
            # Get other medicines in same category
            other_meds = [m for m in meds if m.medicine_id != primary.medicine_id]

            # Select 3-5 random alternatives
            num_alternatives = min(random.randint(3, 5), len(other_meds))
            selected_alts = random.sample(other_meds, num_alternatives)

            for i, alt in enumerate(selected_alts):
                alternative = AlternativeMedicine(
                    primary_medicine_id=primary.medicine_id,
                    alternative_medicine_id=alt.medicine_id,
                    reason="Same category - similar therapeutic effect",
                    priority=i + 1
                )
                alternatives.append(alternative)

    db.session.bulk_save_objects(alternatives)
    db.session.commit()

    print(f"✓ Created {len(alternatives)} alternative medicine mappings")

def main():
    """Main seeding function"""
    app = create_app('development')

    with app.app_context():
        print("\n" + "="*50)
        print("DATABASE SEEDING STARTED")
        print("="*50 + "\n")

        seed_users()
        seed_medicines()
        seed_alternatives()

        print("\n" + "="*50)
        print("DATABASE SEEDING COMPLETED")
        print("="*50)
        print("\nLogin Credentials:")
        print("  Admin - username: 'admin' | password: 'admin123'")
        print("  Staff - username: 'staff' | password: 'staff123'")
        print("\nYou can now run the application with: python app.py")
        print("="*50 + "\n")

if __name__ == '__main__':
    main()
