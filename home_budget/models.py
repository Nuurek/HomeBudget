from django.db import models


class KategorieZakupu(models.Model):
    nazwa = models.CharField(primary_key=True, max_length=30)
    czy_opcjonalny = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'kategorie_zakupu'


class Paragony(models.Model):
    czas_zakupu = models.DateField()
    sklepy_adres = models.ForeignKey('Sklepy', models.DO_NOTHING, db_column='sklepy_adres')
    id = models.FloatField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'paragony'


class SieciSklepow(models.Model):
    nazwa = models.CharField(primary_key=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'sieci_sklepow'


class Sklepy(models.Model):
    adres = models.CharField(primary_key=True, max_length=60)
    sieci_sklepow_nazwa = models.ForeignKey(SieciSklepow, models.DO_NOTHING, db_column='sieci_sklepow_nazwa')

    class Meta:
        managed = False
        db_table = 'sklepy'


class Zakupy(models.Model):
    id = models.FloatField(primary_key=True)
    nazwa_produktu = models.CharField(max_length=30)
    cena_jednostkowa = models.FloatField()
    ilosc_produktu = models.FloatField()
    kategorie_zakupu_nazwa = models.ForeignKey(KategorieZakupu, models.DO_NOTHING, db_column='kategorie_zakupu_nazwa')
    paragony = models.ForeignKey(Paragony, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'zakupy'
