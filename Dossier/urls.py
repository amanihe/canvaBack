
from django.urls import re_path
from Dossier import views
from django.urls import path

from django.conf.urls.static import static


urlpatterns = [


    re_path(r'^dossier/$', views.Crud_Dossier),
    re_path(r'^dossier/([0-9]+)$', views.Crud_Dossier),
    re_path(r'^get_dossier_Byparent/([0-9]+)$', views.get_dossier_Byparent),

    re_path(r'^rect/$', views.Crud_R),
    re_path(r'^rect/([0-9]+)$', views.Crud_R),
    re_path(r'^field/$', views.Crud_Field),
    re_path(r'^field/([0-9]+)$', views.Crud_Field),
    re_path(r'^link/$', views.Crud_Link),
    re_path(r'^link/([0-9]+)$', views.Crud_Link),
    re_path(r'^getLink_ByField/([0-9]+)$', views.getLink_ByField),
    re_path(r'^Link_By_FieldDossier/([0-9]+)/([0-9]+)$', views.getLink_ByFieldDossier),
    re_path(r'^Field_By_Rect/([0-9]+)$', views.Field_By_Rect),
    re_path(r'^Field_By_RectDossier/([0-9]+)/([0-9]+)$', views.Field_By_RectDossier),
    re_path(r'^Field_By_DossierParent/([0-9]+)/([0-9]+)$', views.Field_By_DossierParent),
    re_path(r'^delete_dossier_from_link/([0-9]+)/([0-9]+)$', views.delete_dossier_from_link),
    re_path(r'^delete_dossier_from_rect/([0-9]+)/([0-9]+)$', views.delete_dossier_from_rect),
    re_path(r'^rectdossier/$', views.add_dossier_to_rect),
    re_path(r'^fielddossier/$', views.add_dossier_to_Field),
    re_path(r'^add_dossier_to_link/$', views.add_dossier_to_Link),
    re_path(r'^getAllRectByParent/([0-9]+)$', views.getAllRectByParent),
    re_path(r'^getRectByDossier/([0-9]+)$', views.getRectByDossier),
    
    re_path(r'^drive/add_folder/$', views.add_folder),
   

    # re_path(r'^send$',views.send_email),

]
