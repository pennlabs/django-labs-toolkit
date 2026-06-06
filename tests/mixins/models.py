from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # implicit username, email, first_name, and last_name fields
    # from AbstractUser that contains the user's PennKey
    pennid = models.IntegerField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    preferred_name = models.CharField(max_length=225, blank=True)

    VERIFICATION_EXPIRATION_MINUTES = 10

    def get_preferred_name(self):
        if self.preferred_name != "":
            return self.preferred_name
        else:
            return self.first_name

    def get_email(self):
        email = self.emails.filter(primary=True).first()
        return email.value if email else ""

class School(models.Model):
    """
    Represents a school at the University of Pennsylvania.
    """

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Student(models.Model):
    """
    Represents a Student at the University of Pennsylvania.
    """

    user = models.OneToOneField(
        get_user_model(), related_name="student", on_delete=models.DO_NOTHING
    )
    major = models.ManyToManyField(Major, blank=True)
    school = models.ManyToManyField(School, blank=True)
    graduation_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1740)], null=True
    )

    def __str__(self):
        return self.user.username

