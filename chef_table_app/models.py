from django.db import models

class login_table(models.Model):
    username=models.CharField(max_length=220)
    password=models.CharField(max_length=20)
    type=models.CharField(max_length=20)


class UserTable(models.Model):
    LOGIN = models.ForeignKey('login_table', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=100)
    place = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)
    house_number = models.CharField(max_length=20)
    phone = models.BigIntegerField()
    email = models.EmailField(max_length=254)
    image = models.FileField()

class ChefTable(models.Model):
    LOGIN = models.ForeignKey('login_table', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=100)
    place = models.CharField(max_length=50)
    Qualification = models.CharField(max_length=50)
    Experience = models.CharField(max_length=20)
    phone = models.BigIntegerField()
    email = models.EmailField(max_length=254)
    image = models.FileField()

class FoodTable(models.Model):
    CHEF = models.ForeignKey(ChefTable, on_delete=models.CASCADE)
    Cuisine = models.CharField(max_length=50)
    Type = models.CharField(max_length=50)
    Name = models.CharField(max_length=50)
    Details = models.TextField()
    Meals = models.CharField(max_length=50)
    Price = models.CharField(max_length=50)
    Image = models.FileField()
    Date = models.DateField()

class ScheduleTable(models.Model):
    CHEF = models.ForeignKey(ChefTable, on_delete=models.CASCADE)
    From_time = models.CharField(max_length=50)
    To_time = models.CharField(max_length=50)
    date = models.DateField()

class BookingTable(models.Model):
    CHEF = models.ForeignKey(ChefTable, on_delete=models.CASCADE)
    USER = models.ForeignKey(UserTable, on_delete=models.CASCADE)

    number_gas = models.CharField(max_length=50)
    Status = models.CharField(max_length=50)
    Date = models.CharField(max_length=50)
    # Date = models.DateField()


class BookingTable1(models.Model):
    BOOKING = models.ForeignKey(BookingTable, on_delete=models.CASCADE)
    mealstype = models.CharField(max_length=50)
    serving_time = models.CharField(max_length=50)
#
class BookingDetailsTable(models.Model):
    BOOKING = models.ForeignKey(BookingTable, on_delete=models.CASCADE)
    FOOD = models.ForeignKey(FoodTable, on_delete=models.CASCADE)
#
class Events(models.Model):
    event=models.CharField(max_length=100)
#



