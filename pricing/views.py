from django.shortcuts import render, redirect
from .forms import PricingConfigurationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import PricingConfiguration

def pricing_configuration_list(request):
    configurations = PricingConfiguration.objects.all()
    return render(request, 'configuration_list.html', {'configurations': configurations})

def add_pricing_configuration(request):
    if request.method == 'POST':
        form = PricingConfigurationForm(request.POST)
        if form.is_valid():
            configuration = form.save(commit=False)
            configuration.created_by = request.user
            configuration.save()
            return redirect('pricing:configuration_list')
    else:
        form = PricingConfigurationForm()
    return render(request, 'configuration_form.html', {'form': form})

@csrf_exempt
def calculate_price(request):
    print(request.body)
    if request.method == 'POST':
        data = json.loads(request.body)
        distance = data.get('distance', 0)
        time = data.get('time', 0)
        waiting_time = data.get('waiting_time', 0)
        
        # Retrieve active pricing configuration (you can add more logic to handle multiple configurations)
        active_config = PricingConfiguration.objects.filter(active=True).first()
        if not active_config:
            return JsonResponse({'error': 'No active pricing configuration found.'}, status=400)
        
        # Calculate the price based on the formula

        #Distance Base Price
        DBA = active_config.distance_base_price if distance <= active_config.distance_base_price_upto else active_config.distance_base_price_after_upto
        #Distance Additional Price
        DAP = 0
        if distance <= active_config.distance_additional_price_upto:
            DAP = distance * active_config.distance_additional_price
        else:
            DAP = (distance - active_config.distance_additional_price_upto) * active_config.distance_additional_price_after_upto
        #Price from Time factor
        TFP = 0
        if time <= active_config.time_multiplier_factor_upto:
            TFP = time * active_config.time_multiplier_factor
        else:
            TFP = (time - active_config.time_multiplier_factor_upto) * active_config.time_multiplier_factor_after_upto
        #Waiting Charges
        WC = 0
        if waiting_time <= active_config.waiting_charges_upto:
            WC = waiting_time * active_config.waiting_charges
        else:
            WC = (waiting_time - active_config.waiting_charges_upto) * active_config.waiting_charges_after_upto

        price = DBA + DAP +  + TFP + WC
        
        return JsonResponse({"Distance Base Price": DBA,
                             "Distance Additional Price": DAP,
                             "Time Factor Price": TFP,
                             "Waiting Charges": WC,
                             'Accumulated Price': price})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

