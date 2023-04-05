from django.db import models

# Create your models here.


class T_Dossier(models.Model):#p1/p2 #projet 
    Dossier_Id = models.AutoField(primary_key=True)
    Dossier_Name = models.CharField(max_length=100)
    Dossier_Parent = models.ForeignKey(
        "self", null=True, default=None, blank=True, related_name="children", on_delete=models.CASCADE)

class T_Rect(models.Model):#marketing/revenu  
    R_Id = models.AutoField(primary_key=True)
    R_Name = models.CharField(max_length=100)
    Dossier_Id=models.ManyToManyField(T_Dossier)

class T_Field(models.Model):#facebook  #dossier 
    Field_Id = models.AutoField(primary_key=True)
    Field_Name = models.CharField(max_length=100)
    Rect_Id=models.ForeignKey(T_Rect,on_delete=models.CASCADE)
    Dossier_Id=models.ManyToManyField(T_Dossier)
 #models.ForeignKey(
    #    "self", null=True, default=None, blank=True, related_name="children", on_delete=models.CASCADE)
class T_Link(models.Model):#chapitre
    Link_Id=models.AutoField(primary_key=True)
    Link_Name=models.CharField(max_length=100)
    Link_Url=models.CharField(max_length=100)
    Field_Id=models.ForeignKey(T_Field,on_delete=models.CASCADE)
    Dossier_Id=models.ManyToManyField(T_Dossier)
    