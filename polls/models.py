from django.db import models


# Create your models here.
class Data2(models.Model):
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )
    ProCode_CHOICES = (
        ('1868005', 'FB-Removal of Foreign Body from Brain'),
    )
    ProReason_CHOICES = (
        ('2470005', 'Brain damage'),
        ('2776000', 'Organic brain syndrome'),
        ('3119002', 'Brain stem laceration with open intracranial wound AND loss of consciousness'),
        ('4069002', 'Anoxic brain damage during AND/OR resulting from a procedure'),
    )
    ProOutcome_CHOICES = (
        ('385669000', 'Successful'),
        ('385671000', 'Unsuccessful'),
    )
    Gender = models.CharField(max_length = 20, choices = GENDER_CHOICES)
    ProcedureType = models.CharField(max_length = 120, choices= ProCode_CHOICES)
    ProcedureReason = models.CharField(max_length = 120, choices=ProReason_CHOICES)
    ProcedureOutcome = models.CharField(max_length = 120, choices=ProOutcome_CHOICES)



class Data(models.Model):
    AGE_CHOICES = (
        ('0-19', 'Under 20'),
        ('20-30', '20-30'),
        ('30-40', '30-40'),
        ('40-50', '40-50'),
        ('50-60', '50-60'),
        ('60-70', '60-70'),
        ('70-80', '70-80'),
        ('80-90', 'Over 80'),
    )
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )
    ProCode_CHOICES = (
        ('1868005', 'FB-Removal of Foreign Body from Brain'),
    )
    ProReason_CHOICES = (
        ('2470005', 'Brain damage'),
        ('2776000', 'Organic brain syndrome'),
        ('3119002', 'Brain stem laceration with open intracranial wound AND loss of consciousness'),
        ('4069002', 'Anoxic brain damage during AND/OR resulting from a procedure'),
    )
    ProOutcome_CHOICES = (
        ('385669000', 'Successful'),
        ('385671000', 'Unsuccessful'),
    )

    FirstName = models.CharField(max_length=120)  # max_length = required
    LastName = models.CharField(max_length=120)
    DateOfBirth = models.DateField()
    Age = models.CharField(max_length = 20, choices=AGE_CHOICES)
    Gender = models.CharField(max_length = 20, choices = GENDER_CHOICES)
    ProcedureType = models.CharField(max_length = 120, choices= ProCode_CHOICES)
    ProcedureReason = models.CharField(max_length = 120, choices=ProReason_CHOICES)
    ProcedureOutcome = models.CharField(max_length = 120, choices=ProOutcome_CHOICES)




