from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseRedirect
from django.urls import reverse

# List of houses from Game of Thrones
houses = [
    {
        "id": 1,
        "house_name": "House Stark",
        "motto": "Winter is Coming",
        "home": "Winterfell",
        "motto_meaning": "A reminder of the inevitability of hardship and the need to prepare for difficult times ahead."
    },
    {
        "id": 2,
        "house_name": "House Lannister",
        "motto": "Hear Me Roar!",
        "home": "Casterly Rock",
        "motto_meaning": "A declaration of their power and dominance, meant to command respect and fear."
    },
    {
        "id": 3,
        "house_name": "House Targaryen",
        "motto": "Fire and Blood",
        "home": "Dragonstone",
        "motto_meaning": "A representation of their fiery nature and their willingness to conquer through destruction and strength."
    },
    {
        "id": 4,
        "house_name": "House Baratheon",
        "motto": "Ours is the Fury",
        "home": "Storm's End",
        "motto_meaning": "A warning of their tempestuous and aggressive approach to conflicts."
    },
    {
        "id": 5,
        "house_name": "House Greyjoy",
        "motto": "We Do Not Sow",
        "home": "Pyke",
        "motto_meaning": "A statement of their reaving and raiding culture, taking what they need rather than working for it."
    },
    {
        "id": 6,
        "house_name": "House Martell",
        "motto": "Unbowed, Unbent, Unbroken",
        "home": "Sunspear",
        "motto_meaning": "A reflection of their resilience and refusal to yield, no matter the circumstances."
    },
    {
        "id": 7,
        "house_name": "House Tyrell",
        "motto": "Growing Strong",
        "home": "Highgarden",
        "motto_meaning": "A subtle boast of their prosperity, ambition, and ever-increasing influence."
    },
    {
        "id": 8,
        "house_name": "House Tully",
        "motto": "Family, Duty, Honor",
        "home": "Riverrun",
        "motto_meaning": "An expression of their values, prioritizing family, fulfilling obligations, and maintaining integrity."
    },
    {
        "id": 9,
        "house_name": "House Arryn",
        "motto": "As High as Honor",
        "home": "The Eyrie",
        "motto_meaning": "A metaphor for their lofty ideals of nobility and their impregnable mountain stronghold."
    },
    {
        "id": 10,
        "house_name": "House Bolton",
        "motto": "Our Blades Are Sharp",
        "home": "The Dreadfort",
        "motto_meaning": "A sinister warning of their cruelty and efficiency in dealing with enemies."
    },
]




# Create your views here.
def home(request):
    # print(reverse('home', args = ['simar']))
    html = ''
    for house in houses:
        html += f'''
            <div>
                <a href="/house/{house['id']}/">
                    <h1>{house['id']}.{house['house_name']} ({(house['home'])})</h1>
                </a>
                <h2>{house['motto']}</h2>
                <p>{house['motto_meaning']}</p>
               
            </div>
'''
    # return HttpResponse(html)
    return render(request, 'posts/home.html')


def house(request,id):
    valid_id = False
    for house in houses:
        if house['id'] == id:
            house_dict = house 
            valid_id = True
            break
    if valid_id:
        html = f'''
                <h2>{house_dict['house_name']}</h2>
                <p>{house_dict['motto_meaning']}</p>
            '''
        # print(type(id))
        return HttpResponse(html)
    else:
        return HttpResponseNotFound('House not available')
    
    
def google(request,id):
    url = reverse('house', args = [id])
    return HttpResponseRedirect(url) 