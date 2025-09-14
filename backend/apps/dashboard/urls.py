from django.urls import path
from .views import DashboardView, DasboardPostListsView, DashboardCommentListsView, DashboardMarkNotiSeenAPIView, DashboardNotificationListsView, DashboardPostCreateAPIView, DashboardPostEditAPIView


urlpatterns = [
    # Vue principale du dashboard
    path('dashboard/<int:user_id>/', DashboardView.as_view(), name='dashboard-main'),

    # Liste des posts de l'utilisateur
    path('dashboard/<int:user_id>/posts/', DasboardPostListsView.as_view(), name='dashboard-post-list'),

    # Création d'un nouveau post (pas besoin d'user_id si on a un token)
    path('dashboard/posts/create/', DashboardPostCreateAPIView.as_view(), name='dashboard-post-create'),

    # Édition d'un post spécifique
    path('dashboard/posts/<int:post_id>/edit/', DashboardPostEditAPIView.as_view(), name='dashboard-post-edit'),

    # Commentaires (peut être global ou filtré)
    path('dashboard/comments/', DashboardCommentListsView.as_view(), name='dashboard-comment-list'),

    # Notifications
    path('dashboard/<int:user_id>/notifications/', DashboardNotificationListsView.as_view(), name='dashboard-notification-list'),
    path('dashboard/notifications/mark-seen/', DashboardMarkNotiSeenAPIView.as_view(), name='dashboard-notification-mark-seen'),
]
