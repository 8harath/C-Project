"""
Seed database with initial data:
- Admin and Staff users
- 100 medicines across 9 categories
- Alternative medicine mappings
"""

from app import create_app
from models import db
from models.user import User
from models.medicine import Medicine, AlternativeMedicine
from datetime import datetime, timedelta
import random

def seed_users():
    """Create default admin and staff users"""
    print("Creating users...")

    # Check if users already exist
    if User.query.filter_by(username='admin').first():
        print("Users already exist, skipping...")
        return

    # Create admin user
    admin = User(
        username='admin',
        email='admin@warehouse.com',
        password='admin123',
        role='Admin'
    )

    # Create staff user
    staff = User(
        username='staff',
        email='staff@warehouse.com',
        password='staff123',
        role='Staff'
    )

    db.session.add(admin)
    db.session.add(staff)
    db.session.commit()
    print("✓ Created admin and staff users")


def generate_barcode(index):
    """Generate a unique 13-digit barcode"""
    base = 8901234000000
    return str(base + index)


def seed_medicines():
    """Create 100 medicines across 9 categories"""
    print("Creating medicines...")

    # Check if medicines already exist
    if Medicine.query.count() > 0:
        print("Medicines already exist, skipping...")
        return

    medicines_data = [
        # Allergy (11 medicines)
        ("Cetirizine 10mg", "Antihistamine for allergy relief", "Cipla Ltd", "Allergy", 150, 45.00, 20),
        ("Loratadine 10mg", "Non-drowsy allergy relief", "Sun Pharma", "Allergy", 120, 55.00, 15),
        ("Fexofenadine 120mg", "Fast-acting antihistamine", "Sanofi India", "Allergy", 100, 85.00, 10),
        ("Levocetirizine 5mg", "Advanced allergy medication", "Dr. Reddy's", "Allergy", 180, 50.00, 25),
        ("Desloratadine 5mg", "Long-lasting relief", "Glenmark", "Allergy", 90, 95.00, 15),
        ("Diphenhydramine 25mg", "Classic antihistamine", "Pfizer", "Allergy", 200, 35.00, 30),
        ("Chlorpheniramine 4mg", "Multi-symptom relief", "Abbott", "Allergy", 160, 25.00, 20),
        ("Hydroxyzine 25mg", "Anxiety and allergy relief", "Lupin", "Allergy", 75, 65.00, 10),
        ("Montelukast 10mg", "Asthma and allergy", "Cipla Ltd", "Allergy", 110, 120.00, 15),
        ("Beclomethasone Nasal Spray", "Nasal allergy relief", "GSK", "Allergy", 85, 145.00, 10),
        ("Budesonide Nasal Spray", "Steroid nasal spray", "AstraZeneca", "Allergy", 95, 155.00, 12),

        # Cold and Mild Flu (11 medicines)
        ("Paracetamol 500mg", "Fever and pain relief", "Micro Labs", "Cold and Mild Flu", 500, 15.00, 50),
        ("Phenylephrine 10mg", "Nasal decongestant", "Cipla Ltd", "Cold and Mild Flu", 200, 35.00, 25),
        ("Pseudoephedrine 30mg", "Sinus relief", "Sun Pharma", "Cold and Mild Flu", 150, 45.00, 20),
        ("Guaifenesin 200mg", "Expectorant for chest congestion", "Lupin", "Cold and Mild Flu", 180, 55.00, 22),
        ("Acetaminophen + Phenylephrine", "Cold combo", "Johnson & Johnson", "Cold and Mild Flu", 220, 65.00, 30),
        ("Ambroxol 30mg", "Mucolytic agent", "Alkem Labs", "Cold and Mild Flu", 160, 40.00, 20),
        ("Bromhexine 8mg", "Cough suppressant", "Torrent Pharma", "Cold and Mild Flu", 140, 38.00, 18),
        ("Cetirizine + Phenylephrine", "Allergy and cold combo", "Dr. Reddy's", "Cold and Mild Flu", 175, 58.00, 25),
        ("Dextromethorphan 10mg", "Cough suppressant", "Pfizer", "Cold and Mild Flu", 130, 48.00, 15),
        ("Zinc Acetate Lozenges", "Immune support", "Nature's Bounty", "Cold and Mild Flu", 250, 120.00, 35),
        ("Vitamin C 500mg", "Immunity booster", "HealthKart", "Cold and Mild Flu", 300, 95.00, 40),

        # Cough (11 medicines)
        ("Dextromethorphan Syrup", "Cough suppressant syrup", "Abbott", "Cough", 180, 85.00, 25),
        ("Codeine 15mg", "Prescription cough relief", "GSK", "Cough", 60, 125.00, 8),
        ("Guaifenesin Syrup", "Expectorant syrup", "Cipla Ltd", "Cough", 200, 75.00, 30),
        ("Ambroxol Syrup", "Mucolytic syrup", "Sun Pharma", "Cough", 190, 68.00, 28),
        ("Bromhexine Syrup", "Cough relief syrup", "Lupin", "Cough", 170, 62.00, 24),
        ("Honey-based Cough Syrup", "Natural cough relief", "Dabur", "Cough", 250, 95.00, 35),
        ("Terbutaline 2.5mg", "Bronchodilator", "Dr. Reddy's", "Cough", 100, 55.00, 15),
        ("Salbutamol 4mg", "Asthma and cough", "Cipla Ltd", "Cough", 120, 45.00, 18),
        ("Levosalbutamol Inhaler", "Fast-acting inhaler", "GSK", "Cough", 75, 185.00, 10),
        ("Theophylline 200mg", "Bronchodilator", "Zydus Cadila", "Cough", 90, 72.00, 12),
        ("Chlorpheniramine + Codeine", "Cold and cough combo", "Abbott", "Cough", 85, 98.00, 12),

        # Dermatology (11 medicines)
        ("Betamethasone Cream", "Steroid cream for skin", "GSK", "Dermatology", 140, 125.00, 20),
        ("Hydrocortisone 1% Cream", "Mild steroid cream", "Johnson & Johnson", "Dermatology", 160, 95.00, 22),
        ("Clotrimazole Cream", "Antifungal cream", "Glenmark", "Dermatology", 180, 78.00, 25),
        ("Ketoconazole 2% Cream", "Antifungal treatment", "Cipla Ltd", "Dermatology", 150, 88.00, 20),
        ("Mupirocin Ointment", "Antibiotic ointment", "GSK", "Dermatology", 120, 145.00, 18),
        ("Fusidic Acid Cream", "Bacterial skin infection", "Leo Pharma", "Dermatology", 110, 165.00, 15),
        ("Benzoyl Peroxide 5% Gel", "Acne treatment", "Galderma", "Dermatology", 200, 225.00, 28),
        ("Tretinoin 0.025% Cream", "Anti-acne retinoid", "Johnson & Johnson", "Dermatology", 95, 285.00, 12),
        ("Calamine Lotion", "Soothing skin lotion", "Himalaya", "Dermatology", 250, 55.00, 35),
        ("Povidone-Iodine Solution", "Antiseptic solution", "Win-Medicare", "Dermatology", 220, 45.00, 30),
        ("Silver Sulfadiazine Cream", "Burn treatment", "Sun Pharma", "Dermatology", 130, 185.00, 18),

        # Eye/ENT (11 medicines)
        ("Moxifloxacin Eye Drops", "Antibiotic eye drops", "Alcon", "Eye/ENT", 150, 145.00, 20),
        ("Ofloxacin Eye Drops", "Bacterial eye infection", "Cipla Ltd", "Eye/ENT", 180, 85.00, 25),
        ("Ciprofloxacin Ear Drops", "Ear infection treatment", "Sun Pharma", "Eye/ENT", 160, 65.00, 22),
        ("Chloramphenicol Eye Drops", "Broad-spectrum antibiotic", "Pfizer", "Eye/ENT", 140, 55.00, 20),
        ("Timolol Eye Drops", "Glaucoma treatment", "Allergan", "Eye/ENT", 90, 225.00, 12),
        ("Latanoprost Eye Drops", "Glaucoma medication", "Pfizer", "Eye/ENT", 85, 285.00, 10),
        ("Tropicamide Eye Drops", "Pupil dilator", "Alcon", "Eye/ENT", 100, 125.00, 15),
        ("Phenylephrine Eye Drops", "Eye decongestant", "Bausch & Lomb", "Eye/ENT", 175, 95.00, 24),
        ("Sodium Chloride Eye Drops", "Lubricating eye drops", "Refresh", "Eye/ENT", 250, 45.00, 35),
        ("Artificial Tears", "Dry eye relief", "Systane", "Eye/ENT", 220, 135.00, 30),
        ("Wax Softener Ear Drops", "Earwax removal", "Cipla Ltd", "Eye/ENT", 180, 55.00, 25),

        # Fever (11 medicines)
        ("Dolo 650mg", "Paracetamol for fever", "Micro Labs", "Fever", 600, 25.00, 75),
        ("Crocin 650mg", "Fast fever relief", "GSK", "Fever", 550, 28.00, 70),
        ("Ibuprofen 400mg", "NSAID for fever and pain", "Abbott", "Fever", 400, 18.00, 50),
        ("Mefenamic Acid 250mg", "Pain and fever relief", "Blue Cross", "Fever", 300, 35.00, 40),
        ("Diclofenac 50mg", "Strong anti-inflammatory", "Novartis", "Fever", 250, 22.00, 35),
        ("Aspirin 325mg", "Classic fever reducer", "Bayer", "Fever", 450, 12.00, 55),
        ("Nimesulide 100mg", "Fast-acting fever relief", "Panacea Biotec", "Fever", 280, 28.00, 38),
        ("Calpol 250mg Suspension", "Children's fever medicine", "GSK", "Fever", 350, 55.00, 45),
        ("Metacin 500mg", "Paracetamol variant", "Sun Pharma", "Fever", 420, 22.00, 52),
        ("Ibuprofen Suspension", "Children's fever syrup", "Abbott", "Fever", 300, 68.00, 40),
        ("Paracetamol + Ibuprofen", "Dual-action fever relief", "Cipla Ltd", "Fever", 270, 45.00, 35),

        # Pain Relief (12 medicines)
        ("Brufen 400mg", "Ibuprofen for pain", "Abbott", "Pain Relief", 350, 32.00, 45),
        ("Voveran 50mg", "Diclofenac pain relief", "Novartis", "Pain Relief", 280, 38.00, 38),
        ("Aceclofenac 100mg", "Joint pain relief", "Ipca Labs", "Pain Relief", 250, 28.00, 32),
        ("Piroxicam 20mg", "Long-acting pain relief", "Pfizer", "Pain Relief", 180, 45.00, 24),
        ("Tramadol 50mg", "Moderate pain relief", "Sun Pharma", "Pain Relief", 150, 85.00, 20),
        ("Ketorolac 10mg", "Strong pain relief", "Dr. Reddy's", "Pain Relief", 120, 55.00, 15),
        ("Etoricoxib 90mg", "Arthritis pain", "Merck", "Pain Relief", 200, 125.00, 28),
        ("Naproxen 250mg", "NSAID pain relief", "Cipla Ltd", "Pain Relief", 220, 35.00, 30),
        ("Indomethacin 25mg", "Anti-inflammatory", "Lupin", "Pain Relief", 160, 42.00, 22),
        ("Paracetamol + Ibuprofen Combo", "Dual pain relief", "Abbott", "Pain Relief", 300, 48.00, 40),
        ("Diclofenac Gel", "Topical pain relief", "Novartis", "Pain Relief", 250, 155.00, 35),
        ("Capsaicin Cream", "Muscle pain relief", "Himalaya", "Pain Relief", 180, 125.00, 25),

        # Vitamins (11 medicines)
        ("Vitamin D3 60000 IU", "Bone health supplement", "Lupin", "Vitamins", 400, 45.00, 50),
        ("B-Complex Tablets", "Energy and metabolism", "HealthKart", "Vitamins", 500, 85.00, 65),
        ("Vitamin C 1000mg", "Immunity booster", "Nature Made", "Vitamins", 450, 125.00, 58),
        ("Multivitamin Tablets", "Complete nutrition", "Centrum", "Vitamins", 380, 395.00, 48),
        ("Calcium + Vitamin D3", "Bone strength", "Shelcal", "Vitamins", 350, 185.00, 45),
        ("Iron + Folic Acid", "Anemia treatment", "Sun Pharma", "Vitamins", 320, 65.00, 42),
        ("Vitamin E 400 IU", "Antioxidant", "Nature's Bounty", "Vitamins", 280, 225.00, 38),
        ("Vitamin A 10000 IU", "Vision and immunity", "Solgar", "Vitamins", 250, 285.00, 32),
        ("Omega-3 Fish Oil", "Heart health", "Nordic Naturals", "Vitamins", 300, 845.00, 40),
        ("Biotin 10000mcg", "Hair and nail health", "Wow Life Science", "Vitamins", 420, 595.00, 55),
        ("Zinc 50mg", "Immune support", "Nature Made", "Vitamins", 380, 295.00, 48),

        # Women Hygiene (11 medicines)
        ("Clotrimazole Pessaries", "Vaginal infection treatment", "Glenmark", "Women Hygiene", 150, 125.00, 20),
        ("Metronidazole Vaginal Gel", "Bacterial vaginosis", "Cipla Ltd", "Women Hygiene", 130, 145.00, 18),
        ("Fluconazole 150mg", "Yeast infection", "Pfizer", "Women Hygiene", 200, 85.00, 28),
        ("Mefenamic Acid 500mg", "Menstrual pain relief", "Blue Cross", "Women Hygiene", 250, 45.00, 35),
        ("Tranexamic Acid 500mg", "Heavy menstrual bleeding", "Lupin", "Women Hygiene", 180, 125.00, 24),
        ("Norethisterone 5mg", "Menstrual regulation", "Abbott", "Women Hygiene", 120, 85.00, 15),
        ("Iron + Folic Acid Combo", "Pregnancy supplement", "Sun Pharma", "Women Hygiene", 300, 55.00, 40),
        ("Folic Acid 5mg", "Prenatal supplement", "Cipla Ltd", "Women Hygiene", 350, 25.00, 45),
        ("Calcium Supplements", "Pregnancy calcium", "Shelcal", "Women Hygiene", 280, 165.00, 38),
        ("Cranberry Extract", "UTI prevention", "Himalaya", "Women Hygiene", 220, 395.00, 30),
        ("Lactobacillus Probiotic", "Vaginal health", "Yakult", "Women Hygiene", 190, 285.00, 26),
    ]

    # Generate expiry dates (between 6 months to 3 years from now)
    medicines = []
    for index, (name, desc, mfr, cat, qty, price, reorder) in enumerate(medicines_data):
        expiry_days = random.randint(180, 1095)  # 6 months to 3 years
        expiry_date = datetime.now().date() + timedelta(days=expiry_days)

        medicine = Medicine(
            name=name,
            description=desc,
            manufacturer=mfr,
            category=cat,
            quantity=qty,
            price=price,
            expiry_date=expiry_date,
            stock=qty,
            reorder_level=reorder,
            barcode=generate_barcode(index + 1)
        )
        medicines.append(medicine)
        db.session.add(medicine)

    db.session.commit()
    print(f"✓ Created {len(medicines)} medicines")
    return medicines


