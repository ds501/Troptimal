import urllib.request as ul
import json
import datetime
from django.shortcuts import render,HttpResponse,get_object_or_404
from troptimal_app.models import trop_request
from troptimal_app.models import attraction
from troptimal_app.models import attraction_pair
from troptimal_app.models import output
from bs4 import BeautifulSoup
import pulp


"""
Functions triggered by urls are at the bottom.  Preliminary functions above.
"""

# Reccover list of selected attractions
def get_attraction_list(utr):
    al_str = utr.attract_list_nums
    a_l_num_str = al_str.split(',')
    a_l = []
    for num_str in a_l_num_str:
        attract = get_object_or_404(attraction,pk=int(num_str))
        a_l.append(attract)
    return a_l

"""
These functions are for dealing with the selected attractions list
"""

# Writes new attraction pair entries from list of attractions and trop_request
def enter_attraction_pairs(a_l, utr):
    attraction_num = len(a_l)
    str_attract = ''
    for i in range(attraction_num):
        a1_num = a_l[i].attraction_number
        str_attract = str_attract + str(a1_num)
        if i == attraction_num -1:
            pass
        else:
            str_attract = str_attract + ','
        utr.attract_list_nums = str_attract
        utr.save()
        for j in range(attraction_num):
            a2_num = a_l[j].attraction_number
            new_pair = attraction_pair(user_trop_request=utr, attraction=a_l[i])
            new_pair.attraction_second_num = a2_num
            new_pair.save()

"""
These functions are used to pull attractions data from TripAdvisor and manage the data
"""

def get_address(soup):
    attractions_address = soup.find('div', class_="info_wrapper")
    address_rough = attractions_address.get_text()
    address_rough.find('Address: ')
    begin = address_rough.find('Address: ')+9
    end = address_rough[begin:].find('\n')+1
    address = ''
    for char in address_rough[begin:end]:
        address+=char
    return address

# Define a function to obtain descriptions from attraction page soup:
def get_description(soup):
    description_rough = soup.find('div', class_="listing_details")
    if description_rough == None:
        return None
    else:
        description_rough2 = description_rough.get_text()
        begin = description_rough2.find('\n')+1
        end = description_rough2[begin:].find('\n')+1
        description = ''
        for char in description_rough2[begin:end]:
            description+=char
        return description

# Define a function to obtain times open from attraction page soup:
def get_times(soup):
    attractions_times = soup.find('div', class_="time")
    if attractions_times == None:
        return None
    else:
        times = attractions_times.get_text()
        return times

# Define a function to gets attraction links from soup:
def get_city_attractions_links(soup):
    for link in soup.find_all('a'):
        h_link=link.get('href')
        if h_link and '/Attractions-g' in h_link:
            city_attractions_link = "http://www.tripadvisor.com"+h_link
            return city_attractions_link
    else:
        return None

