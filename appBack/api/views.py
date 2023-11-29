from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from . import models
from rest_framework import serializers
import random, json
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from fpdf import FPDF
from datetime import datetime, timedelta

font_path = "D:\\Github\\foodcom\\foodcom_backend\\telegram-bot\\myfile.ttf"
directory_path = "D:\\Github\\foodcom\\foodcom_backend\\telegram-bot\\docs"

event_types = (
    ('wedding', '가족 개인행사'),
    ('business', '기업 이벤트'),
    ('public', '사회 단체행사'),
    ('festival', '기관, 축제등'),
    ('birthday', '스몰웨딩, 야외결혼'),
    ('steak', '스테이크 행사'),
    ('fingerFood', '핑거푸드')
)

event_places = (
    ('실내', '실내'),
    ('야외', '야외'),
    ('체육관', '체육관'),
    ('연회장', '연회장'),
    ('호텔', '호텔'),
    ('미정', '미정')
)


@api_view(['GET'])
def api(request):
    return Response({"message": "Welcome to the API"})


class LatestCustomerSerializer(models.CustomerSerializer):
    class Meta:
        model = models.Customer
        fields = ('ticket_number', 'name', 'address')

class CustomerViewAPIView(generics.RetrieveAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = models.CustomerSerializer
    lookup_field = 'ticket_number'

class LatestCustomers(generics.ListAPIView):
    queryset = models.Customer.objects.all().order_by('-id')[:10]
    serializer_class = LatestCustomerSerializer

class PDF(FPDF):
    def header(self):
        self.add_font('nanumgothic', '', font_path, uni=True)
        self.set_font('nanumgothic', '', 15)
        page_width = self.w
        header_cell_width = 50
        x = (page_width - header_cell_width) / 2
        self.set_xy(x, 10)
        self.cell(header_cell_width, 10, '푸드컴 확인서', 1, 0, 'C')
        self.ln(10)

@api_view(['GET'])
def generatePDF(request, ticket_number):
    data = models.Customer.objects.get(ticket_number=ticket_number)
    
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('nanumgothic', '', 20)

    line_spacing = 5

    pdf.set_draw_color(0, 0, 0)
    pdf.rect(10, 10, pdf.w - 20, pdf.h - 20) 

    border_height = pdf.h - 100
    border_width = pdf.w - 40
    total_data_height = 12 * 12  

    y = (border_height - total_data_height) / 2 + 10

    pdf.set_xy(20, y)

    tool_data = ", ".join(k.name for k in data.tool.all())

    event = ""
    for event_type in event_types:
        if event_type[0] == data.event_type:
            event = event_type[1]
            break

    if data.event_place == None:
        data.event_place = ""

    if data.event_type == None:
        data.event_type = ""

    pdf.multi_cell(border_width, 10,
                                      f"고객 이름: {data.name}\n\n"
                                      f"고객 전화 번호: {data.phone_number}\n\n"
                                      f"이벤트 유형: {event} {data.custom_event_type}\n\n"
                                      f"사람 수: {data.people_count}명\n\n"
                                      f"식사비: {data.meal_cost}원\n\n"
                                      f"행사 장소: {data.event_place} {data.custom_event_place}\n\n"
                                      f"주소: {data.address}\n\n"
                                      f"추가: {tool_data}, {data.custom_tool}\n\n"
                                      f"개최 날짜: {data.event_date}\n\n"                                      
                                      f"고객 등록 날짜: {data.date_registered}\n\n"
                                      f"티켓 번호: {data.ticket_number}",
                   align='C')


    pdf_file = f"{directory_path}/{data.name}.pdf"
    pdf.output(pdf_file, 'F')
    return Response({"message" : f"{data.name}.pdf is created in the documents folder"})

@api_view(['GET'])
def new_customer(request):
    all_customers = models.Customer.objects.values()
    all_tickets = []

    for k in all_customers:
        all_tickets.append(k['ticket_number'])

    while True:
        ticket_number = random.randint(1, 100000000)
        if ticket_number not in all_tickets:
            models.Customer.objects.create(name=request.GET.get('name'), address=request.GET.get('address'), \
                                        phone_number=request.GET.get('phone_number'), ticket_number=ticket_number)
        break
    return Response({'ticket_number' : ticket_number})


@csrf_exempt
def process_data(request, ticket_number):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event_type = data['event_type']
            event_type_choices = [choice[0] for choice in models.event_types]
            event_place = data['event_place']
            event_place_choices = [choice[0] for choice in models.event_places]
            message = ""

            tool = data['tool']
            custom_tool = None  # Initialize the custom_tool variable
            numeric_tool = []

            for value in tool:
                if value.isnumeric():
                    numeric_tool.append(int(value))
                elif isinstance(value, str):
                    custom_tool = value
                    message += "Custom tool : " + custom_tool + "\n"

            people_count = data['people_count']

            #convert people_count to integer
            if isinstance(people_count, str):
                people_count = int(people_count)
        
            customer = models.Customer.objects.get(ticket_number=ticket_number)
            customer.name = data['name']
            customer.address = data['address']
            customer.phone_number = data['phone_number']
            customer.message = data['message']
            if event_type in event_type_choices:
                message += "Custom event type\n"
                customer.event_type = data['event_type']
            else:
                customer.custom_event_type = data['event_type']

            if event_place in event_place_choices:
                message += "Custom event place\n"
                customer.event_place = data['event_place']
            else:
                customer.custom_event_place = data['event_place']
            customer.people_count = people_count
            event_date = data['event_date']
            event_time = data['event_time']
            customer.event_date = (datetime.strptime(event_date, "%Y-%m-%dT%H:%M:%S.%fZ").replace(hour=0, minute=0) + timedelta(hours=int(event_time.split(":")[0]), minutes=int(event_time.split(":")[1]))).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            customer.meal_cost = data['meal_cost']
            customer.date_registered = datetime.now()
            customer.tool.set(numeric_tool)
            customer.custom_tool = custom_tool
            customer.ticket_number = ticket_number

            try:
                customer.save()
                print("Customer saved")
            except Exception as e:
                message += str(e) + "\n"
                print("Customer could not be created")

            response_data = {
                'message' : message
            }
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error' : str(e)})

# class MenuDetail(APIView):
#     def get_object(self, ticket_number):
#         try:
#             customer = models.Customer.objects.get(ticket_number=ticket_number)
#             return models.Menu.objects.get(customer=customer)
#         except models.Menu.DoesNotExist:
#             raise Http404
        
#     def get(self, request, ticket_number, format=None):
#         menu = self.get_object(ticket_number)
#         serializer = models.MenuSerializer(menu)
#         mydata = serializer.data

#         custom_menu_index = mydata['custom_menu']
#         custom_menu = []
#         for k in custom_menu_index:
#             food_object = models.Food.objects.get(id=k)
#             serialized_food_object = models.FoodSerializer(food_object)
#             custom_menu.append(serialized_food_object.data)
        
#         mydata['custom_menu'] = custom_menu

#         food_set_index = mydata['food_set']
#         food_set_object = models.Set.objects.get(id=food_set_index)
#         serialized_food_set = models.SetSerializer(food_set_object)
#         mydata['food_set'] = serialized_food_set.data

#         return Response(mydata)
#     def put(self, request, ticket_number, format=None):
#         customer = models.Customer.objects.get(ticket_number=ticket_number)
#         menu = models.Menu.objects.get(customer=customer)
#         serializer = models.MenuSerializer(menu, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         print(serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # pdf.multi_cell(border_width, 10,
    #                                   f"고객 이름: {data.name}\n\n"
    #                                   f"고객 전화 번호: {data.phone_number}\n\n"
    #                                   f"이벤트 유형: {event_types[int(data.event_type)-1][1]}\n\n"
    #                                   f"행사 장소: {event_places[int(data.event_place)-1][1]}\n\n"
    #                                   f"개최 날짜: {data.event_date}\n\n"
    #                                   f"주소: {data.address}\n\n"
    #                                   f"고객 등록 날짜: {data.date_registered}\n\n"
    #                                   f"티켓 번호: {data.ticket_number}\n\n"
    #                                   f"추가: {tool_data}",
    #                align='C')