#!/usr/bin/env python3
"""Seed demo follows and saved trips for development.

Run from the backend folder:
  python3 scripts/seed_demo.py

This will create some follows for follower 'auth0|me' and add example saved trips
for the followed users so the frontend can display them.
"""
import json
import importlib.util
import os

# Import trip_planner/db.py directly to avoid importing package-level modules that
# may pull heavy dependencies (like google.generativeai) during this dev-only script.
db_path = os.path.join(os.path.dirname(__file__), '..', 'trip_planner', 'db.py')
spec = importlib.util.spec_from_file_location('tp_db', db_path)
tp_db = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tp_db)


def seed():
    tp_db.init_db()

    follower = 'auth0|me'
    people = [
        {
            'id': 'auth0|alice',
            'name': 'Alice Moreno',
            'username': 'alice.m',
            'bio': 'Weekend city escapes | coffee snob | amateur street photographer',
            'picture': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&h=400&fit=crop'
        },
        {
            'id': 'auth0|bob',
            'name': 'Robert "Bob" Chen',
            'username': 'bob_travels',
            'bio': 'Backpacker & photographer. Always planning the next train route.',
            'picture': 'https://images.unsplash.com/photo-1527980965255-d3b416303d12?w=400&h=400&fit=crop'
        },
        {
            'id': 'auth0|sarah',
            'name': 'Sarah Kumari',
            'username': 'sarahk',
            'bio': 'Food-first traveler. Markets, street food, and night walks.',
            'picture': 'https://images.unsplash.com/photo-1547425260-76bcadfb4f2c?w=400&h=400&fit=crop'
        },
    ]

    print('Seeding follows...')
    for p in people:
        rowid = tp_db.save_follow(follower, p['id'], name=p['name'], username=p['username'], bio=p.get('bio'), picture=None)
        print(f'  follow id={rowid} -> {p["id"]}')

    print('Seeding saved trips for followed users...')

    for p in people:
        # create two richer itineraries per user with realistic dates and activities
        itin1 = {
            'destination': f"{p['name'].split()[0]}'s Weekend in Lisbon",
            'duration': 3,
            'destination_info': {'name': 'Lisbon, Portugal'},
            'cover_photo': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1200&h=600&fit=crop',
            'days': [
                {'day': 1, 'date': '2025-11-01', 'theme': 'Arrival & Alfama walk', 'activities': [
                    'Coffee at local cafe', 'Walk through Alfama', 'Fado house dinner'
                ]},
                {'day': 2, 'date': '2025-11-02', 'theme': 'Belém & museums', 'activities': [
                    'Visit Jerónimos Monastery', 'Pastéis de Belém tasting', 'MAAT museum'
                ]},
                {'day': 3, 'date': '2025-11-03', 'theme': 'Coast day', 'activities': [
                    'Train to Cascais', 'Beach time', 'Seafood dinner'
                ]}
            ]
        }
        rowid = tp_db.save_itinerary(p['id'], json.dumps(itin1))
        print(f'  saved_trip id={rowid} for user={p["id"]} dest={itin1["destination"]}')

        itin2 = {
            'destination': f"{p['name'].split()[0]}'s Autumn Hike",
            'duration': 5,
            'destination_info': {'name': 'Lake District, UK'},
            'cover_photo': 'https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1200&h=600&fit=crop',
            'days': [
                {'day': 1, 'date': '2025-09-15', 'theme': 'Arrival & settle', 'activities': [
                    'Check in B&B', 'Short lakeside walk'
                ]},
                {'day': 2, 'date': '2025-09-16', 'theme': 'Long hike', 'activities': [
                    'Full day hike to Helvellyn', 'Picnic lunch'
                ]},
                {'day': 3, 'date': '2025-09-17', 'theme': 'Village exploring', 'activities': [
                    'Visit local market', 'Pub dinner'
                ]}
            ]
        }
        rowid = tp_db.save_itinerary(p['id'], json.dumps(itin2))
        print(f'  saved_trip id={rowid} for user={p["id"]} dest={itin2["destination"]}')

    # also add a saved trip for the current user
    my_itin = {
        'destination': "Gagen's Test Roadtrip",
        'duration': 6,
        'destination_info': {'name': 'Pacific Coast'},
        'cover_photo': 'https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1200&h=600&fit=crop',
        'days': [
            {'day': 1, 'date': '2025-10-05', 'theme': 'Kickoff', 'activities': ['Drive to first viewpoint', 'Sunset photos']},
            {'day': 2, 'date': '2025-10-06', 'theme': 'Coastal drive', 'activities': ['Explore seaside towns', 'Fresh seafood']}
        ]
    }
    my_row = tp_db.save_itinerary(follower, json.dumps(my_itin))
    print(f'  saved_trip id={my_row} for current user={follower}')

    # Add a full Paris itinerary for Sarah (richer structure similar to sample)
    paris_itin = {
        'destination': 'France',
        'duration': 5,
        'destination_info': {
            'name': 'France',
            'language': 'French',
            'currency': 'Euro (€)',
            'best_time_to_visit': 'April-May, September-October',
            'cultural_tips': [
                "Always greet people with 'Bonjour' before asking a question.",
                'Tipping is not always required, but rounding up is appreciated for good service.',
                'Dress respectfully when visiting religious sites.'
            ]
        },
        'outbound_transport': {
            'departure_location': 'New York City (JFK)',
            'arrival_location': 'Paris Charles de Gaulle Airport (CDG)',
            'transport_type': 'Flight',
            'duration': '7-8 hours',
            'estimated_cost': '$600-1200 USD (roundtrip, economy)'
        },
        'return_transport': {
            'departure_location': 'Paris Charles de Gaulle Airport (CDG)',
            'arrival_location': 'New York City (JFK)',
            'transport_type': 'Flight',
            'duration': '8-9 hours'
        },
        'practical_info': {
            'emergency_info': 'Dial 112 for emergencies. The U.S. Embassy in Paris is located at 2 Avenue Gabriel, 75008 Paris.',
            'important_phrases': {'excuse me': 'Excusez-moi', 'hello': 'Bonjour', 'please': "S'il vous plaît", 'thank you': 'Merci'},
            'total_estimated_budget': '$1500-2500 USD (excluding flights and accommodation)'
        },
        'days': [
            {
                'day': 1,
                'date': 'Day 1',
                'theme': 'Arrival and Parisian Charm',
                'total_estimated_cost': '$70-120 USD',
                'transportation_notes': 'Use the Paris Metro (purchase a Navigo Découverte pass for unlimited travel within zones 1-5), or walk.',
                'activities': [
                    {
                        'name': 'Eiffel Tower Visit',
                        'category': 'sightseeing',
                        'description': 'Ascend the Eiffel Tower for panoramic views of Paris.',
                        'duration': '2-3 hours',
                        'estimated_cost': '$30-40 USD (elevator access)',
                        'address': 'Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France',
                        'location': 'Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France',
                        'opening_hours': '9:30 AM - 11:00 PM',
                        'phone': '+33 892 70 12 39',
                        'rating': 4.7,
                        'tips': 'Book tickets online in advance to avoid long queues. Visit during sunset for stunning views.',
                        'website': 'https://www.toureiffel.paris/en'
                    },
                    {
                        'name': 'Seine River Cruise',
                        'category': 'sightseeing',
                        'description': 'Enjoy a relaxing boat tour along the Seine River, passing iconic landmarks.',
                        'duration': '1-1.5 hours',
                        'estimated_cost': '$15-25 USD',
                        'address': 'Bateaux Mouches: Port de la Conférence, Pont de l\'Alma, 75008 Paris, France',
                        'location': 'Various departure points along the Seine',
                        'opening_hours': 'Varies depending on the company and time of year',
                        'phone': '+33 1 42 25 96 10',
                        'rating': 4.4,
                        'tips': 'Choose a cruise with live commentary for a more informative experience. Evening cruises are particularly romantic.',
                        'website': 'https://www.bateaux-mouches.fr/'
                    },
                    {
                        'name': 'Dinner at a Traditional Bistro',
                        'category': 'food',
                        'description': 'Savor classic French cuisine in a charming bistro setting.',
                        'duration': '1.5-2 hours',
                        'estimated_cost': '$25-40 USD',
                        'address': "L'As du Fallafel: 34 Rue des Rosiers, 75004 Paris, France",
                        'location': 'Le Marais district',
                        'opening_hours': '11:00 AM - 12:00 AM',
                        'phone': '+33 1 48 87 63 60',
                        'rating': 4.2,
                        'tips': 'Try steak frites, coq au vin, or onion soup. Make reservations, especially on weekends.',
                        'website': None
                    }
                ]
            },
            {
                'day': 2,
                'date': 'Day 2',
                'theme': 'Art, History, and Gardens',
                'total_estimated_cost': '$50-75 USD',
                'transportation_notes': 'Use the Paris Metro, walk between locations, or take a bus.',
                'activities': [
                    {
                        'name': 'Louvre Museum Visit',
                        'category': 'culture',
                        'description': 'Explore the world-renowned Louvre Museum and admire masterpieces like the Mona Lisa.',
                        'duration': '3-4 hours',
                        'estimated_cost': '$20-25 USD',
                        'address': 'Musée du Louvre: Rue de Rivoli, 75001 Paris, France',
                        'location': '1st arrondissement',
                        'opening_hours': '9:00 AM - 6:00 PM (closed Tuesdays)',
                        'phone': '+33 1 40 20 53 17',
                        'rating': 4.6,
                        'tips': 'Book tickets online in advance to skip the line. Focus on specific wings or collections to avoid feeling overwhelmed.',
                        'website': 'https://www.louvre.fr/'
                    },
                    {
                        'name': 'Notre Dame Cathedral (Exterior)',
                        'category': 'sightseeing',
                        'description': 'View the exterior of the iconic Notre Dame Cathedral, currently under reconstruction.',
                        'duration': '30-45 minutes',
                        'estimated_cost': 'Free',
                        'address': '6 Parvis Notre-Dame - Place Jean-Paul II, 75004 Paris, France',
                        'location': 'Île de la Cité',
                        'opening_hours': 'Exterior view is available anytime',
                        'phone': None,
                        'rating': 4.5,
                        'tips': 'Check the progress of the reconstruction. There are often informative displays nearby.',
                        'website': None
                    },
                    {
                        'name': 'Luxembourg Gardens',
                        'category': 'sightseeing',
                        'description': 'Relax and stroll through the beautiful Luxembourg Gardens.',
                        'duration': '1-2 hours',
                        'estimated_cost': 'Free',
                        'address': 'Jardin du Luxembourg: Rue de Médicis - Rue de Vaugirard, 75006 Paris, France',
                        'location': '6th arrondissement',
                        'opening_hours': 'Varies depending on the season',
                        'phone': None,
                        'rating': 4.7,
                        'tips': 'Enjoy a picnic, rent a small boat on the pond, or watch a puppet show (for kids).',
                        'website': 'https://en.parisinfo.com/paris-museum-monument/71365/Jardin-du-Luxembourg'
                    },
                    {
                        'name': 'Dinner in Saint-Germain-des-Prés',
                        'category': 'food',
                        'description': 'Enjoy dinner at a restaurant in the charming Saint-Germain-des-Prés neighborhood.',
                        'duration': '1.5-2 hours',
                        'estimated_cost': '$30-50 USD',
                        'address': 'Les Deux Magots: 6 Place Saint-Germain des Prés, 75006 Paris, France',
                        'location': 'Saint-Germain-des-Prés',
                        'opening_hours': '7:30 AM - 1:00 AM',
                        'phone': '+33 1 45 48 55 25',
                        'rating': 4.3,
                        'tips': "Try a café crème or a classic French pastry.",
                        'website': 'https://www.lesdeuxmagots.fr/en/'
                    }
                ]
            },
            {
                'day': 3,
                'date': 'Day 3',
                'theme': 'Day Trip to Versailles',
                'total_estimated_cost': '$75-100 USD',
                'transportation_notes': 'Take the RER C train from Paris to Versailles-Château-Rive Gauche station (approx. 45 minutes, ~$8-10 USD each way).',
                'activities': [
                    {
                        'name': 'Palace of Versailles',
                        'category': 'history',
                        'description': 'Explore the opulent Palace of Versailles, the former residence of French royalty.',
                        'duration': '4-5 hours',
                        'estimated_cost': '$20-30 USD (entry fee)',
                        'address': 'Place d\'Armes, 78000 Versailles, France',
                        'location': 'Versailles',
                        'opening_hours': '9:00 AM - 6:30 PM (closed Mondays)',
                        'phone': '+33 1 30 83 78 00',
                        'rating': 4.7,
                        'tips': 'Book tickets online in advance to avoid long queues. Explore the gardens and the Hall of Mirrors.',
                        'website': 'https://en.chateauversailles.fr/'
                    },
                    {
                        'name': 'Gardens of Versailles',
                        'category': 'sightseeing',
                        'description': 'Wander through the extensive and beautifully landscaped Gardens of Versailles.',
                        'duration': '2-3 hours',
                        'estimated_cost': 'Included in Palace ticket or separate entry',
                        'address': 'Place d\'Armes, 78000 Versailles, France',
                        'location': 'Versailles',
                        'opening_hours': '8:00 AM - 8:30 PM (varies by season)',
                        'phone': '+33 1 30 83 78 00',
                        'rating': 4.8,
                        'tips': 'Rent a bike or golf cart to explore the vast gardens. Visit the fountains shows (check schedule).',
                        'website': 'https://en.chateauversailles.fr/'
                    },
                    {
                        'name': 'Dinner near Versailles',
                        'category': 'food',
                        'description': 'Enjoy dinner at a restaurant in Versailles before returning to Paris.',
                        'duration': '1.5-2 hours',
                        'estimated_cost': '$25-40 USD',
                        'address': 'La Flotille: Parc du Château de Versailles, 78000 Versailles, France',
                        'location': 'Versailles',
                        'opening_hours': '12:00 PM - 5:00 PM, 7:00 PM - 11:00 PM',
                        'phone': '+33 1 39 51 41 58',
                        'rating': 4.1,
                        'tips': 'Try a traditional French crepe.',
                        'website': None
                    }
                ]
            },
            {
                'day': 4,
                'date': 'Day 4',
                'theme': 'Montmartre and Parisian Markets',
                'total_estimated_cost': '$60-90 USD',
                'transportation_notes': 'Use the Paris Metro (lines 2 and 12 to Abbesses or Anvers station). Walk around Montmartre.',
                'activities': [
                    {
                        'name': 'Montmartre Exploration',
                        'category': 'sightseeing',
                        'description': 'Explore the artistic neighborhood of Montmartre, including Sacré-Cœur Basilica.',
                        'duration': '3-4 hours',
                        'estimated_cost': 'Free (Basilica entry), Funicular: $2',
                        'address': 'Sacré-Cœur Basilica: 35 Rue du Chevalier de la Barre, 75018 Paris, France',
                        'location': 'Montmartre, 18th arrondissement',
                        'opening_hours': '6:00 AM - 10:30 PM',
                        'phone': '+33 1 53 41 89 00',
                        'rating': 4.7,
                        'tips': 'Take the funicular up to the Basilica to avoid the steep stairs. Visit Place du Tertre to see artists at work.',
                        'website': 'http://www.sacre-coeur-montmartre.com/'
                    },
                    {
                        'name': 'Marché des Enfants Rouges',
                        'category': 'food',
                        'description': "Visit Paris' oldest covered market for a delicious lunch and local products.",
                        'duration': '1-2 hours',
                        'estimated_cost': '$15-30 USD',
                        'address': '39 Rue de Bretagne, 75003 Paris, France',
                        'location': 'Le Marais',
                        'opening_hours': '8:30 AM - 8:30 PM (closed Mondays)',
                        'phone': '+33 1 42 72 20 92',
                        'rating': 4.5,
                        'tips': 'Try the Moroccan or Lebanese food stalls. Browse the fresh produce and cheese vendors.',
                        'website': None
                    },
                    {
                        'name': 'Picasso Museum',
                        'category': 'culture',
                        'description': 'Explore the Picasso Museum dedicated to the life and work of Pablo Picasso.',
                        'duration': '2-3 hours',
                        'estimated_cost': '$15 USD',
                        'address': '5 Rue de Thorigny, 75003 Paris, France',
                        'location': 'Le Marais',
                        'opening_hours': '10:30 AM - 6:00 PM (closed Mondays)',
                        'phone': '+33 1 85 56 00 36',
                        'rating': 4.4,
                        'tips': 'Book tickets online to skip the line. Admire the museum\'s architecture.',
                        'website': 'https://www.museepicassoparis.fr/en/'
                    },
                    {
                        'name': 'Dinner in Montmartre',
                        'category': 'food',
                        'description': 'Enjoy dinner at a restaurant in Montmartre.',
                        'duration': '1.5-2 hours',
                        'estimated_cost': '$25-40 USD',
                        'address': 'Le Consulat: 18 Rue Norvins, 75018 Paris, France',
                        'location': 'Montmartre',
                        'opening_hours': '11:00 AM - 12:00 AM',
                        'phone': '+33 1 42 62 70 00',
                        'rating': 4.2,
                        'tips': 'Try the traditional French cuisine.',
                        'website': None
                    }
                ]
            },
            {
                'day': 5,
                'date': 'Day 5',
                'theme': 'Shopping and Departure',
                'total_estimated_cost': '$30-50 USD (excluding shopping)',
                'transportation_notes': 'Use the Paris Metro or RER B train to reach Charles de Gaulle Airport (CDG). Consider a taxi or Uber for convenience.',
                'activities': [
                    {
                        'name': 'Champs-Élysées Shopping',
                        'category': 'shopping',
                        'description': 'Stroll along the Champs-Élysées, browsing luxury shops and flagship stores.',
                        'duration': '2-3 hours',
                        'estimated_cost': 'Variable (depending on purchases)',
                        'address': 'Avenue des Champs-Élysées, 75008 Paris, France',
                        'location': '8th arrondissement',
                        'rating': 4.3,
                        'website': None
                    },
                    {
                        'name': 'Galeries Lafayette or Printemps Department Store',
                        'category': 'shopping',
                        'description': "Visit one of Paris' iconic department stores for a unique shopping experience.",
                        'duration': '2-3 hours',
                        'estimated_cost': 'Variable (depending on purchases)',
                        'address': 'Galeries Lafayette: 40 Boulevard Haussmann, 75009 Paris, France',
                        'location': '9th arrondissement',
                        'opening_hours': '10:00 AM - 8:00 PM (varies by day)',
                        'phone': '+33 1 42 82 34 56',
                        'rating': 4.6,
                        'website': 'https://www.galerieslafayette.com/'
                    },
                    {
                        'name': 'Departure Preparation',
                        'category': 'transport',
                        'description': 'Head to the airport for your departure flight.',
                        'duration': '3-4 hours (travel and check-in)',
                        'estimated_cost': '$15-20 USD (transport to airport)',
                        'address': '95700 Roissy-en-France, France',
                        'location': 'Paris Charles de Gaulle Airport (CDG)'
                    }
                ]
            }
        ]
    }
    paris_row = tp_db.save_itinerary('auth0|sarah', json.dumps(paris_itin))
    print(f'  saved_trip id={paris_row} for user=auth0|sarah dest=France (Paris)')

    # Variant: Tokyo itinerary for Alice
    tokyo_itin = {
        'destination': 'Japan',
        'duration': 5,
        'destination_info': {'name': 'Japan', 'language': 'Japanese', 'currency': 'Yen (¥)'},
        'days': [
            {'day': 1, 'date': 'Day 1', 'theme': 'Arrival & Shinjuku', 'activities': [
                {'name': 'Metropolitan Government Building', 'category': 'sightseeing', 'description': 'Free observation decks with skyline views.'},
                {'name': 'Omoide Yokocho', 'category': 'food', 'description': 'Tiny izakaya alleys for an atmospheric dinner.'}
            ]},
            {'day': 2, 'date': 'Day 2', 'theme': 'Asakusa & Ueno', 'activities': [
                {'name': 'Senso-ji Temple', 'category': 'culture', 'description': 'Historic temple in Asakusa.'},
                {'name': 'Ameya-Yokocho Market', 'category': 'food', 'description': 'Street food and market stalls.'}
            ]},
            {'day': 3, 'date': 'Day 3', 'theme': 'Harajuku & Shibuya', 'activities': [
                {'name': 'Meiji Shrine', 'category': 'sightseeing', 'description': 'Peaceful shrine near Harajuku.'},
                {'name': 'Shibuya Crossing', 'category': 'sightseeing', 'description': 'Iconic busy intersection.'}
            ]},
            {'day': 4, 'date': 'Day 4', 'theme': 'Day trip to Nikko', 'activities': [
                {'name': 'Toshogu Shrine', 'category': 'history', 'description': 'UNESCO site with ornate shrines.'}
            ]},
            {'day': 5, 'date': 'Day 5', 'theme': 'Shopping & Departure', 'activities': [
                {'name': 'Ginza Shopping', 'category': 'shopping', 'description': 'High-end shopping district.'}
            ]}
        ]
    }
    tokyo_row = tp_db.save_itinerary('auth0|alice', json.dumps(tokyo_itin))
    print(f'  saved_trip id={tokyo_row} for user=auth0|alice dest=Japan (Tokyo)')

    # Variant: New York itinerary for Bob
    ny_itin = {
        'destination': 'United States',
        'duration': 5,
        'destination_info': {'name': 'United States', 'language': 'English', 'currency': 'USD ($)'},
        'days': [
            {'day': 1, 'date': 'Day 1', 'theme': 'Arrival & Midtown', 'activities': [
                {'name': 'Times Square', 'category': 'sightseeing', 'description': 'Bright lights and Broadway vibes.'},
                {'name': 'Broadway Show', 'category': 'culture', 'description': 'Catch a popular musical or play.'}
            ]},
            {'day': 2, 'date': 'Day 2', 'theme': 'Central Park & Museums', 'activities': [
                {'name': 'Central Park walk', 'category': 'sightseeing', 'description': 'Relaxed stroll and boat rental.'},
                {'name': 'Metropolitan Museum of Art', 'category': 'culture', 'description': 'World-class art collections.'}
            ]},
            {'day': 3, 'date': 'Day 3', 'theme': 'Lower Manhattan', 'activities': [
                {'name': '9/11 Memorial', 'category': 'history', 'description': 'Reflective memorial site.'},
                {'name': 'Statue of Liberty ferry', 'category': 'sightseeing', 'description': 'Ferry to Liberty Island.'}
            ]},
            {'day': 4, 'date': 'Day 4', 'theme': 'Brooklyn', 'activities': [
                {'name': 'Brooklyn Bridge walk', 'category': 'sightseeing', 'description': 'Walk across to Brooklyn Heights.'},
                {'name': 'DUMBO photos', 'category': 'sightseeing', 'description': 'Iconic Manhattan views.'}
            ]},
            {'day': 5, 'date': 'Day 5', 'theme': 'Shopping & Departure', 'activities': [
                {'name': 'Fifth Avenue shopping', 'category': 'shopping', 'description': 'High-end department stores and boutiques.'}
            ]}
        ]
    }
    ny_row = tp_db.save_itinerary('auth0|bob', json.dumps(ny_itin))
    print(f'  saved_trip id={ny_row} for user=auth0|bob dest=United States (New York)')

    print('Seeding complete.')


if __name__ == '__main__':
    seed()