# Uses above functions to scrape city attractions
def tripad_scrape(search_terms):
    #Convert the search terms into the url for the searched city:
    location_string = ''
    for i in search_terms:
        if i == " ":
            new_i = "%20"
        else:
            new_i = i
        location_string += new_i

    #Pull up the searched city's page and parse using Beautiful Soup:
    url = "http://www.tripadvisor.com/Search?q="+location_string

    empty1 = True
    empty2 = True
    n = 0
    m = 0

    while empty1 and n<5:
        try:
            url_response=ul.urlopen(url,timeout=5)
            soup = BeautifulSoup(url_response, 'lxml')
            for link in soup.find_all('a'):
                h_link=link.get('href')
                if h_link and '/Attractions-g' in h_link:
                    attractions_link = h_link
                    break
            city_attractions_link = "http://www.tripadvisor.com"+attractions_link
            cal_url_response=ul.urlopen(city_attractions_link,timeout=5)
            city_attractions_soup = BeautifulSoup(cal_url_response, 'lxml')
            ds_city_attractions_link = get_city_attractions_links(city_attractions_soup)
            if ds_city_attractions_link != None:
                empty1=False
        except:
            n+=1


    while empty2 and m<5:
        try:
        #Pull up the city attractions page and parse using Beautiful Soup:
            url_response=ul.urlopen(ds_city_attractions_link,timeout=5)
            attractions_soup = BeautifulSoup(url_response, 'lxml')
            attractions_list = attractions_soup.find_all('div', class_="property_title")
            if len(attractions_list)>0:
                empty2=False
        #Identify the set of attractions on the attractions page:
        except:
            m+=1

    if empty1==False and empty2==False:
        attractions_rough = list()
        for thing in range(0,len(attractions_list)):
            data = attractions_list[thing]
            attractions_rough.append(data.get_text())

    #Print list of attractions (attractions_print):
        attractions_print = list()
        for thing in range(0,len(attractions_rough)):
            begin = attractions_rough[thing].find('\n')+1
            end = attractions_rough[thing][begin:].find('\n')+1
            data = attractions_rough[thing][begin:end]
            if '(' in data:
                pass
            else:
                attractions_print.append(data)

    #Pull up list of links for each attraction (attraction_links_list):
        attraction_links_rough = attractions_soup.find_all('div', class_="property_title")

        attraction_links_list = []
        for thing in range(0,len(attraction_links_rough)):
            attr_links_string = str(attraction_links_rough[thing])
            begin = attr_links_string.find('<a href="')+9
            end = attr_links_string.find('" onclick=')
            data = "http://www.tripadvisor.com" + attr_links_string[begin:end]
            if '<a data-params=' in data:
                pass
            else:
                attraction_links_list.append(data)

    #obtain each address, description, hours:
        addr_list = []
        description_list = []
        times_list = []
        for link in attraction_links_list:
            try:
                als_url_response=ul.urlopen(link,timeout=5)
                attraction_links_soup = BeautifulSoup(als_url_response, 'lxml')
                addr = get_address(attraction_links_soup)
                addr_list.append(addr)
            except:
                addr_list.append(search_terms)
            try:
                descr = get_description(attraction_links_soup)
                description_list.append(descr)
            except:
                description_list.append(None)
            try:
                times = get_times(attraction_links_soup)
                times_list.append(times)
            except:
                times_list.append(None)
        return attractions_print, description_list, times_list, addr_list
    else:
        return [], [], [], []

def go_get_city_attractions(city, state, country):
    if state!='NA':
        a_name_l, descrip_l, sch_1, add_l = tripad_scrape(city+' '+state)
    else:
        a_name_l, descrip_l, sch_1, add_l = tripad_scrape(city+' '+country)
    all_attractions= attraction.objects.all()
    big = 0
    for item in all_attractions:
        big=max(item.attraction_number, big)
    for i in range(len(a_name_l)):
        new_attract = attraction(big+i+1)
        new_attract.attraction_name = a_name_l[i]
        new_attract.attraction_city = city
        new_attract.attraction_state = state
        new_attract.attraction_country = country
        new_attract.description = descrip_l[i]
        new_attract.address = add_l[i]
        new_attract.save()

def city_attractions(city, state, country):
    city_a = attraction.objects.filter(attraction_city=city).filter(attraction_country=country).filter(attraction_state=state)
    if len(city_a):
        return city_a
    else:
        go_get_city_attractions(city, state, country)
        city_a = attraction.objects.filter(attraction_city=city).filter(attraction_country=country).filter(attraction_state=state)
        return city_a

"""
These are functions used to pull data from Google Maps used for optimizing travel
"""

# Function that collects address info from databases from list of attraction objects
def get_attraction_loc_inputs(a_l, utr):
    place_info = []
    for place in a_l:
        attraction_info = []
        attraction_info.append(place.attraction_name)
        attraction_info.append(place.address)
        attraction_info.append(utr.country)
        place_info.append(attraction_info)
    return place_info

def get_words(input):
    Boolean = True
    temp_input = input
    words = []
    while Boolean:
        location = temp_input.find(' ')
        if location != -1:
            curr_word = temp_input[:location]
            if curr_word[-1]==',':
                curr_word=curr_word[:-1]
            words.append(curr_word)
            temp_input = temp_input[location+1:]
        else:
            curr_word = temp_input
            words.append(curr_word)
            Boolean = False
    return words

