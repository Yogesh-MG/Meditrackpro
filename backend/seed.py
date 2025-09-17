import random
import uuid
from faker import Faker
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import qrcode
from io import BytesIO
from django.core.files import File
import os
from hospitals.models import Hospital, Subscription
from employees.models import Employee
from device.models import Device, ServiceLog, Specification, Documentation, Calibration, IncidentReport
from inventory.models import Category, Unit, InventoryItem
from suppliers.models import Supplier, PurchaseOrder, PurchaseOrderItem
from tickets.models import Ticket, TicketComment
from compliance.models import ComplianceStandard, Audit, ComplianceDocument
from patient.models import Patient, EmergencyContact, Vital, MedicalHistory, Medication, Appointment
from django.conf import settings

# Initialize Faker
fake = Faker()

# Ensure media directory exists
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', 'media')
os.makedirs(MEDIA_ROOT, exist_ok=True)

def create_dummy_file(filename):
    """Create a dummy file for FileField."""
    file_path = os.path.join(MEDIA_ROOT, filename)
    try:
        with open(file_path, 'w') as f:
            f.write("Dummy content for " + filename)
        return File(open(file_path, 'rb'), name=filename)
    except Exception as e:
        print(f"Error creating dummy file {filename}: {e}")
        return None

def seed_data():
    print("Starting database seeding...")
    # Clear existing data in reverse dependency order
    models_to_clear = [
        ComplianceDocument, Audit, ComplianceStandard,
        TicketComment, Ticket,
        PurchaseOrderItem, PurchaseOrder, Supplier,
        InventoryItem, Unit, Category,
        IncidentReport, Calibration, Documentation, Specification, ServiceLog, Device,
        Appointment, Medication, MedicalHistory, Vital, EmergencyContact, Patient,
        Employee, Subscription, Hospital,
        User
    ]
    for model in models_to_clear:
        if model == User:
            model.objects.exclude(is_superuser=True).delete()
        else:
            model.objects.all().delete()
    print("Existing data cleared.")

    # Create superuser for hospital admins
    try:
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@meditrackpro.com',
            password='admin123',
            first_name='Super',
            last_name='Admin'
        )
        print("Superuser created.")
    except Exception as e:
        print(f"Error creating superuser: {e}")
        superuser = User.objects.get(username='admin')

    # Lists to store created objects for relationships
    hospitals = []
    employees = []
    devices = []
    categories = []
    units = []
    inventory_items = []
    suppliers = []
    patients = []

    # Create 5 Hospitals
    for i in range(5):
        try:
            hospital = Hospital.objects.create(
                name=fake.company() + f" Hospital {i+1}",
                hospital_type=random.choice(['General', 'Specialty', 'Clinic']),
                address=fake.address(),
                city=fake.city(),
                state=fake.state(),
                zipcode=fake.zipcode(),
                phone_number=fake.phone_number()[:15],
                email=fake.email(),
                admin=superuser,
                plan=random.choice(['basic', 'pro', 'premium']),
                payment_method=random.choice(['prepaid', 'cod', 'direct']),
                is_active=True,
                gstin=fake.bothify(text='??############?')
            )
            hospitals.append(hospital)
            print(f"Created hospital: {hospital.name}")

            # Create Subscription
            Subscription.objects.create(
                hospital=hospital,
                plan=hospital.plan,
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(days=365),
                payment_status=random.choice(['pending', 'paid', 'overdue']),
                base_amount=random.uniform(4999, 19999),
                gst_amount=random.uniform(899, 3599),
                total_amount=random.uniform(5898, 23598)
            )

            # Create 10 Employees, ensuring at least one engineer
            roles = ['doctor', 'nurse', 'staff', 'receptionist', 'other']
            for j in range(10):
                role = 'engineer' if j == 0 else random.choice(roles)
                username = fake.email()
                user = User.objects.create_user(
                    username=username,
                    email=username,
                    password='password123',
                    first_name=fake.first_name(),
                    last_name=fake.last_name()
                )
                employee = Employee.objects.create(
                    user=user,
                    hospital=hospital,
                    role=role,
                    department=random.choice(['cardiology', 'neurology', 'pediatrics', 'orthopedics', 'radiology', 'emergency', 'it', 'administration']),
                    phone_number=fake.phone_number()[:15],
                    access_level=random.choice(['admin', 'full', 'standard', 'limited', 'none']),
                    status=random.choice(['active', 'inactive']),
                    date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=70),
                    employee_id=f"H{hospital.id}-EMP{j+1:03d}"
                )
                employees.append(employee)
            print(f"Created {len([e for e in employees if e.hospital == hospital and e.role == 'engineer'])} engineers for hospital {hospital.id}")

            # Create 10 Patients
            doctors = [e for e in employees if e.hospital == hospital and e.role == 'doctor']
            for j in range(10):
                # Randomly decide if insurance details should be included (50% chance)
                include_insurance = random.choice([True, False])
                patient = Patient.objects.create(
                    hospital=hospital,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=80),
                    gender=random.choice(['male', 'female', 'other']),
                    email=fake.email(),
                    phone_number=fake.phone_number()[:15],
                    address=fake.street_address(),
                    city=fake.city(),
                    state=fake.state(),
                    postal_code=fake.zipcode(),
                    country='India',
                    blood_type=random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
                    height=random.uniform(150, 200),
                    weight=random.uniform(50, 120),
                    primary_physician=random.choice(doctors) if doctors else None,
                    allergies=', '.join(fake.words(nb=random.randint(0, 3), unique=True)) if random.choice([True, False]) else None,
                    medical_conditions=', '.join(fake.words(nb=random.randint(0, 3), unique=True)) if random.choice([True, False]) else None,
                    medication=', '.join(fake.words(nb=random.randint(0, 3), unique=True)) if random.choice([True, False]) else None,
                    insurance_provider=fake.company() if include_insurance else None,
                    policy_number=fake.bothify(text='POL####-#####') if include_insurance else None,
                    group_number=fake.bothify(text='GRP####') if include_insurance else None,
                    policy_holder=fake.name() if include_insurance else None,
                    relationship_to_holder=random.choice(['self', 'spouse', 'child', 'other']) if include_insurance else None,
                    coverage_start_date=fake.date_between(start_date='-2y', end_date='today') if include_insurance else None,
                    coverage_end_date=fake.date_between(start_date='today', end_date='+2y') if include_insurance else None,
                    has_secondary_insurance=random.choice([True, False]) if include_insurance else False,
                    status=random.choice(['Active', 'Inactive']),
                    last_visit=fake.date_between(start_date='-1y', end_date='today')
                )
                patients.append(patient)
                print(f"Created patient: {patient.patient_id} for hospital {hospital.id}")

                # Create 1-2 Emergency Contacts
                for _ in range(random.randint(1, 2)):
                    EmergencyContact.objects.create(
                        patient=patient,
                        name=fake.name(),
                        relationship=random.choice(['spouse', 'parent', 'child', 'sibling', 'friend']),
                        phone=fake.phone_number()[:15]
                    )

                # Create 1-3 Vitals
                for _ in range(random.randint(1, 3)):
                    Vital.objects.create(
                        patient=patient,
                        heart_rate=random.randint(60, 100),
                        blood_pressure=f"{random.randint(100, 140)}/{random.randint(60, 90)}",
                        temperature=random.uniform(97.0, 99.5),
                        respiratory_rate=random.randint(12, 20),
                        oxygen_saturation=random.randint(95, 100),
                        recorded_at=fake.date_time_between(start_date='-1y', end_date='now')
                    )

                # Create 1-3 Medical History Records
                for _ in range(random.randint(1, 3)):
                    MedicalHistory.objects.create(
                        patient=patient,
                        condition=fake.word().capitalize(),
                        diagnosed_date=fake.date_between(start_date='-5y', end_date='today'),
                        status=random.choice(['Active', 'Controlled', 'Resolved']),
                        notes=fake.text(max_nb_chars=200)
                    )

                # Create 1-3 Medications
                for _ in range(random.randint(1, 3)):
                    Medication.objects.create(
                        patient=patient,
                        name=fake.word().capitalize(),
                        dosage=f"{random.randint(5, 500)}mg",
                        frequency=random.choice(['Once daily', 'Twice daily', 'As needed']),
                        prescribed_by=random.choice(doctors) if doctors else None,
                        start_date=fake.date_between(start_date='-1y', end_date='today'),
                        end_date=fake.date_between(start_date='today', end_date='+1y') if random.choice([True, False]) else None
                    )

                # Create 1-3 Appointments
                for _ in range(random.randint(1, 3)):
                    Appointment.objects.create(
                        patient=patient,
                        doctor=random.choice(doctors) if doctors else None,
                        appointment_date=fake.date_between(start_date='-1y', end_date='+30d'),
                        appointment_time=fake.time(),
                        type=random.choice(['Consultation', 'Follow-up', 'Procedure']),
                        status=random.choice(['Scheduled', 'Completed', 'Canceled']),
                        notes=fake.text(max_nb_chars=200)
                    )

            # Create 10 Categories
            for j in range(10):
                category = Category.objects.create(
                    hospital=hospital,
                    name=f"Category {j+1} - {fake.word().capitalize()}"
                )
                categories.append(category)

            # Create 5 Units
            for j in range(5):
                unit = Unit.objects.create(
                    hospital=hospital,
                    name=f"Unit {j+1} - {fake.word().capitalize()}"
                )
                units.append(unit)

            # Create 50 Inventory Items
            for j in range(50):
                item = InventoryItem.objects.create(
                    hospital=hospital,
                    name=fake.word().capitalize() + f" Item {j+1}",
                    category=random.choice(categories),
                    quantity=random.randint(1, 100),
                    unit=random.choice(units),
                    reorder_level=random.randint(5, 20),
                    expiry_date=fake.date_between(start_date='today', end_date='+2y'),
                    location=fake.word().capitalize() + " Storage",
                    sku=f"H{hospital.id}-SKU{j+1:04d}",
                    barcode=fake.ean13(),
                    cost=random.uniform(10, 1000),
                    tax=random.uniform(0, 18),
                    batch=fake.bothify(text='BAT####'),
                    description=fake.text(max_nb_chars=200)
                )
                inventory_items.append(item)

            # Create 10 Suppliers
            for j in range(10):
                supplier = Supplier.objects.create(
                    hospital=hospital,
                    name=fake.company() + f" Supplier {j+1}",
                    contact_name=fake.name(),
                    contact_email=fake.email(),
                    contact_phone=fake.phone_number()[:20],
                    address=fake.address(),
                    reliability_score=random.randint(1, 100),
                    status=random.choice(['Active', 'OnHold', 'Inactive']),
                    tax_id=fake.bothify(text='TAX####'),
                    website=fake.url(),
                    supplier_type=fake.word().capitalize(),
                    payment_terms=random.choice(['Net 30', 'Net 60', 'COD']),
                    currency='INR',
                    approved=True
                )
                supplier.categories.set(random.sample(categories, random.randint(1, 5)))
                suppliers.append(supplier)

            # Create 20 Devices
            for j in range(20):
                nfc_uuid = str(uuid.uuid4())
                device = Device.objects.create(
                    hospital=hospital,
                    name=fake.word().capitalize() + f" Device {j+1}",
                    make_model=fake.word().capitalize() + " Model",
                    manufacture=fake.company(),
                    serial_number=f"H{hospital.id}-SER{j+1:04d}",
                    nfc_uuid=nfc_uuid,
                    date_of_installation=fake.date_between(start_date='-5y', end_date='today'),
                    warranty_until=fake.date_between(start_date='today', end_date='+3y'),
                    asset_number=f"H{hospital.id}-AST{j+1:04d}",
                    asset_details=random.choice(['Excellent', 'Poor']),
                    is_active=random.choice(['Operational', 'Needs_Calibration', 'Under_Maintenance']),
                    department=random.choice(['cardiology', 'neurology', 'pediatrics', 'orthopedics', 'radiology', 'emergency', 'it', 'administration']),
                    Room=f"Room {j+1}",
                    next_calibration=fake.date_between(start_date='today', end_date='+1y')
                )
                devices.append(device)

                engineers = [e for e in employees if e.hospital == hospital and e.role == 'engineer']
                ServiceLog.objects.create(
                    device=device,
                    service_date=fake.date_between(start_date='-1y', end_date='today'),
                    service_type=fake.word().capitalize(),
                    engineer=random.choice(engineers if engineers else [e for e in employees if e.hospital == hospital]),
                    service_details=fake.text(max_nb_chars=200),
                    status=random.choice(['scheduled', 'completed', 'overdue']),
                    document=create_dummy_file(f"service_log_{device.id}.txt")
                )

                Specification.objects.create(
                    device=device,
                    power_supply=fake.word().capitalize(),
                    battery_type=fake.word().capitalize(),
                    battery_life=f"{random.randint(1, 24)} hours",
                    weight=f"{random.uniform(1, 50):.2f} kg",
                    dimensions=f"{random.randint(10, 100)}x{random.randint(10, 100)}x{random.randint(10, 100)} cm",
                    conncetivity_options=fake.word().capitalize(),
                    certifications=fake.word().capitalize()
                )

                Documentation.objects.create(
                    device=device,
                    document=fake.word().capitalize() + " Manual",
                    types=fake.word().capitalize(),
                    storage_location=fake.file_path(depth=3)
                )

                Calibration.objects.create(
                    device=device,
                    calibration_date=timezone.now(),
                    next_calibration=fake.date_between(start_date='today', end_date='+1y'),
                    result=fake.word().capitalize(),
                    notes=fake.text(max_nb_chars=200),
                    engineer=random.choice(engineers if engineers else [e for e in employees if e.hospital == hospital]),
                    status=random.choice(['scheduled', 'completed', 'overdue']),
                    document=create_dummy_file(f"calibration_{device.id}.txt")
                )

                IncidentReport.objects.create(
                    device=device,
                    incident_type=random.choice([t[0] for t in IncidentReport.INCIDENT_TYPES]),
                    description=fake.text(max_nb_chars=200),
                    reported_by=random.choice([e for e in employees if e.hospital == hospital]),
                    related_employee=random.choice([e for e in employees if e.hospital == hospital])
                )

            # Create 10 Purchase Orders
            for j in range(10):
                po = PurchaseOrder.objects.create(
                    hospital=hospital,
                    supplier=random.choice([s for s in suppliers if s.hospital == hospital]),
                    status=random.choice(['DRAFT', 'SUBMITTED', 'RECEIVED', 'CANCELLED']),
                    order_date=timezone.now(),
                    expected_delivery=fake.date_between(start_date='today', end_date='+30d'),
                    notes=fake.text(max_nb_chars=200)
                )
                for _ in range(random.randint(1, 5)):
                    PurchaseOrderItem.objects.create(
                        purchase_order=po,
                        inventory_item=random.choice([item for item in inventory_items if item.hospital == hospital]),
                        quantity=random.randint(1, 50),
                        unit_price=random.uniform(10, 1000),
                        received_quantity=random.randint(0, 50)
                    )

            # Create 20 Tickets
            for j in range(20):
                try:
                    ticket = Ticket.objects.create(
                        hospital=hospital,
                        title=fake.sentence(nb_words=5),
                        device=random.choice([d for d in devices if d.hospital == hospital]),
                        category=random.choice([c[0] for c in Ticket.CATEGORY_CHOICES]),
                        priority=random.choice([p[0] for p in Ticket.PRIORITY_CHOICES]),
                        status=random.choice([s[0] for s in Ticket.STATUS_CHOICES]),
                        location=fake.word().capitalize() + " Room",
                        created_by=random.choice([e for e in employees if e.hospital == hospital]),
                        assigned_to=random.choice(engineers if engineers else [e for e in employees if e.hospital == hospital]),
                        description=fake.text(max_nb_chars=200)
                    )
                    print(f"Created ticket: {ticket.ticket_id} for hospital {hospital.id}")
                    for _ in range(random.randint(1, 3)):
                        TicketComment.objects.create(
                            ticket=ticket,
                            author=random.choice([e for e in employees if e.hospital == hospital]),
                            content=fake.text(max_nb_chars=200),
                            file=create_dummy_file(f"ticket_comment_{ticket.id}.txt")
                        )
                except Exception as e:
                    print(f"Error creating ticket: {e}")

            # Create 5 Compliance Standards
            for j in range(5):
                standard = ComplianceStandard.objects.create(
                    hospital=hospital,
                    name=f"Standard {j+1} - {fake.word().capitalize()}",
                    status=random.choice(['Compliant', 'Pending Review', 'Require Attention']),
                    progress=random.randint(0, 100),
                    last_audit_date=fake.date_time_between(start_date='-1y', end_date='now'),
                    next_audit_date=fake.date_time_between(start_date='now', end_date='+1y')
                )
                for _ in range(random.randint(1, 3)):
                    Audit.objects.create(
                        hospital=hospital,
                        Compliance_standard=standard,
                        title=fake.sentence(nb_words=4),
                        audit_date=fake.date_between(start_date='today', end_date='+1y'),
                        status=random.choice(['Scheduled', 'Pending', 'Completed']),
                        auditor=fake.name(),
                        notes=fake.text(max_nb_chars=200)
                    )
                for _ in range(random.randint(1, 3)):
                    ComplianceDocument.objects.create(
                        hospital=hospital,
                        Compliance_standard=standard,
                        name=fake.word().capitalize() + " Document",
                        file=create_dummy_file(f"compliance_doc_{standard.id}.txt"),
                        status=random.choice(['Complete', 'In Progress', 'Require Attention'])
                    )

        except Exception as e:
            print(f"Error in hospital {i+1}: {e}")

    print("Database seeded successfully!")

# Management command boilerplate
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Seed the database with dummy data'

    def handle(self, *args, **kwargs):
        seed_data()
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))