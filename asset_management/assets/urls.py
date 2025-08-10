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

    #telephone-related
    path('telephones/', views.all_telephones, name='all_telephones'),
    path('telephones/add/', views.create_telephone, name='create_telephone'),
    path('telephones/<int:telephone_id>/', views.telephone_details, name='telephone_details'),
    path('telephones/<int:telephone_id>/edit/', views.edit_telephone, name='edit_telephone'),
    path('telephones/unassign/<int:telephone_id>/<int:employee_id>/', views.unassign_telephone, name='unassign_telephone'),
    path('branches/<slug:slug>/telephones/', views.branch_telephones, name='branch_telephones'),
    path('logs/telephones/<slug:slug>/', views.all_telephone_log, name='all_telephones_log'),

    path('branches/<slug:slug>/upload-telephones/', views.upload_telephones, name='upload_telephones'),
    path('branches/<slug:slug>/extract-telephones/', views.extract_telephones_data, name='extract_telephones_bulk'),
    path('telephones/template/download/', views.download_telephones_template, name='download_telephones_template'),
    
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
    
    # Firewalls part
    path('firewalls/', views.all_firewalls, name='all_firewalls'),
    path('firewalls/add/', views.add_firewall, name='add_firewall'),
    path('firewalls/<int:firewall_id>/', views.firewall_details, name='firewall_details'),
    path('firewalls/<slug:slug>/', views.branch_firewalls, name='branch_firewalls'),
    path('firewalls/<int:firewall_id>/edit/', views.edit_firewall, name='edit_firewall'),
    path('logs/firewalls/<slug:slug>/', views.all_firewalls_log, name='all_firewalls_log'),
    path('branches/<slug:slug>/upload-firewalls/', views.upload_firewalls, name='upload_firewalls'),
    path('firewalls/template/download/', views.download_firewalls_template, name='download_firewalls_template'),
    path('branches/<slug:slug>/extract-firewalls/', views.extract_firewalls_data, name='extract_firewalls_bulk'),

    # switch part 
    # SWITCH ROUTES

    path('switches/', views.all_switches, name='all_switches'),
    path('switches/add/', views.create_switch, name='create_switch'),
    path('switches/<int:switch_id>/', views.switch_details, name='switch_details'),
    path('switches/<int:switch_id>/edit/', views.edit_switch, name='edit_switch'),
    path('branches/<slug:slug>/switches/', views.branch_switches, name='branch_switches'),
    path('logs/switches/<slug:slug>/', views.all_switch_log, name='all_switch_log'),
    path('branches/<slug:slug>/upload-switches/', views.upload_switches, name='upload_switches'),
    path('branches/<slug:slug>/extract-switches/', views.extract_switches_data, name='extract_switches_bulk'),
    path('switches/template/download/', views.download_switches_template, name='download_switches_template'),

    # Access Points
    path('access-points/', views.all_access_points, name='all_access_points'),
    path('access-points/add/', views.create_access_point, name='add_access_point'),
    path('access-points/<int:access_point_id>/', views.access_point_details, name='access_point_details'),
    path('access-points/<int:access_point_id>/edit/', views.edit_access_point, name='edit_access_point'),
    path('branches/<slug:slug>/access-points/', views.branch_access_points, name='branch_access_points'),
    path('logs/access-points/<slug:slug>/', views.all_access_point_log, name='all_access_point_logs'),
    path('branches/<slug:slug>/upload-access-points/', views.upload_access_points, name='upload_access_points'),
    path('branches/<slug:slug>/extract-access-points/', views.extract_access_points_data, name='extract_access_points_bulk'),
    path('access-points/template/download/', views.download_access_points_template, name='download_access_point_template'),

    # Routers
    path('routers/', views.all_routers, name='all_routers'),
    path('routers/add/', views.create_router, name='add_router'),
    path('routers/<int:router_id>/', views.router_details, name='router_details'),
    path('routers/<int:router_id>/edit/', views.edit_router, name='edit_router'),
    path('branches/<slug:slug>/routers/', views.branch_routers, name='branch_routers'),
    path('logs/routers/<slug:slug>/', views.all_router_log, name='all_router_logs'),
    path('branches/<slug:slug>/upload-routers/', views.upload_routers, name='upload_routers'),
    path('branches/<slug:slug>/extract-routers/', views.extract_routers_data, name='extract_routers_bulk'),
    path('routers/template/download/', views.download_routers_template, name='download_router_template'),
    
    # UPS
    path('ups/', views.all_ups, name='all_ups'),
    path('ups/add/', views.create_ups, name='add_ups'),
    path('ups/<int:ups_id>/', views.ups_details, name='ups_details'),
    path('ups/<int:ups_id>/edit/', views.edit_ups, name='edit_ups'),
    path('branches/<slug:slug>/ups/', views.branch_ups, name='branch_ups'),
    path('logs/ups/<slug:slug>/', views.all_ups_log, name='all_ups_logs'),
    path('branches/<slug:slug>/upload-ups/', views.upload_ups, name='upload_ups'),
    path('branches/<slug:slug>/extract-ups/', views.extract_ups_data, name='extract_ups_bulk'),
    path('ups/template/download/', views.download_ups_template, name='download_ups_template'),
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