# Constructs Google Maps Distance API
def get_url_google_maps(place_info):
    basic_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    url = basic_url
    url = url + 'origins='
    counter1 = 0
    for attraction_info in place_info:
        counter2 = 0
        for input in attraction_info:
            words = get_words(input)
            for word in words:
                if len(word)>0:
                    if counter2 == 0:
                        url = url+word
                    else:
                        url = url+'+'+word
                counter2 += 1
        if counter1 < len(place_info):
            url = url + '|'
        counter1 += 1
    url = url + '&'
    url = url + 'destinations='
    counter1 = 0
    for attraction_info in place_info:
        counter2 = 0
        for input in attraction_info:
            words = get_words(input)
            for word in words:
                if len(word)>0:
                    if counter2 == 0:
                        url = url+word
                    else:
                        url = url+'+'+word
                counter2 += 1
        if counter1 < len(place_info):
            url = url + '|'
        counter1 += 1
    url = url + '&'
    url = url + 'mode=driving'
    url = url + '&'
    url = url + 'key=AIzaSyAzHmT6y1B4DfLePx8Aspb6Kt9HRzSeSCQ'
    return url

# Get JSON object from Google Maps
def get_json_google_maps(url):
    response=ul.urlopen(url,timeout=5)
    response = response.read().decode('utf-8')
    response = json.loads(response)
    return response

# Gets durations from JSON object
def travel_durations(response):
    try:
        super_dictionary = response['rows']
        num_attractions = len(super_dictionary)
        durs = list()
        for i in range(num_attractions):
            dimension = []
            for j in range(num_attractions):
                dimension.append([])
            durs.append(dimension)
        count1 = 0
        for row in super_dictionary:
            count2 = 0
            for sub_dictionary in row['elements']:
                duration = sub_dictionary['duration']['value']
                durs[count1][count2]=duration
                count2 += 1
            count1 += 1
        return durs
    except:
        return None

# Writes travel durations to database.
def write_durations(a_l, utr, durs):
    attraction_num = len(a_l)
    for i in range(attraction_num):
        a1_num = a_l[i].attraction_number
        for j in range(attraction_num):
            a2_num = a_l[j].attraction_number
            if i!=j:
                try:
                    pairs = attraction_pair.objects.filter(user_trop_request=utr).filter(attraction=a_l[i])
                    for pair in pairs:
                        if pair.attraction_second_num == a2_num:
                            pair.duration = durs[i][j]
                            pair.save()
                except:
                    new_pair = attraction_pair(user_trop_request = utr, attraction=a_l[i])
                    new_pair.attraction_second_num = a2_num
                    new_pair.duration = durs[i][j]
                    new_pair.save()

"""
These are function for the linear programming optimizer
"""
# Gets basic parameters of problem from user_trop_request model
def create_params(utr):
    select_attract = utr.attract_list_nums
    select_attract = select_attract.split(',')
    num_attract = len(select_attract)
    for i in range(num_attract):
        select_attract[i]=int(select_attract[i])
    start = utr.start_time
    finish = utr.finish_time
    temp_start = datetime.datetime(2015, 1, 1, start.hour,start.minute,0)
    temp_finish = datetime.datetime(2015, 1, 1, finish.hour,finish.minute,0)
    delta = temp_finish-temp_start
    num_periods = int((delta.seconds/60)/20)+1
    return num_periods, num_attract, select_attract


# Creates a structure to store values for problem.
def define_value_matrix(num_periods, num_attract):
    values = list()
    for i in range(num_periods):
        values.append([])
    for item in values:
        for j in range(num_attract):
            item.append([])
    for item1 in values:
        for item2 in item1:
            for j in range(num_attract):
                item2.append([])
    return values

"""
To define a problem, we need to input the number of hours we are trying to schedule, how many periods we want to try to
schedule per hour, and the number of event-attractions we are considering in our scheduling.  The more periods per hour, the
more fine-grained the scheduling can be, but the more difficult the problem is to solve computationally.
"""
def sch_param(num_periods, num_attract):
    period = [str(i) for i in range(num_periods)]
    attract_start = [str(i) for i in range(num_attract)]
    attract_end = [str(i) for i in range(num_attract)]
    desirability_matrix = define_value_matrix(num_periods, num_attract)
    duration_matrix = define_value_matrix(num_periods, num_attract)
    return period, attract_start, attract_end, desirability_matrix, duration_matrix

