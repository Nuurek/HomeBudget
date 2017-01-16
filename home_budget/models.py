from django.db import models


class KategorieZakupu(models.Model):
    id = models.IntegerField(primary_key=True)
    nazwa = models.CharField(max_length=30)
    czy_opcjonalny = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'kategorie_zakupu'

    def __str__(self):
        return self.nazwa


class Paragony(models.Model):
    czas_zakupu = models.DateField()
    sklepy_id = models.ForeignKey(
        'Sklepy', models.DO_NOTHING, db_column='sklepy_id'
    )
    # id = models.FloatField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'paragony'

    def __str__(self):
        name = self.czas_zakupu.strftime("%d-%m-%Y")
        name += ' - ' + str(self.sklepy_id)
        return name


class SieciSklepow(models.Model):
    nazwa = models.CharField(primary_key=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'sieci_sklepow'

    def __str__(self):
        return self.nazwa


class Sklepy(models.Model):
    # id = models.IntegerField(primary_key=True)
    adres = models.CharField(max_length=60)
    sieci_sklepow_nazwa = models.ForeignKey(
        SieciSklepow, models.DO_NOTHING, db_column='sieci_sklepow_nazwa')

    class Meta:
        managed = False
        db_table = 'sklepy'

    def __str__(self):
        return self.adres


class Zakupy(models.Model):
    # id = models.FloatField(primary_key=True)
    nazwa_produktu = models.CharField(max_length=100)
    cena_jednostkowa = models.FloatField()
    ilosc_produktu = models.FloatField()
    kategorie_zakupu_id = models.ForeignKey(
        KategorieZakupu, models.DO_NOTHING, db_column='kategorie_zakupu_id')
    paragony = models.ForeignKey(Paragony, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'zakupy'

    def __str__(self):
        name = self.nazwa_produktu + ' '
        name += str(self.ilosc_produktu * float(self.cena_jednostkowa)) + 'zł'
        return name