def seed_alternatives():
    """Create alternative medicine mappings"""
    print("Creating alternative medicine mappings...")

    # Check if alternatives already exist
    if AlternativeMedicine.query.count() > 0:
        print("Alternatives already exist, skipping...")
        return

    # Common alternative mappings
    alternatives_map = [
        # Paracetamol alternatives (fever medicines)
        ("Dolo 650mg", ["Crocin 650mg", "Metacin 500mg", "Paracetamol 500mg"], "Same active ingredient: Paracetamol"),

        # Ibuprofen alternatives (pain relief)
        ("Brufen 400mg", ["Ibuprofen 400mg", "Ibuprofen Suspension"], "Same active ingredient: Ibuprofen"),

        # Cetirizine alternatives (allergy)
        ("Cetirizine 10mg", ["Levocetirizine 5mg", "Loratadine 10mg"], "Similar antihistamine effect"),

        # Diclofenac alternatives (pain)
        ("Voveran 50mg", ["Diclofenac 50mg", "Aceclofenac 100mg"], "Similar NSAID properties"),

        # Vitamin D alternatives
        ("Vitamin D3 60000 IU", ["Calcium + Vitamin D3"], "Contains Vitamin D"),
    ]

    for primary_name, alt_names, reason in alternatives_map:
        primary = Medicine.query.filter_by(name=primary_name).first()
        if not primary:
            continue

        for alt_name in alt_names:
            alt_medicine = Medicine.query.filter_by(name=alt_name).first()
            if alt_medicine and alt_medicine.medicine_id != primary.medicine_id:
                alternative = AlternativeMedicine(
                    primary_medicine_id=primary.medicine_id,
                    alternative_medicine_id=alt_medicine.medicine_id,
                    reason=reason,
                    priority=random.randint(5, 9)
                )
                db.session.add(alternative)

    db.session.commit()
    print("✓ Created alternative medicine mappings")


def main():
    """Main seeding function"""
    print("\n" + "="*60)
    print("  Warehouse Inventory Management System - Database Seeding")
    print("="*60 + "\n")

    app = create_app()
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        print("✓ Database tables created\n")

        # Seed data
        seed_users()
        medicines = seed_medicines()
        seed_alternatives()

        print("\n" + "="*60)
        print("  Database Seeding Complete!")
        print("="*60)
        print("\nDefault Login Credentials:")
        print("-" * 60)
        print("  Admin:")
        print("    Username: admin")
        print("    Password: admin123")
        print("\n  Staff:")
        print("    Username: staff")
        print("    Password: staff123")
        print("-" * 60)
        print(f"\nTotal Medicines Created: {Medicine.query.count()}")
        print(f"Total Users Created: {User.query.count()}")
        print(f"Total Alternatives Created: {AlternativeMedicine.query.count()}")
        print("\nYou can now run the application with: python app.py")
        print("="*60 + "\n")


if __name__ == '__main__':
    main()
