# trip_planner/views.py
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging

# Import only the call_agent function
from .agent import call_agent

logger = logging.getLogger(__name__)


def vacation_planner(request):
    """Main vacation planner page - returns HTML directly."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Odyssey - AI Vacation Planner</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .hero-section { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 80px 0; 
        }
        .card-custom { 
            border: none; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
            margin-bottom: 20px;
        }
        .loading { 
            display: none; 
        }
        .ai-response { 
            background: #f8f9fa; 
            border-left: 4px solid #007bff; 
            padding: 20px; 
            margin: 20px 0; 
            border-radius: 5px; 
            white-space: pre-wrap; 
            line-height: 1.6; 
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-plane"></i> Your Odyssey - AI Travel Planner
            </a>
        </div>
    </nav>

    <div class="hero-section text-center">
        <div class="container">
            <h1 class="display-4 mb-4">AI-Powered Vacation Planner</h1>
            <p class="lead">Get personalized travel plans with comprehensive recommendations</p>
        </div>
    </div>

    <div class="container my-5">
        <div class="card card-custom">
            <div class="card-header bg-primary text-white">
                <h3><i class="fas fa-robot"></i> Plan Your Trip with AI</h3>
            </div>
            <div class="card-body">
                <div class="row mb-3">
                    <div class="col-md-4">
                        <label class="form-label">Destination</label>
                        <input type="text" class="form-control" id="destination" placeholder="e.g., Paris, Tokyo, Rome">
                    </div>
                    <div class="col-md-2">
                        <label class="form-label">Days</label>
                        <select class="form-select" id="days">
                            <option value="3" selected>3 days</option>
                            <option value="5">5 days</option>
                            <option value="7">7 days</option>
                            <option value="10">10 days</option>
                            <option value="14">14 days</option>
                        </select>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label">Budget</label>
                        <select class="form-select" id="budget">
                            <option value="low">Budget-Friendly</option>
                            <option value="medium" selected>Mid-Range</option>
                            <option value="high">Luxury</option>
                        </select>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label">&nbsp;</label>
                        <button class="btn btn-success w-100" onclick="planTrip()">
                            <i class="fas fa-magic"></i> Create AI Plan
                        </button>
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-12">
                        <button class="btn btn-outline-info" onclick="askQuestion()">
                            <i class="fas fa-question-circle"></i> Ask AI About Travel
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <div class="loading text-center my-5" id="loading">
            <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;"></div>
            <p class="mt-3">Your AI assistant is researching and planning...</p>
        </div>

        <div id="results"></div>
    </div>

    <script>
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').innerHTML = '';
        }

        function hideLoading() {
            document.getElementById('loading').style.display = 'none';
        }

        function planTrip() {
            const destination = document.getElementById('destination').value;
            const days = document.getElementById('days').value;
            const budget = document.getElementById('budget').value;

            if (!destination) {
                alert('Please enter a destination');
                return;
            }

            showLoading();

            fetch('/comprehensive-plan/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    destination: destination,
                    days: parseInt(days),
                    budget_level: budget
                })
            })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                if (data.success) {
                    showResult('AI Travel Plan for ' + destination, data.plan.ai_comprehensive_response);
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                hideLoading();
                alert('Error: ' + error);
            });
        }

        function askQuestion() {
            const question = prompt('Ask your AI travel assistant anything:\\n\\nExamples:\\n- "What should I pack for Japan in winter?"\\n- "Tell me about French dining etiquette"\\n- "Plan a European adventure for me"');

            if (!question) return;

            showLoading();

            fetch('/chat/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: question})
            })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                if (data.success) {
                    showResult('AI Assistant Answer', data.response);
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                hideLoading();
                alert('Error: ' + error);
            });
        }

        function showResult(title, content) {
            document.getElementById('results').innerHTML = `
                <div class="card card-custom">
                    <div class="card-header bg-success text-white">
                        <h4><i class="fas fa-robot"></i> ${title}</h4>
                    </div>
                    <div class="card-body">
                        <div class="ai-response">${content}</div>
                    </div>
                </div>
            `;
        }
    </script>
</body>
</html>"""
    return HttpResponse(html)


@csrf_exempt
def comprehensive_plan_view(request):
    """Comprehensive trip planning endpoint."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            destination = data.get('destination', '')
            days = data.get('days', 3)
            budget_level = data.get('budget_level', 'medium')

            # Create natural language prompt for the AI
            prompt = f"Create a comprehensive {days}-day vacation plan for {destination} with a {budget_level} budget level."

            logger.info(f"Processing comprehensive plan request for {destination}")
            agent_response = call_agent(prompt)
            logger.info(f"Agent response generated successfully")

            return JsonResponse({
                'success': True,
                'plan': {
                    'ai_comprehensive_response': agent_response
                }
            })

        except Exception as e:
            logger.error(f"Error in comprehensive_plan_view: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
def chat_view(request):
    """General chat endpoint for travel questions."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')

            if not message:
                return JsonResponse({
                    'success': False,
                    'error': 'No message provided'
                })

            logger.info(f"Processing chat request: {message}")
            agent_response = call_agent(message)
            logger.info(f"Chat response generated successfully")

            return JsonResponse({
                'success': True,
                'response': agent_response
            })

        except Exception as e:
            logger.error(f"Error in chat_view: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return JsonResponse({'success': False, 'error': 'Invalid request method'})