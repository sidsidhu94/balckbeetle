from django.contrib import admin
from .models import Trade, TradeHistory, Analysis, Insight,Premium

class TradeHistoryInline(admin.TabularInline):
    model = TradeHistory
    extra = 1  

class AnalysisInline(admin.TabularInline):
    model = Analysis
    extra = 1  

class InsightInline(admin.TabularInline):
    model = Insight
    extra = 1  

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('stock_index','company_name', 'segment', 'expiry_date', 'trade_type','created_at')
    inlines = [TradeHistoryInline, AnalysisInline, InsightInline]  

@admin.register(TradeHistory)
class TradeHistoryAdmin(admin.ModelAdmin):
    list_display = ('trade', 'buy', 'target', 'sl', 'changed_at')
    ordering = ('-changed_at',)

@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('trade', 'bull_scenario', 'bear_scenario', 'status')

@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ('trade', 'prediction', 'actual')


@admin.register(Premium)
class PremiumAdmin(admin.ModelAdmin):
    # Optionally customize what is displayed in the list view
    list_display = ('premium_amount', 'premium_period')
    search_fields = ('premium_period',)
    list_filter = ('premium_period',)