# Gets desirabilities, durations
def get_values(utr, desirability_matrix, duration_matrix):
    num_periods, num_attract, select_attract = create_params(utr)
    for i in range(num_periods):
        for j in range(num_attract):
            for k in range(num_attract):
                attract1_num = select_attract[j]
                attract1 = get_object_or_404(attraction,pk=attract1_num)
                attract2_num = select_attract[k]
                attract_pair_cur = attraction_pair.objects.filter(user_trop_request=utr).filter(attraction=attract1)
                for event in attract_pair_cur:
                    if event.attraction_second_num == attract2_num:
                        desirability_matrix[i][j][k] = event.value
                        duration_matrix[i][j][k] = int(((event.duration)/60)/20)+1
    return desirability_matrix, duration_matrix

"""
The function below creates a linear programming problem.  The choices line defines the decision variables.  Each
decision variable corresponds to a period.  In addition, the attract_start corresponds to the starting place for the
event while the attract_end corresponds to the ending place for the event.  Thus, Choice_0_1_1 is the decision of
whether to start and end at attraction 1 during period 0.  Choice_13_2_4 is the decision of whether to be traveling
from attraction 2 to attraction 4 during period 13.  A value of 1 means "Yes."  A value of 0 means "No."  This function
restricts the values of these decision variables to 0 and 1.
"""
def define_problem(period, attract_start, attract_end):
    prob = pulp.LpProblem('Schedule_Vacay', pulp.LpMaximize)
    choices = pulp.LpVariable.dicts('Choice', (period, attract_start, attract_end), 0, 1, pulp.LpInteger)
    return prob, choices

"""
Adds objective function to problem.  It's the sum of desirabilities of events multiplied by periods doing the event.
So, desirabilities must be rates rather than totals.
"""
def add_objective(prob, choices, period, attract_start, attract_end, desirability_matrix):
    obj_dict = dict()
    for p in period:
        for a1 in attract_start:
            for a2 in attract_end:
                obj_dict[choices[p][a1][a2]]=desirability_matrix[int(p)][int(a1)][int(a2)]
    obj = pulp.LpAffineExpression(obj_dict)
    prob += obj

# Adds constraints that prevent multiple activities at same time
def add_time_exclusivity(prob, choices, period, attract_start, attract_end):
    for p in period:
        prob += pulp.lpSum([choices[p][a1][a2] for a1 in attract_start for a2 in attract_end]) <= 1

# Adds constraint that prevents activities from going over duration
def duration_limit(prob, choices, period, attract_start, attract_end, duration_matrix):
    for a1 in attract_start:
        for a2 in attract_end:
            prob += pulp.lpSum([choices[p][a1][a2] for p in period]) <= duration_matrix[0][int(a1)][int(a2)]

"""
A function for figuring out what the proximal periods are for an event with a given duration.  Proximal periods are
ones where one would expect to find that the event is still ongoing.  The add_one parameter allows one to find the range
required to find where the events starts and stops.
"""
def get_adjacent_periods(duration, period, max_period, add_one=False):
    period_num = int(period)
    end = period_num + duration
    start = period_num - duration
    if not add_one:
        adj = [str(x) for x in range(start+1, end, 1) if x>=0 and x<max_period]
    else:
        adj = [str(x) for x in range(start, end+1, 1) if x>=0 and x<max_period]
    return adj

# Adds constraints that assure same event periods are scheduled contiguously
def contiguity_constraint(prob, choices, period, attract_start, attract_end, duration_matrix):
    for a1 in attract_start:
        for a2 in attract_end:
            for p in period:
                adj = get_adjacent_periods(duration_matrix[int(p)][int(a1)][int(a2)], p, len(period))
                constr_dict = {}
                for item in adj:
                    constr_dict[choices[item][a1][a2]]=1
                constr_dict[choices[p][a1][a2]]=constr_dict[choices[p][a1][a2]]-duration_matrix[int(p)][int(a1)][int(a2)]
                duration_constraint = pulp.LpAffineExpression(constr_dict)
                prob += duration_constraint >= 0

# Adds constraints that assure events scheduled after initial are traveled to
def travel_constraint_1(prob, choices, period, attract_start, attract_end, duration_matrix):
    for a1 in attract_start:
        for a2 in attract_end:
            for p in period:
                adj = get_adjacent_periods(duration_matrix[int(p)][int(a1)][int(a2)], p, len(period), add_one=True)
                if int(p)<(len(period)-duration_matrix[int(p)][int(a1)][int(a2)]):
                    adj_high = [x for x in adj if int(x)>int(p)]
                    constr_dict_1 = {}
                    for time in adj_high:
                        for dest in attract_end:
                            if dest != a1 and a1==a2:
                                constr_dict_1[choices[time][a1][dest]]=1
                            elif dest == a2 and a1!=a2:
                                constr_dict_1[choices[time][a2][a2]]=1
                    if len(constr_dict_1)>0:
                        constr_dict_1[choices[p][a1][a2]]=-1
                        travel_constraint_1 = pulp.LpAffineExpression(constr_dict_1)
                        prob += travel_constraint_1 >= 0

