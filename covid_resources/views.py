from django.shortcuts import render
from django.views import View
import os
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import csv

state_data = []
category_data = []
file_path_state = os.path.join(settings.BASE_DIR,'indian_states.json')
file_path_cat = os.path.join(settings.BASE_DIR,'category_state.json')
JSON_FILE_URL = os.path.join(settings.BASE_DIR,'leads.json')

leads=[]


def ssl(request):
	return render(request,'1C330E9E8A0E6A9BB9A2E33E150C0183.txt')

@login_required(login_url='/admin')
def excl(request):
	EXCEL_FILE_URL = os.path.join(settings.BASE_DIR,'leads.csv')
	JSON_FILE_URL = os.path.join(settings.BASE_DIR,'leads.json')
	with open(EXCEL_FILE_URL,'r') as f:
		reader = csv.reader(f)
		next(reader)
		data_csv = {"data": []}
		num=0
		for row in reader:
			num=num+1
			data_csv["data"].append({"Count": num ,"Date": row[0], "Supply": row[1], "State": row[2],"lead": {"City": row[3], "Vendor": row[4], "Contact": row[5],"Mode_of_contact": row[6],"Links": row[7],"Misc":row[8],"Status":row[9]}})
			
	with open(JSON_FILE_URL,'w') as f:
		json.dump(data_csv,f,indent=4)
		i = len(data_csv["data"])
		
		return JsonResponse(data_csv, safe=False)



class Homepage_View(View):

	
			
		
	
	def get(self, request):
		return render(request,'index.html')

				
	def get(self, request):
		
		with open(file_path_cat,'r')as cat_json_file:
			data_c = json.load(cat_json_file)
			
			with open(file_path_state,'r') as state_json_file:
				data_s = json.load(state_json_file)
			
				for key,value in data_c.items(): 
					category_data.append({'code':key,'category':value})

				
			for k,v in data_s.items():
				state_data.append({'name': k, 'value':v})
		
		return render(request,'index.html',{'indian_states': state_data,'category_state': category_data})

		
	def post(self, request):
		sno=0
		state = request.POST['state']
		category = request.POST['category']
		context = {
			'fieldvalues':request.POST
		}

		with open(JSON_FILE_URL,'r') as read_json_leads:
			sno=0
			leads=[]
			jSno=[]
			json_leads = json.load(read_json_leads)
			comp_leads = json_leads["data"]
			leads_len = len(json_leads["data"])
			leads.clear()
			for comp_int in range(leads_len):
				if comp_leads[comp_int]["State"] == state and comp_leads[comp_int]["Supply"] == category:
					leads_gen=comp_leads[comp_int]
					sno=sno+1
					leads.append(leads_gen)
									

		
		
		return render(request,'index.html',{'leads_result':leads,'indian_states': state_data,'category_state': category_data})
