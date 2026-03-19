
from django.db import models

# Dynamic Form
class Form(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Field(models.Model):
    FIELD_TYPES = (
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('password', 'Password'),
    )

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="fields")
    label = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label


# Employee
class Employee(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class EmployeeData(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="data")
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    value = models.TextField()

    def __str__(self):
        return f"{self.employee.name} - {self.field.label}"