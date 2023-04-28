from django.db import models


class Branches(models.Model):
    bnumber = models.CharField(
        db_column='Bnumber', primary_key=True, max_length=100)
    baddress = models.CharField(
        db_column='Baddress', max_length=255, blank=True, null=True)
    city = models.CharField(
        db_column='City', max_length=255, blank=True, null=True)
    pincode = models.CharField(
        db_column='PinCode', max_length=255, blank=True, null=True)
    mobileno1 = models.BigIntegerField(db_column='MobileNo1')
    mobileno2 = models.BigIntegerField(
        db_column='MobileNo2', blank=True, null=True)
    mobileno3 = models.BigIntegerField(
        db_column='MobileNo3', blank=True, null=True)
    
    def __str__(self) -> str:
        return self.bnumber
    class Meta:
        managed = False
        db_table = 'branches'


class Clientrental(models.Model):
    cnumber = models.CharField(
        db_column='Cnumber', primary_key=True, max_length=100)
    cname = models.CharField(
        db_column='Cname', max_length=255, blank=True, null=True)
    caddress = models.CharField(
        db_column='Caddress', max_length=255, blank=True, null=True)
    manageno = models.ForeignKey(
        'Staff', models.DO_NOTHING, db_column='ManageNo', blank=True, null=True)
    brno = models.ForeignKey(Branches, models.DO_NOTHING,
                             db_column='Brno', blank=True, null=True)
    rdate = models.DateField(db_column='Rdate', blank=True, null=True)

    def __str__(self) -> str:
        return self.cnumber
    class Meta:
        managed = False
        db_table = 'clientRental'


class Lease(models.Model):
    leaseid = models.CharField(
        db_column='LeaseId', primary_key=True, max_length=255)
    cno = models.CharField(
        db_column='Cno', max_length=255, blank=True, null=True)
    pno = models.CharField(
        db_column='Pno', max_length=255, blank=True, null=True)
    mrent = models.FloatField(db_column='Mrent', blank=True, null=True)
    paymentmethod = models.CharField(
        db_column='PaymentMethod', max_length=255, blank=True, null=True)
    rdate = models.DateField(db_column='Rdate', blank=True, null=True)
    fdate = models.DateField(db_column='Fdate', blank=True, null=True)
    duration = models.FloatField(db_column='Duration', blank=True, null=True)
    deposit = models.CharField(
        db_column='Deposit', max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lease'

class Ownermanage(models.Model):
    ownno = models.CharField(
        db_column='OwnNo', primary_key=True, max_length=255)
    ownname = models.CharField(
        db_column='OwnName', max_length=255, blank=True, null=True)
    ownaddress = models.CharField(
        db_column='OwnAddress', max_length=255, blank=True, null=True)
    ownbusinesstype = models.CharField(
        db_column='OwnBusinessType', max_length=255, blank=True, null=True)
    ownmno = models.BigIntegerField(db_column='OwnMno', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ownerManage'

class Property(models.Model):
    pnumber = models.CharField(
        db_column='Pnumber', primary_key=True, max_length=100)
    ptype = models.CharField(
        db_column='PType', max_length=100, blank=True, null=True)
    rooms = models.IntegerField(db_column='Rooms', blank=True, null=True)
    rent = models.FloatField(db_column='Rent', blank=True, null=True)
    paddress = models.CharField(
        db_column='Paddress', max_length=255, blank=True, null=True)
    city = models.CharField(
        db_column='City', max_length=255, blank=True, null=True)
    pin = models.CharField(
        db_column='Pin', max_length=255, blank=True, null=True)
    ownno = models.ForeignKey(
        Ownermanage, models.DO_NOTHING, db_column='Ownno', blank=True, null=True)
    staffno = models.ForeignKey(
        'Staff', models.DO_NOTHING, db_column='StaffNo', blank=True, null=True)
    brno = models.ForeignKey(Branches, models.DO_NOTHING,
                             db_column='BrNo', blank=True, null=True)
    isavailable = models.IntegerField(db_column='isAvailable')
    hnumber = models.CharField(
        db_column='Hnumber', unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'property'

class Staff(models.Model):
    staffno = models.CharField(
        db_column='staffNo', primary_key=True, max_length=255)
    fname = models.CharField(max_length=255, blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    bdate = models.DateField(db_column='Bdate', blank=True, null=True)
    mno1 = models.BigIntegerField(db_column='Mno1')
    mno2 = models.BigIntegerField(db_column='Mno2', blank=True, null=True)
    mno3 = models.BigIntegerField(db_column='Mno3', blank=True, null=True)
    brno = models.ForeignKey(Branches, models.DO_NOTHING,
                             db_column='Brno', blank=True, null=True)
    salary = models.IntegerField(db_column='Salary', blank=True, null=True)
    sposition = models.CharField(
        db_column='SPosition', max_length=255, blank=True, null=True)
    super_id = models.CharField(
        db_column='Super_id', max_length=255, blank=True, null=True)
    bonus = models.IntegerField(db_column='Bonus', blank=True, null=True)
    start_date = models.DateField(
        db_column='Start_date', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staff'


class Invoice(models.Model):
    invoiceid = models.IntegerField(db_column='InvoiceId', primary_key=True, auto_created= True)
    pno = models.ForeignKey('Property', models.DO_NOTHING,
                            db_column='Pno', blank=True, null=True)
    cno = models.ForeignKey('clientrental', models.DO_NOTHING,
                            db_column='Cno', blank=True, null=True, related_name= 'clientrental')
    comments = models.CharField(
        db_column='Comments', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Invoice'