# Adds constraints that assure events scheduled before final are traveled from
def travel_constraint_2(prob, choices, period, attract_start, attract_end, duration_matrix):
    for a1 in attract_start:
        for a2 in attract_end:
            for p in period:
                adj = get_adjacent_periods(duration_matrix[int(p)][int(a1)][int(a2)], p, len(period), add_one=True)
                if int(p)>duration_matrix[int(p)][int(a1)][int(a2)]:
                    adj_low = [x for x in adj if int(x)<int(p)]
                    constr_dict_2 = {}
                    for time in adj_low:
                        for begin in attract_start:
                            if begin != a2 and a1==a2:
                                constr_dict_2[choices[time][begin][a2]]=1
                            elif begin == a1 and a1!=a2:
                                constr_dict_2[choices[time][a1][a1]]=1
                    if len(constr_dict_2)>0:
                        constr_dict_2[choices[p][a1][a2]]=-1
                        travel_constraint_2 = pulp.LpAffineExpression(constr_dict_2)
                        prob += travel_constraint_2 >= 0

# Sets up the optimizer
def optimize_schedule_setup(utr):
    num_periods, num_attract, select_attract = create_params(utr)
    period, attract_start, attract_end, desirability_matrix, duration_matrix = sch_param(num_periods, num_attract)
    get_values(utr, desirability_matrix, duration_matrix)
    prob, choices = define_problem(period, attract_start, attract_end)
    add_objective(prob, choices, period, attract_start, attract_end, desirability_matrix)
    add_time_exclusivity(prob, choices, period, attract_start, attract_end)
    duration_limit(prob, choices, period, attract_start, attract_end, duration_matrix)
    contiguity_constraint(prob, choices, period, attract_start, attract_end, duration_matrix)
    travel_constraint_1(prob, choices, period, attract_start, attract_end, duration_matrix)
    travel_constraint_2(prob, choices, period, attract_start, attract_end, duration_matrix)
    return prob, choices, period, attract_start, attract_end, select_attract

# Runs the optimizer
def optimize(prob, choices, period, attract_start, attract_end, select_attract):
    prob.solve()
    optimized_schedule = []
    if prob.status==1:
        for p in period:
            for a1 in attract_start:
                for a2 in attract_end:
                    if pulp.value(choices[p][a1][a2])>0:
                        optimized_schedule.append([int(p), select_attract[int(a1)], select_attract[int(a2)]])
    return optimized_schedule

def make_more_readable(optimized_schedule):
    periods = []
    start_place = []
    end_place = []
    for item in optimized_schedule:
        periods.append(item[0])
        attract_1 = get_object_or_404(attraction, pk=item[1])
        attract_2 = get_object_or_404(attraction, pk=item[2])
        start_place.append(attract_1)
        end_place.append(attract_2)
    return periods, start_place, end_place

def write_solution(utr, periods, start_places, end_places):
    attract_pair_cur = attraction_pair.objects.filter(user_trop_request=utr)
    for i in range(len(periods)):
        for event in attract_pair_cur:
            if event.attraction == start_places[i] and event.attraction_second_num == end_places[i].attraction_number:
                new_output_event = output(user_trop_request=utr, attraction_pair=event)
                new_output_event.period = periods[i]
                new_output_event.save()

class event(object):
    def __init__(self, attraction1, attraction2):
        self.attraction1 = attraction1
        self.attraction2 = attraction2

    def __str__(self):
        if self.attraction1==self.attraction2:
            return self.attraction1.attraction_name
        else:
            return 'Travel from ' + self.attraction1.attraction_name + ' to ' + self.attraction2.attraction_name

class solution_row(object):
    def __init__(self, time, event):
        self.time = time
        self.event = event

"""
Below are the functions called by url requests
"""

def home(request):
    context = dict()
    return render(request,"home.html",context)

