from rest_framework import serializers
from .models import Trade, TradeHistory, Analysis, Insight,Premium

# class TradeHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TradeHistory
#         fields = ['buy', 'target', 'sl']


# class AnalysisSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Analysis
#         fields = ['bull_scenario', 'bear_scenario', 'status']


# class InsightSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Insight
#         fields = ['prediction', 'actual']


# class TradeSerializer(serializers.ModelSerializer):
#     history = TradeHistorySerializer(many=True)
#     analysis = AnalysisSerializer(many=True)  # Changed to many=True
#     insights = InsightSerializer(many=True)

#     class Meta:
#         model = Trade
#         fields = ['id','stock_index','company_name', 'segment', 'expiry_date', 'trade_type', 'history', 'analysis', 'insights']

#     def create(self, validated_data):
#         # Extract nested data
#         history_data = validated_data.pop('history')
#         analysis_data = validated_data.pop('analysis')
#         insights_data = validated_data.pop('insights')

#         # Create Trade instance
#         trade = Trade.objects.create(**validated_data)

#         # Create related TradeHistory instances
#         for history in history_data:
#             TradeHistory.objects.create(trade=trade, **history)

#         # Create related Analysis instances
#         for analysis in analysis_data:  # Correct handling of many-to-one relation
#             Analysis.objects.create(trade=trade, **analysis)

#         # Create related Insight instances
#         for insight in insights_data:
#             Insight.objects.create(trade=trade, **insight)

#         return trade

class TradeSerializer(serializers.ModelSerializer):
    buy = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)
    target = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)
    sl = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)
    
    bull_scenario = serializers.CharField(max_length=1000, write_only=True)
    bear_scenario = serializers.CharField(max_length=1000, write_only=True)
    status = serializers.ChoiceField(choices=Analysis.STATUS_CHOICES, write_only=True)

    prediction = serializers.CharField(max_length=255, write_only=True)
    actual = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = Trade
        fields = ['id', 'stock_index', 'company_name', 'segment', 'expiry_date', 'trade_type', 
                  'buy', 'target', 'sl', 
                  'bull_scenario', 'bear_scenario', 'status', 
                  'prediction', 'actual']

    def create(self, validated_data):
        # Extract flat data for nested models
        buy = validated_data.pop('buy')
        target = validated_data.pop('target')
        sl = validated_data.pop('sl')
        
        bull_scenario = validated_data.pop('bull_scenario')
        bear_scenario = validated_data.pop('bear_scenario')
        status = validated_data.pop('status')
        
        prediction = validated_data.pop('prediction')
        actual = validated_data.pop('actual')

        # Create the Trade instance
        trade = Trade.objects.create(**validated_data)

        # Create related TradeHistory instance
        TradeHistory.objects.create(trade=trade, buy=buy, target=target, sl=sl)

        # Create related Analysis instance
        Analysis.objects.create(trade=trade, bull_scenario=bull_scenario, bear_scenario=bear_scenario, status=status)

        # Create related Insight instance
        Insight.objects.create(trade=trade, prediction=prediction, actual=actual)

        return trade

#######admin listing tables ######

class InsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insight
        fields = ['prediction', 'actual']

class TradeListSerializer(serializers.ModelSerializer):
    buy = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()
    sl = serializers.SerializerMethodField()
    bull_scenario = serializers.SerializerMethodField()
    bear_scenario = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    prediction = serializers.SerializerMethodField()
    actual = serializers.SerializerMethodField()

    class Meta:
        model = Trade
        fields = ['id', 'stock_index','company_name','segment', 'expiry_date', 'trade_type', 
                  'buy', 'target', 'sl', 'bull_scenario', 'bear_scenario', 'status', 'prediction','actual']

    def get_buy(self, obj):
        trade_history = obj.history.first()  
        return trade_history.buy if trade_history else None

    def get_target(self, obj):
        trade_history = obj.history.first()
        return trade_history.target if trade_history else None

    def get_sl(self, obj):
        trade_history = obj.history.first()
        return trade_history.sl if trade_history else None

    def get_bull_scenario(self, obj):
        analysis = obj.analysis.first()
        return analysis.bull_scenario if analysis else None

    def get_bear_scenario(self, obj):
        analysis = obj.analysis.first()
        return analysis.bear_scenario if analysis else None

    def get_status(self, obj):
        analysis = obj.analysis.first()
        return analysis.status if analysis else None
    
    def get_prediction(self, obj):
        analysis = obj.insights.first()
        return analysis.prediction if analysis else None
    
    def get_actual(self, obj):
        analysis = obj.insights.first()
        return analysis.actual if analysis else None
    
    





class PremiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Premium
        fields = ['premium_amount', 'premium_period']
    

    def validate_premium_period(self, value):
        if Premium.objects.filter(premium_period=value).exists():
            raise serializers.ValidationError(f"The premium period '{value}' already exists.")
        return value



# update trade history 

class TradeUpdateSerializer(serializers.Serializer):
    buy = serializers.DecimalField(max_digits=10, decimal_places=2)
    target = serializers.DecimalField(max_digits=10, decimal_places=2)
    sl = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    def update_trade_history(self, trade):
        TradeHistory.objects.create(
            trade=trade,
            buy=self.validated_data['buy'],
            target=self.validated_data['target'],
            sl=self.validated_data['sl']
        )
        return trade


class TradeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeHistory
        fields = ['buy', 'target', 'sl', 'changed_at']

class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = ['bull_scenario', 'bear_scenario', 'status']


class TradeDetailsSerializer(serializers.ModelSerializer):
    history = TradeHistorySerializer(many=True, read_only=True)
    analysis = AnalysisSerializer(many=True, read_only=True)
    insights = InsightSerializer(many=True, read_only=True)
    
    class Meta:
        model = Trade
        fields = ['id', 'stock_index', 'company_name', 'segment', 'expiry_date', 'trade_type', 
                  'created_at', 'history', 'analysis', 'insights']
