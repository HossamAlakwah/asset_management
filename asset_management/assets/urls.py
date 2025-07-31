from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    # Branch-related
    path('branches/', views.branches_view, name='branches'),
    path('branches/<slug:slug>/', views.view_branch, name='view_branch'),
    path('branches/<slug:slug>/assets/', views.branch_assets, name='branch_assets'),
    path('employees/', views.employees_view, name='employees'),
    path('create_employee/', views.create_employee, name='create_employee'),
    path('edit_employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),    
    path('reports/', views.dynamic_report_view, name='dynamic_report'),
    path('report-fields/', views.get_model_fields, name='get_model_fields'),
    # Asset-related
    #Laptop and Desktop as assets
    path('all/', views.view_all, name='view_all'),
    path('all', views.all_assets, name='all_assets'),
    path('logs/<slug:slug>/', views.all_assets_log, name='all_assets_log'),
    path('assets/<int:asset_id>/', views.asset_details, name='asset_details'),
    path('assets/<int:asset_id>/edit/', views.edit_asset, name='edit_asset'),
    path('branches/<slug:slug>/upload-assets/', views.upload_assets, name='upload_assets_bulk'),
    path('branches/<slug:slug>/extract-assets/', views.extract_assets_data, name='extract_assets_bulk'),
    path('assets/add/', views.add_asset, name='add_asset'),
    path('assets/template/download/', views.download_asset_template, name='download_asset_template'),
    path('assets/unassign/<int:asset_id>/<int:employee_id>/', views.unassign_asset, name='unassign_asset'),
    path('assets/laptop-acknowledgment/', views.laptop_acknowledgment, name='laptop_acknowledgment'),
    
    # Screen-related
    path('screens/', views.all_screens, name='all_screens'),
    path('screens/add/', views.create_screen, name='create_screen'),
    path('screens/<int:screen_id>/', views.screen_details, name='screen_details'),
    path('screens/<int:screen_id>/edit/', views.edit_screen, name='edit_screen'),
    path('screens/unassign/<int:screen_id>/<int:employee_id>/', views.unassign_screen, name='unassign_screen'),

    path('branches/<slug:slug>/screens/', views.branch_screens, name='branch_screens'),
    path('logs/screens/<slug:slug>/', views.all_screen_log, name='all_screen_log'),

    path('branches/<slug:slug>/upload-screens/', views.upload_screens, name='upload_screens'),
    path('branches/<slug:slug>/extract-screens/', views.extract_screens_data, name='extract_screens_bulk'),
    path('screens/template/download/', views.download_screens_template, name='download_screens_template'),

    #Infra
    path('infra/', views.infrastructure_assets_view, name='infrastructure'),

    #Cameras part
    path('cameras/', views.all_cameras, name='all_cameras'),
    path('cameras/add/', views.add_camera, name='add_camera'),
    path('cameras/<int:camera_id>/', views.camera_details, name='camera_details'),
    path('cameras/<slug:slug>/', views.branch_cameras, name='branch_cameras'),
    path('cameras/<int:camera_id>/edit/', views.edit_camera, name='edit_camera'),
    path('logs/cameras/<slug:slug>/', views.all_cameras_log, name='all_cameras_log'),
    path('branches/<slug:slug>/upload-cameras/', views.upload_cameras, name='upload_cameras'),
    path('cameras/template/download/', views.download_cameras_template, name='download_cameras_template'),
    path('branches/<slug:slug>/extract-cameras/', views.extract_cameras_data, name='extract_cameras_bulk'),

    #NVR part
    path('nvrs/', views.all_nvrs, name='all_nvrs'),
    path('nvrs/add/', views.add_nvr, name='add_nvr'),
    path('nvrs/<int:nvr_id>/', views.nvr_details, name='nvr_details'),
    path('nvrs/<slug:slug>/', views.branch_nvrs, name='branch_nvrs'),
    path('nvrs/<int:nvr_id>/edit/', views.edit_nvr, name='edit_nvr'),

    path('logs/nvrs/<slug:slug>/', views.all_nvr_logs, name='all_nvrs_log'),

    path('branches/<slug:slug>/upload-nvrs/', views.upload_nvrs, name='upload_nvrs'),
    path('nvrs/template/download/', views.download_nvr_template, name='download_nvrs_template'),
    path('branches/<slug:slug>/extract-nvrs/', views.extract_nvrs_data, name='extract_nvrs_bulk'),
    # # Telecom-Access Related
    # path('telecom-access/', views.all_telecom_access, name='all_telecom_access'),
    # path('branches/<slug:slug>/telecom-access/', views.branch_telecom_access, name='branch_telecom_access'),
    # path('telecom-access/<int:item_id>/', views.telecom_access_details, name='telecom_access_details'),
    # path('telecom-access/<int:item_id>/edit/', views.edit_telecom_access, name='edit_telecom_access'),
    # path('logs/telecom-access/<slug:slug>/', views.all_telecom_access_log, name='all_telecom_access_log'),
    # path('branches/<slug:slug>/upload-telecom-access/', views.upload_Telecom_Access, name='upload_telecom_access_bulk'),
    # path('branches/<slug:slug>/extract-telecom-access/', views.extract_telecom_access_data, name='extract_telecom_access_bulk'),
    
    # # Cameras-Access Related

    # path('cameras/', views.all_cameras, name='all_cameras'),
    # path('branches/<slug:slug>/cameras/', views.branch_cameras, name='branch_cameras'),
    # path('cameras/<int:item_id>/', views.cameras_details, name='camera_details'),
    # path('cameras/<int:item_id>/edit/', views.edit_cameras, name='edit_cameras'),
    # path('logs/cameras/<slug:slug>/', views.all_cameras_log, name='all_cameras_log'),
    # path('branches/<slug:slug>/upload-cameras/', views.upload_cameras, name='upload_cameras_bulk'),
    # path('branches/<slug:slug>/extract-cameras/', views.extract_cameras_data, name='extract_cameras_bulk'),
    
    # # Network equipment

    # path('network_equipment/', views.all_network_equipment, name='all_network_equipment'),
    # # path('branches/<slug:slug>/network_equipment/', views.network_equipment, name='branch_network_equipment'),
    # # path('network_equipment/<int:item_id>/', views.network_equipment_details, name='network_equipment_details'),
    # # path('network_equipment/<int:item_id>/edit/', views.edit_network_equipment, name='edit_network_equipment'),
    # path('logs/network_equipment/<slug:slug>/', views.all_network_equipment_log, name='all_network_equipment_log'),
    # path('branches/<slug:slug>/upload-network_equipment/', views.upload_network_equipment, name='upload_network_equipment_bulk'),
    # path('branches/<slug:slug>/extract-network_equipment/', views.extract_network_equipment_data, name='extract_network_equipment_bulk'),
    # # Auth
    # path('consumables/', views.consumables_dashboard, name='consumables_dashboard'),
    # path('consumables/import/', views.import_consumables, name='import_consumables'),
    path('logout/', views.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)