def make_trop_request(request):
    context = dict()
    user_city = request.GET['u_city']
    user_state = request.GET['u_state']
    user_country = request.GET['u_country']
    all_requests = trop_request.objects.all()
    big = 0
    for item in all_requests:
        big=max(item.request_number, big)
    new_utr = trop_request(request_number=big+1)
    new_utr.city = user_city
    new_utr.state = user_state
    new_utr.country = user_country
    new_utr.save()
    city_a = city_attractions(user_city, user_state, user_country)
    context['trop_num']= new_utr.request_number
    context['city']=user_city
    context['state']=user_state
    context['country']=user_country
    context['city_a']=city_a
    return render(request,"attractions.html",context)

def selections(request, trop_request_num):
    context = dict()
    context['trop_num']=trop_request_num
    utr = get_object_or_404(trop_request,pk=trop_request_num)
    selected_attractions = request.GET.getlist('Attractions List')
    city_a = []
    for thing in selected_attractions:
        attract_cur_q = attraction.objects.filter(attraction_city=utr.city).filter(attraction_country=utr.country).filter(attraction_state=utr.state).filter(attraction_name=thing)
        stuff = list()
        for x in attract_cur_q:
            stuff.append(x)
        if len(stuff):
            attract_cur = stuff[0]
            city_a.append(attract_cur)
    context['city_a']=city_a
    enter_attraction_pairs(city_a, utr)
    try:
        place_info = get_attraction_loc_inputs(city_a, utr)
        url = get_url_google_maps(place_info)
        durs = None
        i = 0
        while durs == None and i<3:
            response = get_json_google_maps(url)
            durs = travel_durations(response)
            i += 1
        if durs == None:
            pass
        else:
            write_durations(city_a, utr, durs)
    except:
        pass
    return render(request,"selections.html",context)

def schedule(request, trop_request_num):
    context = dict()
    context['trop_num']= trop_request_num
    utr = get_object_or_404(trop_request,pk=trop_request_num)
    str_nums = utr.attract_list_nums
    str_num_list = str_nums.split(',')
    vals = dict()
    duras = dict()
    for item in str_num_list:
        name = item + ' ' + 'duration'
        duras[item] = int(float(request.GET[name])*60*60)
        name = item + ' ' + 'value'
        vals[item] = int(request.GET[name])/(((duras[item]/60)/60)*3)
    attract_pairs_cur = attraction_pair.objects.filter(user_trop_request=utr)
    all_values = []
    for key in vals:
        all_values.append(vals[key])
    avg_value = sum(all_values)/len(all_values)
    for pair in attract_pairs_cur:
        for key in vals:
            if pair.attraction.attraction_number == int(key):
                if pair.attraction_second_num == int(key):
                    pair.value = vals[key]
                    pair.duration = duras[key]
                    pair.save()
                else:
                    pair.value = -avg_value/3
                    pair.save()
    return render(request,"schedule.html",context)

def optimize_schedule(request, trop_request_num):
    context = dict()
    context['trop_num']= trop_request_num
    start = request.GET['start']
    start = start.split(':')
    start = datetime.time(int(start[0]), int(start[1]), 0)
    finish = request.GET['finish']
    finish = finish.split(':')
    finish = datetime.time(int(finish[0]), int(finish[1]), 0)
    utr = get_object_or_404(trop_request,pk=trop_request_num)
    utr.start_time = start
    utr.finish_time = finish
    utr.save()
    prob, choices, period, attract_start, attract_end, select_attract = optimize_schedule_setup(utr)
    optimized_schedule = optimize(prob, choices, period, attract_start, attract_end, select_attract)
    periods, start_place, end_place = make_more_readable(optimized_schedule)
    write_solution(utr, periods, start_place, end_place)
    times = []
    start_time = datetime.datetime(2015, 1, 1, start.hour, start.minute)
    for i in range(len(periods)):
        time_= start_time + i * datetime.timedelta(minutes=20)
        print(time_)
        time_ = datetime.time(time_.hour, time_.minute)
        times.append(time_)
    solution_rows = []
    for i in range(len(periods)):
        e = event(start_place[i], end_place[i])
        s_r = solution_row(times[i], e)
        solution_rows.append(s_r)
    context['solution_rows']=solution_rows
    return render(request,"output.html",context)
