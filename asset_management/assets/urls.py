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
    
    # Raya Data Center
    path('raya-data-center/', views.all_raya_vms, name='all_raya_vms'),
    path('raya-data-center/add/', views.create_raya_vm, name='add_raya_vm'),
    path('raya-data-center/<int:vm_id>/', views.raya_vm_details, name='raya_vm_details'),
    path('raya-data-center/<int:vm_id>/edit/', views.edit_raya_vm, name='edit_raya_vm'),
    path('branches/<slug:slug>/upload-vms/', views.upload_raya_vms, name='upload_raya_vms'),
    path('raya-data-center/extract-vms/', views.extract_vm_data, name='extract_vms_bulk'),
    path('raya-data-center/template/download/', views.download_raya_vm_template, name='download_raya_vm_template'),
    
    # === ZK Devices ===
    path('zks', views.all_zk_devices, name='all_zk_devices'),
    path('zk/logs/<slug:slug>/', views.zk_device_logs, name='zk_device_logs'),
    path('zk/<int:device_id>/', views.zk_device_details, name='zk_details'),
    path('zk/<int:device_id>/edit/', views.edit_zk_device, name='edit_zk'),
    path('branches/<slug:slug>/upload-zk/', views.upload_zk_devices, name='upload_zk_devices_bulk'),
    path('branches/<slug:slug>/extract-zk/', views.extract_zk_devices, name='extract_zk_devices_bulk'),
    path('zk/add/', views.add_zk_device, name='add_zk_device'),
    path('zk/template/download/', views.download_zk_template, name='download_zk_template'),
    
    # === Servers ===
    path('servers/', views.all_servers, name='all_servers'),
    path('servers/add/', views.add_server, name='add_server'),
    path('servers/<int:server_id>/', views.server_details, name='server_details'),
    path('servers/<int:server_id>/edit/', views.edit_server, name='edit_server'),
    path('servers/logs/', views.server_logs, name='server_logs'),
    path("servers/<int:server_id>/resources/", views.server_resources, name="server_resources"),

    # === On-Premises Virtual Machines ===
    path('vms/', views.all_vms, name='all_vms'),
    path('vms/add/', views.add_vm, name='add_vm'),
    path('vms/<int:vm_id>/', views.vm_details, name='vm_details'),
    path('vms/<int:vm_id>/edit/', views.edit_vm, name='edit_vm'),
    path('logs/vms/<int:vm_id>/', views.vm_logs, name='vm_logs'),

    # === Notification for low stock ===
    path('notifications/add/', views.NotificationConfigCreateView.as_view(), name='notification_config_create'),
    path('notifications/<int:pk>/edit/', views.NotificationConfigUpdateView.as_view(), name='notification_config_update'),
    path('notifications/<int:pk>/delete/', views.NotificationConfigDeleteView.as_view(), name='notification_config_delete'),
    path('notifications/recipients/add/', views.RecipientCreateView.as_view(), name='recipient_create'),
    path('notifications/recipients/<int:pk>/edit/', views.RecipientUpdateView.as_view(), name='recipient_update'),
    path('notifications/recipients/<int:pk>/delete/', views.RecipientDeleteView.as_view(), name='recipient_delete'),
    path('notifications/dashboard/', views.NotificationDashboardView.as_view(), name='notification_dashboard'),

    path('logout/', views.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)