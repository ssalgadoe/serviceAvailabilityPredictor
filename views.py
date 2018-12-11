from django.shortcuts import render, get_object_or_404
from .models import locations
from .forms import locationsForm
import random


# Create your views here.

cust_types = ['active','site_survey_waiting','install_waiting','unable_to_serve','response_waiting', 'distributor', 'non-wireless_customer', 'other']

def home(request):
    return render(request, 'locations/home.html',)


def index(request, select_id=''):
    select_id = request.GET.get('cust_type')
    if select_id =='':
        select_id = 100
    print('select_id', select_id)
    #news_list = sorted(active_news_items.objects.all().values().order_by('?'), key=lambda x:random.random())
    customer_list = locations.objects.all().values()
    customers_a = []
    customers_s = []
    customers_i = []
    customers_u = []
    customers_r = []
    customers_d = []
    customers_n = []    
    customers_o = []
    default_geo = {}
    default_geo['lat'] = float(43.912126)
    default_geo['lng'] = float(-79.524203)    
    center_point = []
    cust = {}
    cust['lat'] = float(customer_list[0]['lat'])
    cust['lng'] = float(customer_list[0]['lng'])
   # center_point.append(cust)
    
    for ele in customer_list:
        row = {}
        g_data = {}
        c_label = ele['name']

        row['id'] = ele['id']                   
        row['name'] = ele['name']
        try:
            row['lat'] = float(ele['lat'])
            row['lng'] = float(ele['lng'])
        except:
            row['lat'] = float(default_geo['lat'])
            row['lng'] = float(default_geo['lng'])
            
        row['c_type'] = ele['cust_type']
        
        address = ele['address1'] + ', ' + ele['city'] + ', ' + ele['postalcode']
        row['address'] = address
       
        if ele['cust_type'] == 'active':
            customers_a.append(row)
        elif ele['cust_type'] == 'site_survey_waiting':
            customers_s.append(row)
        elif ele['cust_type'] == 'install_waiting':
            customers_i.append(row)
        elif ele['cust_type'] == 'unable_to_serve':
            customers_u.append(row)
        elif ele['cust_type'] == 'response_waiting':
            customers_r.append(row)
        elif ele['cust_type'] == 'distributor':
            customers_d.append(row)
        elif ele['cust_type'] == 'non-wireless_customer':
            customers_n.append(row)
        elif ele['cust_type'] == 'other':
            customers_o.append(row)

    
    cust_size = 5
    active_list = [{'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}]
       
    if select_id == '0':
        active_list = [{'a':0}]
        if len(customers_a) > 0:
            cust['lat'] = float(customers_a[0]['lat'])
            cust['lng'] = float(customers_a[0]['lng'])
    elif select_id == '1':
        active_list = [{'a':1}]
        if len(customers_s) > 0:
            cust['lat'] = float(customers_s[0]['lat'])
            cust['lng'] = float(customers_s[0]['lng'])        
    elif select_id == '2':
        active_list = [{'a':2}]
        if len(customers_i) > 0:
            cust['lat'] = float(customers_i[0]['lat'])
            cust['lng'] = float(customers_i[0]['lng'])        
    elif select_id == '3':
        active_list = [{'a':3}]
        if len(customers_u) > 0:
            cust['lat'] = float(customers_u[0]['lat'])
            cust['lng'] = float(customers_u[0]['lng'])     
    elif select_id == '4':
        active_list = [{'a':4}]
        if len(customers_r) > 0:
            cust['lat'] = float(customers_r[0]['lat'])
            cust['lng'] = float(customers_r[0]['lng'])        
    elif select_id == '5':
        active_list = [{'a':5}]
        if len(customers_d) > 0:        
            cust['lat'] = float(customers_d[0]['lat'])
            cust['lng'] = float(customers_d[0]['lng'])
    elif select_id == '6':
        active_list = [{'a':6}]
        if len(customers_n) > 0:
            cust['lat'] = float(customers_n[0]['lat'])
            cust['lng'] = float(customers_n[0]['lng'])        
    elif select_id == '7':
        active_list = [{'a':7}]
        if len(customers_o) > 0:
            cust['lat'] = float(customers_o[0]['lat'])
            cust['lng'] = float(customers_o[0]['lng'])        
    else:
        active_list = [{'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}] 
        select_id = 100
    #print('label list',label_list)
    center_point.append(cust)
    temp_list = [[i, cust_types[i]] for i in range(len(cust_types))]
    context = {
        'customer_list_active': customers_a[:cust_size],
        'customer_list_sitesurvey': customers_s[:cust_size],
        'customer_list_install': customers_i[:cust_size],
        'customer_list_unable': customers_u[:cust_size],
        'customer_list_response': customers_r[:cust_size],
        'customer_list_distributor': customers_d[:cust_size],
        'customer_list_non_wireless': customers_n[:cust_size],
        'customer_list_other': customers_o[:cust_size],
        'cust_types': cust_types,
        'center_point':center_point,
        'active_list': active_list,
        'select_id': int(select_id),
        'temp_list': temp_list

    }
    return render(request, 'locations/index.html',context)



  

def customer(request,cust_id, select_id=100):
    subject = request.POST.get('subject')

    if request.method=='POST':
        if subject == "Update":
            print("need to save")
            cust_id = request.POST.get('cust_id')
            print(cust_id)
            customer_form = locationsForm(request.POST)
            if customer_form.is_valid():
                print("got a valid form")
                cust = locations.objects.get(id=cust_id)
                print(cust.name)
                try:
                    cust1 = locations()
                    cust1.name = customer_form.cleaned_data['name']
                    cust1.address1 = customer_form.cleaned_data['address1']
                    cust1.address2 = customer_form.cleaned_data['address2']
                    cust1.city = customer_form.cleaned_data['city']
                    cust1.province = customer_form.cleaned_data['province']
                    cust1.postalcode = customer_form.cleaned_data['postalcode']
                    cust1.country = customer_form.cleaned_data['country']
                    cust1.cust_type = customer_form.cleaned_data['cust_type']
                    cust1.comments = customer_form.cleaned_data['comments']
                    cust1.winbox = customer_form.cleaned_data['winbox']
                    cust1.lat = customer_form.cleaned_data['lat']
                    cust1.lng = customer_form.cleaned_data['lng']
                    cust1.sitesurvey_ok = customer_form.cleaned_data['sitesurvey_ok']
                    cust1.rssi = customer_form.cleaned_data['rssi']
                    cust1.ccq_tx = customer_form.cleaned_data['ccq_tx']
                    cust1.ccq_rx = customer_form.cleaned_data['ccq_rx']
                    cust1.snr = customer_form.cleaned_data['snr']
                    cust1.ap_id = customer_form.cleaned_data['ap_id']
                    cust1.id = cust_id
                    cust1.save()
                except Exception as e:
                    print("something went wrong--->", e)
            else:
                print("somethng wrong with the form")
        else:
            print("cancel the update")




        
    cust_list = locations.objects.values().distinct().filter(id=cust_id).values()
    center_point = {}
    center_point['lat'] = float(cust_list[0]['lat'])
    center_point['lng'] = float(cust_list[0]['lng'])
    
    
    cust_types = ['active','site_survey_waiting','install_waiting','unable_to_serve','response_waiting', 'distributor', 'non-wireless_customer', 'other']
    customer = {}
    customer['id'] = cust_list[0]['id']
    customer['name'] = cust_list[0]['name']
    customer['address1'] = cust_list[0]['address1'] if cust_list[0]['address1'] else "n/a"
    customer['address2'] = cust_list[0]['address2'] if cust_list[0]['address2'] else "n/a"
    customer['city'] = cust_list[0]['city'] if cust_list[0]['city'] else "n/a"
    customer['province'] = cust_list[0]['province'] if cust_list[0]['province'] else "n/a"
    customer['postalcode'] = cust_list[0]['postalcode'] if cust_list[0]['postalcode']   else "n/a"
    customer['country'] = cust_list[0]['country'] if cust_list[0]['country']   else "n/a"
    customer['cust_type'] = cust_list[0]['cust_type'] if cust_list[0]['cust_type']   else 0
    customer['winbox'] = cust_list[0]['winbox'] if cust_list[0]['winbox']   else "n/a"
    customer['lng'] = float(cust_list[0]['lng']) if cust_list[0]['lng']   else -79.524203
    customer['lat'] = float(cust_list[0]['lat']) if cust_list[0]['lat']   else 43.912126
    customer['comments'] = cust_list[0]['comments'] if cust_list[0]['comments']   else "n/a"
    customer['sitesurvey_ok'] = cust_list[0]['sitesurvey_ok'] if cust_list[0]['sitesurvey_ok']   else 0
    customer['ap_id'] = cust_list[0]['ap_id'] if cust_list[0]['ap_id']   else "n/a"
    customer['ccq_rx'] = cust_list[0]['ccq_rx'] if cust_list[0]['ccq_rx']   else 0
    customer['ccq_tx'] = cust_list[0]['ccq_tx'] if cust_list[0]['ccq_tx']   else 0
    customer['rssi'] = cust_list[0]['rssi'] if cust_list[0]['rssi']   else 0
    customer['snr'] = cust_list[0]['snr'] if cust_list[0]['snr']   else 0
    customer['neighbours'] = cust_list[0]['neighbours'] if cust_list[0]['neighbours']   else 0
    
    neighbours = cust_list[0]['neighbours'].split(',')
    print(neighbours)
    neighbour_list = []
    for ele in neighbours:
        neighbour_data = {}
        neighbour = locations.objects.values().distinct().filter(id=ele).values()
        
        neighbour_data['id'] = neighbour[0]['id']
        neighbour_data['name'] = neighbour[0]['name']
        neighbour_data['address1'] = neighbour[0]['address1'] if neighbour[0]['address1'] else "n/a"
        neighbour_data['lng'] = float(neighbour[0]['lng']) if neighbour[0]['lng']   else -79.524203
        neighbour_data['lat'] = float(neighbour[0]['lat']) if neighbour[0]['lat']   else 43.912126        
        neighbour_data['ap_id'] = neighbour[0]['ap_id'] if neighbour[0]['ap_id']   else "n/a"
        neighbour_data['ccq_rx'] = neighbour[0]['ccq_rx'] if neighbour[0]['ccq_rx']   else 0
        neighbour_data['ccq_tx'] = neighbour[0]['ccq_tx'] if neighbour[0]['ccq_tx']   else 0
        neighbour_data['rssi'] = neighbour[0]['rssi'] if neighbour[0]['rssi']   else 0
        neighbour_data['snr'] = neighbour[0]['snr'] if neighbour[0]['snr']   else 0    
   
        neighbour_list.append(neighbour_data)
   
    
    context = {
            'customer': customer, 
            'customer1': cust_list[0], 
            'cust_types': cust_types,
            'select_id': select_id,
            'neighbour_list': neighbour_list[1:6],
            'center_point': center_point
    }        
    return render(request, 'locations/customer.html', context)




