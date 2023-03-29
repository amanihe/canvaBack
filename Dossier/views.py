from ctypes.wintypes import SERVICE_STATUS_HANDLE
from http.client import HTTPResponse
from multiprocessing import connection
from django.http import HttpResponse
from django.shortcuts import render
from Dossier.models import *
from Dossier.serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

@csrf_exempt
def add_folder(request):
    if request.method == 'POST':
        # Récupérer le fichier depuis le formulaire
        file = request.FILES['file']

        # Créer des informations d'identification à partir du fichier de clé JSON
        credentials = service_account.Credentials.from_service_account_file(
            'D:/canva/canvaBack/credentials.json',
            scopes=['https://www.googleapis.com/auth/drive']
        )

        # Créer un service Google Drive
        service = build('drive', 'v3', credentials=credentials)

        # Créer un dossier dans Google Drive
        folder_metadata = {'name': file.name, 'mimeType': 'application/vnd.google-apps.folder'}
        folder = service.files().create(body=folder_metadata, fields='id, webViewLink').execute()

        # Charger le contenu du fichier dans la mémoire
        media = MediaIoBaseUpload(file, mimetype=file.content_type, resumable=True)

        # Envoyer le fichier à Google Drive
        file_metadata = {'name': file.name, 'parents': [folder['id']]}
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        # Supprimer le fichier de la mémoire
        f = file.file
        f.close()
         

        permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': 'amanihedia00@gmail.com'
        }
        service.permissions().create(
            fileId=folder['id'],
            body=permission,
            sendNotificationEmail=False
        ).execute()
        # Retourner le lien de Drive
        name=file.name[:-4]
        return JsonResponse({'link': folder['webViewLink'],'name':name})

    # Si la méthode n'est pas POST
    return JsonResponse({'error': 'Méthode non autorisée'}) 

@csrf_exempt
def Crud_Link(request, id=0):
    if request.method == 'GET':
        link = T_Link.objects.all()
        link_serializer = S_Link(link, many=True)
        return JsonResponse(link_serializer.data, safe=False)
    elif request.method == 'POST':
        link_data = JSONParser().parse(request)
        link_serializer = S_Link(data=link_data)
        if link_serializer.is_valid():
            link_serializer.save()

            return JsonResponse("Added Successfully", safe=False)

        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        link_data = JSONParser().parse(request)
        link = T_Link.objects.get(Link_Id=link_data['Link_Id'])
        link_serializer = S_Link(
            link, data=link_data)
        if link_serializer.is_valid():
            link_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == 'DELETE':
        link = T_Link.objects.get(Link_Id=id)
        link.delete()
        return JsonResponse("Deleted Successfully", safe=False)
@csrf_exempt
def getLink_ByField(request, id):
    try:
        # Récupération des dossiers ayant le parent_id donné
        links = T_Link.objects.filter(Field_Id=id)
        # Sérialisation des données des dossiers
        serializer = S_Link(links, many=True)
        # Renvoi des données sérialisées en JSON
        return JsonResponse(serializer.data, safe=False)
    except:
        return JsonResponse({"error": "Une erreur s'est produite"}, status=500)


@csrf_exempt
def Crud_Dossier(request, id=0):
    if request.method == 'GET':
        dossier = T_Dossier.objects.all()
        dossier_serializer = S_Dossier(dossier, many=True)
        return JsonResponse(dossier_serializer.data, safe=False)
    elif request.method == 'POST':
        dossier_data = JSONParser().parse(request)
        dossier_serializer = S_Dossier(data=dossier_data)
        if dossier_serializer.is_valid():
            dossier_serializer.save()

            return JsonResponse("Added Successfully", safe=False)

        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        dossier_data = JSONParser().parse(request)
        dossier = T_Dossier.objects.get(Dossier_Id=dossier_data['Dossier_Id'])
        dossier_serializer = S_Dossier(
            dossier, data=dossier_data)
        if dossier_serializer.is_valid():
            dossier_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == 'DELETE':
        dossier = T_Dossier.objects.get(Dossier_Id=id)
        dossier.delete()
        return JsonResponse("Deleted Successfully", safe=False)


@csrf_exempt
def get_dossiers_by_parent(request, parent_id):
    try:
        # Récupération des dossiers ayant le parent_id donné
        dossiers = T_Dossier.objects.filter(Dossier_Parent=parent_id)
        # Sérialisation des données des dossiers
        serializer = S_Dossier(dossiers, many=True)
        # Renvoi des données sérialisées en JSON
        return JsonResponse(serializer.data, safe=False)
    except:
        return JsonResponse({"error": "Une erreur s'est produite"}, status=500)




@csrf_exempt
def get_dossier_Byparent(request, id):
    try:
        if int(id) == 0:
            dossiers = T_Dossier.objects.filter(Dossier_Parent__isnull=True)
        else:
            dossiers = T_Dossier.objects.filter(Dossier_Parent=id)
        serializer = S_Dossier(dossiers, many=True)
        return JsonResponse(serializer.data, safe=False)
    except:
        return HTTPResponse(status=404)


