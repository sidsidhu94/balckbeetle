# urls.py
from django.urls import path,include
from .views import TradeCreateView,TradeDetailView,PremiumCreate,PremiumEdit,UserListView,UserCountView,TradeStatsView,TradeUpdateView

urlpatterns = [
    ######trades######
    path('create-trade/', TradeCreateView.as_view(), name='create-trade'),
    path('update-trade/<int:trade_id>/', TradeUpdateView.as_view()),

    path('trades/', TradeDetailView.as_view(), name='trade-list'),
    path('trade-counts/', TradeStatsView.as_view(), name='trade-counts'),
    

    ######premium######
    path('premium/', PremiumCreate.as_view(), name='premium-create'),
    path('edit-premium/<int:pk>/', PremiumEdit.as_view(), name='premium-edit'),

    ######users######
    path('users/', UserListView.as_view(), name='user-list'),
    path('user-counts/', UserCountView.as_view(), name='user-counts'),

    
]
