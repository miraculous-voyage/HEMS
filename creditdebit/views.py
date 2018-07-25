from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import connection

from .models import Creditdebit
from .models import Dashboard
from .models import Inv_equ
from accounts.models import Extrainfo

@login_required(login_url="/accounts/signup")
def global_call(request):
    match = request.user.username
    info = Extrainfo.objects.get(user_name=match)
    return info

@login_required(login_url="/accounts/signup")
def home(request):
    try:
        inv = Inv_equ.objects.get(user_name=request.user.username)
        print(inv.amount)
        print(inv.amount)
    except:
        inv = Inv_equ()
        inv.user_name = request.user.username
        inv.save()
    dashs = Dashboard.objects
    return render(request, 'creditdebit/home.html', {'dashs': dashs, 'inv_amount':inv.amount, 'user_info':request.user, 'info':global_call(request)})

def tables(request):
    return render(request, 'creditdebit/tables.html', {'user_info':request.user, 'info':global_call(request)})

def reports(request):
    return render(request, 'creditdebit/reports.html', {'user_info':request.user, 'info':global_call(request)})

def datatable(request):
    items = Creditdebit.objects 
    return render(request, 'creditdebit/datatable.html', {'items': items, 'user_info':request.user, 'info':global_call(request)})

def usertable(request):
    items = Creditdebit.objects
    return render(request, 'creditdebit/usertable.html', {'items': items, 'user_info':request.user, 'info':global_call(request)})

def datatable_detail(request, item_id):
    item = get_object_or_404(Creditdebit, pk=item_id)
    if request.method == 'POST':
        if request.POST['description'] and request.POST['rupees']:

            if item.credit_or_debit == 'credit' and item.used_for == 'household' and item.money_source == 'own':
                val2 = int(item.id) + 1
                case_item = get_object_or_404(Creditdebit, pk=val2)
                dash = Dashboard.objects.get(source_id=case_item.id)                
                if(dash.flag_on_off == 0):                    
                    return render(request, 'creditdebit/datatable_detail.html',{'error':'You have already Redeemed.','item':item, 'user_info':request.user, 'info':global_call(request)})

            if item.credit_or_debit == 'credit' and item.used_for == 'personal' and item.money_source == 'khata':
                dash = Dashboard.objects.get(source_id=item.id)
                if(dash.flag_on_off == 0):                    
                    return render(request, 'creditdebit/datatable_detail.html',{'error':'You have already been paid.','item':item, 'user_info':request.user, 'info':global_call(request)})

            item.description = request.POST['description']
            item.rupees = request.POST['rupees']   
            item.last_edited_date = timezone.datetime.now()

            val = item.id - 2 
            
            try:
                cd = Creditdebit.objects.raw('SELECT * FROM creditdebit_creditdebit;')[val]
                                            
                if item.credit_or_debit == 'credit':                    
                    item.remaining_bal = cd.remaining_bal - int(request.POST['rupees'])
                else:                
                    item.remaining_bal = cd.remaining_bal + int(request.POST['rupees'])
            except:
                if item.credit_or_debit == 'credit':                    
                    item.remaining_bal = 0.00 - int(request.POST['rupees'])
                else:                
                    item.remaining_bal = 0.00 + int(request.POST['rupees'])

            item.save()

            if item.credit_or_debit == 'credit' and item.used_for == 'household' and item.money_source == 'own':
                case_item = get_object_or_404(Creditdebit, pk=item.id+1)               
                
                case_item.rupees = item.rupees  
                case_item.last_edited_date = timezone.datetime.now()
                case_item.remaining_bal = int(item.remaining_bal) + int(item.rupees)            
                case_item.save()

                dash = Dashboard.objects.get(source_id=case_item.id)
                dash.source_id = case_item.id   
                dash.price = item.rupees                
                dash.save()
            
            if item.credit_or_debit == 'credit' and item.used_for == 'personal' and item.money_source == 'khata':
                dash = Dashboard.objects.get(source_id=item.id)
                dash.source_id = item.id   
                dash.price = item.rupees
                dash.save()
            
        else:
             return render(request, 'creditdebit/datatable_detail.html',{'error':'All fields are required.','item':item, 'user_info':request.user, 'info':global_call(request)})
               
    return render(request, 'creditdebit/datatable_detail.html', {'item':item, 'user_info':request.user, 'info':global_call(request)})

def give_take(request, dash_id):    
    if request.method == 'POST':
        dash = get_object_or_404(Dashboard, pk=dash_id)
        print(dash.id)
        ref_item = get_object_or_404(Creditdebit, pk=dash.source_id)
        cd = Creditdebit.objects.raw('SELECT * FROM creditdebit_creditdebit;')[-1]
        item = Creditdebit()
        item.rupees = ref_item.rupees 
        item.used_for = ref_item.used_for
        item.money_source = ref_item.money_source
        item.pub_datetime = timezone.datetime.now()      
        item.hunter = ref_item.hunter
        item.last_edited_date = timezone.datetime.now()
        if(dash.give_take == 0):
            #redeem
            item.description = 'Redeemed By: ' + str(ref_item.hunter) + ' ID-' + str(ref_item.id)      
            item.credit_or_debit = 'credit'
            item.remaining_bal = cd.remaining_bal - ref_item.rupees        
        else:
            #pay
            item.description = 'Paid By: ' + str(ref_item.hunter) + ' ID-' + str(ref_item.id)      
            item.credit_or_debit = 'debit'
            item.remaining_bal = cd.remaining_bal + ref_item.rupees
        
        item.save()

        dash.flag_on_off = False
        dash.save()
        #return render(request, 'creditdebit/home.html', {'dashs': dashs, 'user_info':request.user, 'info':global_call(request)})
        return redirect('/creditdebit/')