@csrf_exempt
def Crud_R(request, id=0):
    if request.method == 'GET':
        rect = T_Rect.objects.all()
        rect_serializer = S_Rect(rect, many=True)
        return JsonResponse(rect_serializer.data, safe=False)
    elif request.method == 'POST':
        rect_data = JSONParser().parse(request)
        dossier_id = rect_data.pop('Dossier_Id')
        dossier = T_Dossier.objects.get(Dossier_Id=dossier_id)
        rect = T_Rect.objects.create(**rect_data)
        rect.Dossier_Id.add(dossier)
        rect_serializer = S_Rect(rect)
        return JsonResponse(rect_serializer.data, safe=False)
    elif request.method == 'PUT':
        rect_data = JSONParser().parse(request)
        rect = T_Rect.objects.get(Rect_Id=rect_data['R_Id'])
        rect_serializer = S_Rect(rect, data=rect_data)
        if rect_serializer.is_valid():
            rect_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == 'DELETE':
        rect = T_Rect.objects.get(R_Id=id)
        rect.delete()
        return JsonResponse("Deleted Successfully", safe=False)


@csrf_exempt
def Crud_Field(request, id=0):
    if request.method == 'GET':
        field = T_Field.objects.all()
        field_serializer = S_Field(field, many=True)
        return JsonResponse(field_serializer.data, safe=False)
    elif request.method == 'POST':
        field_data = JSONParser().parse(request)
        dossier_id = field_data.pop('Dossier_Id')
        rect_id = field_data.pop('Rect_Id')
        dossier = T_Dossier.objects.get(Dossier_Id=dossier_id)
        rect = T_Rect.objects.get(R_Id=rect_id)
        field = T_Field.objects.create(Rect_Id=rect, **field_data)
        field.Dossier_Id.add(dossier)
        field_serializer = S_Field(field)
        return JsonResponse(field_serializer.data, safe=False)
    elif request.method == 'PUT':
        field_data = JSONParser().parse(request)
        field = T_Field.objects.get(Field_Id=field_data['Field_Id'])
        field_serializer = S_Field(rect, data=field_data)
        if field_serializer.is_valid():
            field_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == 'DELETE':
        rect = T_Field.objects.get(Field_Id=id)
        rect.delete()
        return JsonResponse("Deleted Successfully", safe=False)



@csrf_exempt
def add_dossier_to_rect(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            rect = T_Rect.objects.get(R_Id=data["R_Id"])
            dossier = T_Dossier.objects.get(Dossier_Id=data["Dossier_Id"])
            rect.Dossier_Id.add(dossier)
            return JsonResponse({"status": "success"})
        except T_Rect.DoesNotExist:
            return JsonResponse({"status": f'T_Rect object with R_Id={data["R_Id"]} does not exist'}, status=400)
        except T_Dossier.DoesNotExist:
            return JsonResponse({"status": f'T_Dossier object with Dossier_Id={data["Dossier_Id"]} does not exist'}, status=400)
    return JsonResponse({"status": "failed"})

@csrf_exempt
def add_dossier_to_Field(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            field = T_Field.objects.get(Field_Id=data["Field_Id"])
            dossier = T_Dossier.objects.get(Dossier_Id=data["Dossier_Id"])
            field.Dossier_Id.add(dossier)
            return JsonResponse({"status": "success"})
        except T_Field.DoesNotExist:
            return JsonResponse({"status": f'T_Field object with Field_Id={data["Field_Id"]} does not exist'}, status=400)
        except T_Dossier.DoesNotExist:
            return JsonResponse({"status": f'T_Dossier object with Dossier_Id={data["Dossier_Id"]} does not exist'}, status=400)
    return JsonResponse({"status": "failed"})


@csrf_exempt
def Field_By_Rect(request, id):
    try:
        field = T_Field.objects.filter(Rect_Id=id)
        if request.method == 'GET':
            serializer = S_Field(field, many=True)
            return JsonResponse(serializer.data, safe=False)
    except:
        return HTTPResponse(status=404)


@csrf_exempt
def Field_By_RectDossier(request, idRect, idDossier):
   
    try:
        field = T_Field.objects.filter(
            Rect_Id=idRect, Dossier_Id=idDossier)
        if request.method == 'GET':
            serializer = S_Field(field, many=True)
            return JsonResponse(serializer.data, safe=False)
    except:
        return HTTPResponse(status=404)


@csrf_exempt
def getAllRectByParent(request, id):
    try:
        dossiers = T_Dossier.objects.filter(
            Dossier_Id=id) | T_Dossier.objects.filter(Dossier_Parent=id)
        serializer = S_Dossier(dossiers, many=True)
        T = []
        for L in serializer.data:
            rect = T_Rect.objects.filter(
                Dossier_Id=L["Dossier_Id"])
            if request.method == 'GET':
                ser = S_Rect(rect, many=True)
                for rect_data in ser.data:
                    # Compare seulement l'id du rectangle
                    if rect_data['R_Id'] not in [r['R_Id'] for r in T]:
                        T.append(rect_data)
        print(T)
        return JsonResponse(T, safe=False)
    except:
        return HttpResponse(status=404)


@csrf_exempt
def getRectByDossier(request, id):
    try:
        rect = T_Rect.objects.filter(Dossier_Id=id)
        if request.method == 'GET':
            serializer = S_Rect(rect, many=True)
            return JsonResponse(serializer.data, safe=False)
    except:
        return HTTPResponse(status=404)
