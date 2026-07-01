from django.db import models
from django.contrib.auth.models import AbstractUser
from pathlib import Path

# Create your models here.

class Login(AbstractUser):
    usertype=models.CharField(max_length=50,null=True)
    view_password=models.CharField(max_length=50,null=True)


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    image = models.FileField(null=True, upload_to="profile")
    loginId = models.ForeignKey(Login, on_delete=models.CASCADE, null=True) 
    medical_license_number = models.CharField(max_length=255,null=True)
    specialization=models.CharField(max_length=255,default="")

class Pharmacist(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    image = models.FileField(null=True, upload_to="profile")
    loginId = models.ForeignKey(Login, on_delete=models.CASCADE, null=True) 
    pharmacy_license_number = models.CharField(max_length=255,null=True)
    pharmacy_name = models.CharField(max_length=255,null=True)



class User(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=300, null=True)
    age = models.CharField(max_length=100,null=True)
    gender = models.CharField(max_length=100,null=True)
    image = models.FileField(null=True, upload_to="profile")
    loginId = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    blood_group=models.CharField(max_length=200,null=True) 
    # medical_prblm = models.CharField(max_length=500, null=True)


class CareChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="care_chat_sessions")
    linked_doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="care_chat_sessions",
    )
    title = models.CharField(max_length=255, blank=True)
    symptom_summary = models.TextField(blank=True)
    doctor_summary_override = models.TextField(blank=True)
    doctor_approved_summary = models.BooleanField(default=False)
    doctor_approved_medicine = models.BooleanField(default=False)
    structured_symptoms = models.CharField(max_length=255, blank=True)
    primary_intent = models.CharField(max_length=100, blank=True)
    recommended_specialty = models.CharField(max_length=120, blank=True)
    urgency_level = models.CharField(max_length=20, default="routine")
    last_user_message = models.TextField(blank=True)
    care_image = models.FileField(upload_to="care_chat_images", null=True, blank=True)
    visual_analysis_label = models.CharField(max_length=120, blank=True)
    visual_analysis_summary = models.TextField(blank=True)
    visual_analysis_details = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "-id"]


class CareChatMessage(models.Model):
    session = models.ForeignKey(CareChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20)
    text = models.TextField()
    sender_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name="care_chat_messages_sent")
    detected_intent = models.CharField(max_length=100, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    patient_read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]

    
class Medicine(models.Model):
    pid=models.ForeignKey(Pharmacist, on_delete=models.CASCADE, null=True)
    name=models.CharField(max_length=255)
    price=models.IntegerField()
    desc=models.CharField(max_length=255,null=True, blank=True)
    qty=models.IntegerField()
    image = models.FileField(null=True, upload_to="profile")
    date=models.DateField(null=True)
    expiry=models.DateField(null=True)
    side_effects=models.CharField(max_length=255,null=True)
    orginal_Price=models.IntegerField(null=True)

    GENERATED_PLACEHOLDER_IMAGES = {
        "medicine_antacid_suspension.png",
        "medicine_benzocaine_throat_lozenges.png",
        "medicine_carmellose_eye_drops.png",
        "medicine_cetirizine_10mg.png",
        "medicine_diclofenac_pain_relief_gel.png",
        "medicine_dopamine_injection.png",
        "medicine_doxylamie.png",
        "medicine_ibuprofen_400mg.png",
        "medicine_loratadine_10mg.png",
        "medicine_mefenamic_acid_500mg.png",
        "medicine_nitroglycerin.png",
        "medicine_omeprazole_20mg.png",
        "medicine_ors_sachet.png",
        "medicine_paracetamol_500mg.png",
        "medicine_saline_nasal_spray.png",
        "medicine_sodium_cromoglicate_eye_drops.png",
        "test_dopamine.png",
    }

    @property
    def image_name(self):
        return str(self.image or "").strip()

    @property
    def has_exact_image(self):
        image_name = Path(self.image_name).name.lower()
        if not image_name:
            return False
        return image_name not in self.GENERATED_PLACEHOLDER_IMAGES

    @property
    def display_image_url(self):
        if not self.has_exact_image:
            return "/static/assets/images/pharmacy/shop/medicine.jpg"

        image_name = self.image_name
        if image_name.startswith(("http://", "https://")):
            return image_name

        try:
            return self.image.url
        except Exception:
            return f"/assets/{image_name.lstrip('/')}"




class Appointments(models.Model):
    date=models.DateField()
    time=models.TimeField()
    desc=models.CharField(max_length=255,null=True, blank=True)
    status=models.CharField(max_length=255,null=True, blank=True)
    did=models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    uid=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    chat_session = models.ForeignKey(CareChatSession, on_delete=models.SET_NULL, null=True, blank=True)




class Prescription(models.Model):
    uid=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    pharmacist = models.ForeignKey(Pharmacist, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    medicines = models.CharField(max_length=100,null=True) 
    instructions = models.CharField(max_length=100,null=True) 
    status = models.CharField(max_length=100, default='Pending')



class MedicineOrder(models.Model):
    Pharmacist = models.ForeignKey(Pharmacist, on_delete=models.CASCADE, null=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mid = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='in_cart')
    qty = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    profit = models.IntegerField(null=True, blank=True)  # New field for profit tracking

    def save(self, *args, **kwargs):
        if self.mid and self.qty:
            # Calculate profit
            self.profit = (self.mid.price - self.mid.orginal_Price) * self.qty
        super(MedicineOrder, self).save(*args, **kwargs)



class Invoice(models.Model):
    invoice_no = models.CharField(max_length=20, unique=True, blank=True, null=True)
    pharmacist = models.ForeignKey(Pharmacist, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    medicine_order = models.ForeignKey(MedicineOrder, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)  # 1-5 rating
    date_submitted = models.DateTimeField(auto_now_add=True)

   
   