@login_required(login_url="/accounts/signup")
def add_to_datatable(request):
    if request.method == 'POST':
        if request.POST['description'] and request.POST['rupees'] and request.POST['credit_or_debit'] and request.POST['used_for'] and request.POST['money_source'] and request.POST['pub_datetime']:
            item = Creditdebit()
            item.description = request.POST['description']
            item.rupees = request.POST['rupees']            
            item.credit_or_debit = request.POST['credit_or_debit']
            item.used_for = request.POST['used_for']
            item.money_source = request.POST['money_source']
            item.pub_datetime = request.POST['pub_datetime']            
            item.hunter = request.user 

            if request.POST['credit_or_debit'] == 'debit' and request.POST['used_for'] == 'household' and request.POST['money_source'] == 'khata':
                return render(request, 'creditdebit/add_to_datatable.html',{'error':'The selected Fields are not Valid'})

            elif request.POST['credit_or_debit'] == 'debit' and request.POST['used_for'] == 'personal' and request.POST['money_source'] == 'khata':
                return render(request, 'creditdebit/add_to_datatable.html',{'error':'The selected Fields are not Valid'})

            elif request.POST['credit_or_debit'] == 'debit' and request.POST['used_for'] == 'personal' and request.POST['money_source'] == 'own':
                return render(request, 'creditdebit/add_to_datatable.html',{'error':'The selected Fields are not Valid'})

            elif request.POST['credit_or_debit'] == 'credit' and request.POST['used_for'] == 'personal' and request.POST['money_source'] == 'own':
                return render(request, 'creditdebit/add_to_datatable.html',{'error':'The selected Fields are not Valid'})

            else:
                try:
                    cd = Creditdebit.objects.raw('SELECT * FROM creditdebit_creditdebit;')[-1]                                
                    if request.POST['credit_or_debit'] == 'credit':                    
                        item.remaining_bal = cd.remaining_bal - int(request.POST['rupees'])
                    else:                
                        item.remaining_bal = cd.remaining_bal + int(request.POST['rupees'])
                except:
                    if request.POST['credit_or_debit'] == 'credit':                    
                        item.remaining_bal = 0.00 - int(request.POST['rupees'])
                    else:                
                        item.remaining_bal = 0.00 + int(request.POST['rupees'])
            

            item.last_edited_date = timezone.datetime.now()            
            item.save()

            if item.credit_or_debit == 'debit':
                user_invest = Inv_equ.objects.get(user_name=request.user.username)
                investment_index = user_invest.amount + int(item.rupees)

                if investment_index > 0.00:
                    all_users_investments = Inv_equ.objects.all()
                    for investment in all_users_investments:
                        if investment.user_name is not user_invest.user_name:
                            temp = investment.amount
                            investment.amount = temp - investment_index
                            print(investment.amount)
                            investment.save()
                    user_invest.amount = 0.00
                elif investment_index < 0.00:
                    user_invest.amount = investment_index
                else:
                    user_invest.amount = 0.00
                user_invest.save()

            if request.POST['credit_or_debit'] == 'credit' and request.POST['used_for'] == 'household' and request.POST['money_source'] == 'own':
                case_item = Creditdebit()
                case_item.hunter = item.hunter
                case_item.description = 'Invested By: ' + str(case_item.hunter) + ' ID-' + str(item.id)
                case_item.rupees = item.rupees           
                case_item.credit_or_debit = 'debit'
                case_item.used_for = item.used_for
                case_item.money_source = item.money_source
                case_item.pub_datetime =  item.pub_datetime
                case_item.last_edited_date = timezone.datetime.now()
                case_item.remaining_bal = int(item.remaining_bal) + int(item.rupees)            
                case_item.save()

                dash = Dashboard()
                dash.source_id = case_item.id
                dash.username = request.user
                dash.descript = item.description
                dash.price = item.rupees
                dash.flag_on_off = 1
                dash.give_take = 0 # here 0 indicates take money from khata --- REDEEM
                dash.save()



            if request.POST['credit_or_debit'] == 'credit' and request.POST['used_for'] == 'personal' and request.POST['money_source'] == 'khata':
                dash = Dashboard()
                dash.source_id = item.id
                dash.username = request.user
                dash.descript = item.description
                dash.price = item.rupees
                dash.flag_on_off = 1
                dash.give_take = 1 # here 1 indicates give money to khata ---PAY
                dash.save()


            return redirect('/creditdebit/tables/datatable/' + str(item.id))
        else:
            return render(request, 'creditdebit/add_to_datatable.html',{'error':'All fields are required.'})
    else:
        return render(request, 'creditdebit/add_to_datatable.html')


