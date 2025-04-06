from flask import Flask, render_template, request, redirect, url_for, session
from cities_data import cities, get_weather_data
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DISEASE_FACTORS = {
    'adult': {
        'asthma': {'dust': 0.6, 'smoke': 0.6, 'pollen': 0.3},
        'vitiligo': {'uv_index': 0.9, 'temperature': 0.2},
        'psoriasis': {'uv_index': 0.6, 'humidity': 0.5},
        'bronchitis': {'dust': 0.5, 'smoke': 0.7, 'humidity': 0.4},
        'pollen_allergy': {'pollen': 0.9, 'wind': 0.2},
        'eczema': {'humidity': 0.7, 'temperature': 0.3},
        'lupus': {'uv_index': 0.9, 'temperature': 0.3},
        'copd': {'dust': 0.7, 'smoke': 0.8, 'humidity': 0.4}
    },
    'child': {
        'asthma': {'dust': 0.8, 'smoke': 0.8, 'pollen': 0.4},
        'eczema': {'humidity': 0.9, 'temperature': 0.4},
        'pollen_allergy': {'pollen': 0.9, 'wind': 0.3},
        'bronchitis': {'dust': 0.6, 'smoke': 0.8, 'humidity': 0.5}
    }
}
ALL_CONDITIONS = sorted(list(set(DISEASE_FACTORS['adult'].keys()).union(set(DISEASE_FACTORS['child'].keys()))))
CONDITION_RECOMMENDATIONS = {
    'asthma': [
        "Carry your inhaler at all times",
        "Consider wearing a mask in dusty areas",
        "Avoid outdoor activities during high pollution days"
    ],
    'vitiligo': [
        "Use high SPF sunscreen (50+)",
        "Wear protective clothing and wide-brimmed hats",
        "Avoid peak sun hours (10am-4pm)"
    ],
    'psoriasis': [
        "Moisturize frequently",
        "Use medicated creams as prescribed",
        "Consider moderate sun exposure but avoid burning"
    ],
    'bronchitis': [
        "Wear a mask in polluted areas",
        "Stay hydrated",
        "Avoid smoking and secondhand smoke"
    ],
    'pollen_allergy': [
        "Take antihistamines as prescribed",
        "Keep windows closed during high pollen times",
        "Shower after being outdoors to remove pollen"
    ],
    'eczema': [
        "Use fragrance-free moisturizers",
        "Avoid extreme temperature changes",
        "Wear soft, breathable fabrics"
    ],
    'lupus': [
        "Strict sun protection is essential",
        "Wear UV-protective clothing",
        "Stay hydrated and rest when needed"
    ],
    'copd': [
        "Avoid strenuous activities at high altitudes",
        "Carry supplemental oxygen if prescribed",
        "Stay indoors on poor air quality days"
    ]
}
@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    session['travel_type'] = request.form.get('travel_type')
    if session['travel_type'] == 'individual':
        return redirect(url_for('individual'))
    elif session['travel_type'] == 'group':  
        return redirect(url_for('group_size'))
    else:
        return redirect(url_for('index')) 

@app.route('/individual', methods=['GET', 'POST'])
def individual():
    if request.method == 'POST':
        session['user_data'] = {
            'age_group': request.form.get('age_group'),
            'conditions': request.form.getlist('conditions')
        }
        return redirect(url_for('results'))
    return render_template('individual.html', 
                         all_conditions=ALL_CONDITIONS,
                         adult_conditions=DISEASE_FACTORS['adult'].keys(),
                         child_conditions=DISEASE_FACTORS['child'].keys())
@app.route('/group_size', methods=['GET', 'POST'])
def group_size():
    if request.method == 'POST':
        session['group_size'] = int(request.form.get('group_size'))
        session['group_member'] = []
        return redirect(url_for('group_member', member_num=1))
    return render_template('group_size.html')

@app.route('/group_member/<int:member_num>', methods=['GET', 'POST'])
def group_member(member_num):
    if 'group_members' not in session:
        session['group_members'] = []

    if request.method == 'POST':
        # Debug print to see what we're receiving
        print(f"Processing member {member_num} of {session.get('group_size')}")
        print(f"Form data: {request.form}")
        
        member_data = {
            'age_group': request.form.get('age_group'),
            'conditions': request.form.getlist('conditions')
        }
        
        session['group_members'].append(member_data)
        session.modified = True  # Ensure session is saved
        
        # Debug print to see session content
        print(f"Current session members: {session['group_members']}")
        
        if member_num < session['group_size']:
            return redirect(url_for('group_member', member_num=member_num+1))
        else:
            return redirect(url_for('results'))
    
    return render_template('group_member.html',
                         member_num=member_num,
                         total_members=session['group_size'],
                         all_conditions=ALL_CONDITIONS,
                         DISEASE_FACTORS=DISEASE_FACTORS, 
                         child_conditions=DISEASE_FACTORS['child'].keys(),
                         adult_conditions=DISEASE_FACTORS['adult'].keys())
def calculate_risk_score(city, conditions, age_group):
    weather = get_weather_data(city['name'])
    score = 0
    
    for condition in conditions:
        if condition in DISEASE_FACTORS[age_group]:
            for factor, weight in DISEASE_FACTORS[age_group][condition].items():
                if factor == 'uv_index':
                    value = min(weather.get(factor, 0) / 12, 1)
                elif factor == 'temperature':
                    temp = weather.get(factor, 20)
                    value = min(abs(temp - 22) / 30, 1)
                elif factor in ['dust', 'smoke', 'pollen']:
                    value = min(weather.get(factor, 0) / 500, 1)
                elif factor == 'humidity':
                    humidity = weather.get(factor, 50)
                    value = min(abs(humidity - 50) / 50, 1)
                else:
                    value = 0
                
                score += value * weight
    
    return score / len(conditions) if conditions else 0

@app.route('/results')
def results():
    print("Entering results route")
    print(f"Session data: {dict(session)}")
    
    if 'travel_type' not in session:
        print("No travel_type in session, redirecting to index")
        return redirect(url_for('index'))
    
    if session['travel_type'] == 'individual':
        members = [session['user_data']]
    else:
        members = session.get('group_members', [])
    
    if not members:
        print("No members data found, redirecting to index")
        return redirect(url_for('index'))
    
    print(f"Processing results for {len(members)} members")
    
    city_scores = []
    recommendations = set()
    
    for city in cities:
        total_score = 0
        member_count = 0
        
        for member in members:
            if not member or 'conditions' not in member or not member['conditions']:
                continue
                
            member_score = calculate_risk_score(
                city,
                member['conditions'],
                member['age_group']
            )
            total_score += member_score
            member_count += 1
            for condition in member['conditions']:
                if condition in CONDITION_RECOMMENDATIONS:
                    for rec in CONDITION_RECOMMENDATIONS[condition]:
                        recommendations.add(rec)
        if member_count > 0:
            avg_score = total_score / member_count
            city_scores.append({
                'name': city['name'],
                'country': city['country'],
                'score': round(avg_score * 100, 1), 
                'weather': get_weather_data(city['name'])
            })
    ranked_cities = sorted(city_scores, key=lambda x: x['score'])
    
    return render_template('results.html',
                         cities=ranked_cities,
                         recommendations=sorted(list(recommendations)), 
                         travel_type=session['travel_type'])
if __name__ == '__main__':
    app.run(debug=True)
