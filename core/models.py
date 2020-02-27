from django.db import models


class Profession(models.Model):
    description=models.CharField(max_length=50)
    @property
    def status(self):
        return True
    def __str__(self):
        return self.description



class Datesheet(models.Model):
    description=models.CharField(max_length=50)
    historical_date=models.TextField()
    def __str__(self):
        return self.description


class Customer(models.Model):
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    profession=models.ManyToManyField(Profession)
    date_sheet=models.OneToOneField(Datesheet,on_delete=models.CASCADE)
    active=models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Documents(models.Model):
    PP='PP'
    ID='ID'
    OT='OT'
    DOC_TYPES=(
        (PP,'Passport'),
        (ID,'Identity card'),
        (OT,'Others')
    )

    dtype=models.CharField(max_length=2)
    doc_number=models.CharField(max_length=50)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)

    def __str__(self):
        return self.doc_number
