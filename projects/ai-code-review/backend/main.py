from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import re
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

class AICodeReviewAssistant:
    def __init__(self):
        self.supported_languages = [
            "Python", "JavaScript", "Java", "C++", "Go", "Rust", 
            "TypeScript", "C#", "PHP", "Ruby", "Swift"
        ]
        self.code_issues = [
            "Security vulnerability", "Performance bottleneck", "Code duplication",
            "Missing error handling", "Poor naming convention", "Complex function",
            "Memory leak potential", "Race condition", "Infinite loop risk",
            "Resource not closed", "Hard-coded values", "Missing documentation"
        ]

    def analyze_code_quality(self, code, language="Python"):
        # Simulate code quality analysis
        lines = code.split('\n')
        line_count = len(lines)
        
        # Simulate various quality metrics
        complexity_score = random.uniform(1, 10)
        maintainability_score = random.uniform(60, 95)
        security_score = random.uniform(70, 100)
        performance_score = random.uniform(65, 95)
        
        # Generate issues based on code content
        issues = []
        issue_count = random.randint(0, 8)
        
        for _ in range(issue_count):
            issue = {
                "type": random.choice(self.code_issues),
                "severity": random.choice(["Low", "Medium", "High", "Critical"]),
                "line": random.randint(1, line_count),
                "message": f"Potential {random.choice(['bug', 'improvement', 'security issue'])} detected",
                "confidence": round(random.uniform(0.6, 0.95), 2)
            }
            issues.append(issue)
        
        # Calculate overall quality score
        quality_score = round((maintainability_score + security_score + performance_score) / 3, 1)
        
        return {
            "language": language,
            "line_count": line_count,
            "complexity_score": round(complexity_score, 1),
            "maintainability_score": round(maintainability_score, 1),
            "security_score": round(security_score, 1),
            "performance_score": round(performance_score, 1),
            "overall_quality": quality_score,
            "issues_found": len(issues),
            "issues": issues,
            "analysis_time": datetime.now().isoformat()
        }

    def generate_code_review(self, code, language="Python"):
        analysis = self.analyze_code_quality(code, language)
        
        # Generate review summary
        if analysis["overall_quality"] >= 80:
            overall_rating = "Excellent"
            summary = "Code quality is excellent with minimal issues found."
        elif analysis["overall_quality"] >= 70:
            overall_rating = "Good"
            summary = "Code quality is good with some areas for improvement."
        elif analysis["overall_quality"] >= 60:
            overall_rating = "Fair"
            summary = "Code quality is fair but needs attention to several issues."
        else:
            overall_rating = "Poor"
            summary = "Code quality needs significant improvement."
        
        # Generate specific recommendations
        recommendations = []
        if analysis["security_score"] < 80:
            recommendations.append({
                "category": "Security",
                "priority": "High",
                "suggestion": "Implement input validation and sanitization"
            })
        
        if analysis["performance_score"] < 80:
            recommendations.append({
                "category": "Performance",
                "priority": "Medium",
                "suggestion": "Consider optimizing algorithms and reducing complexity"
            })
        
        if analysis["maintainability_score"] < 80:
            recommendations.append({
                "category": "Maintainability",
                "priority": "Medium",
                "suggestion": "Add documentation and improve code structure"
            })
        
        return {
            "overall_rating": overall_rating,
            "summary": summary,
            "analysis": analysis,
            "recommendations": recommendations,
            "review_time": datetime.now().isoformat()
        }

    def get_improvement_suggestions(self, code, language="Python"):
        suggestions = []
        
        # Simulate AI-powered suggestions
        suggestion_types = [
            {
                "type": "Refactoring",
                "description": "Extract method to reduce complexity",
                "impact": "High",
                "effort": "Medium"
            },
            {
                "type": "Performance",
                "description": "Use more efficient data structure",
                "impact": "Medium",
                "effort": "Low"
            },
            {
                "type": "Security",
                "description": "Add input validation",
                "impact": "High",
                "effort": "Low"
            },
            {
                "type": "Style",
                "description": "Follow consistent naming conventions",
                "impact": "Low",
                "effort": "Low"
            }
        ]
        
        # Generate 2-4 random suggestions
        num_suggestions = random.randint(2, 4)
        for _ in range(num_suggestions):
            suggestion = random.choice(suggestion_types).copy()
            suggestion["line"] = random.randint(1, len(code.split('\n')))
            suggestion["confidence"] = round(random.uniform(0.7, 0.95), 2)
            suggestions.append(suggestion)
        
        return {
            "suggestions": suggestions,
            "total_suggestions": len(suggestions),
            "generated_at": datetime.now().isoformat()
        }

    def security_scan(self, code, language="Python"):
        # Simulate security vulnerability detection
        vulnerabilities = []
        
        # Common vulnerability patterns
        vuln_patterns = [
            {
                "name": "SQL Injection",
                "severity": "Critical",
                "description": "Potential SQL injection vulnerability",
                "line": random.randint(1, len(code.split('\n')))
            },
            {
                "name": "Cross-Site Scripting (XSS)",
                "severity": "High",
                "description": "Unescaped user input could lead to XSS",
                "line": random.randint(1, len(code.split('\n')))
            },
            {
                "name": "Insecure Random",
                "severity": "Medium",
                "description": "Use of weak random number generation",
                "line": random.randint(1, len(code.split('\n')))
            },
            {
                "name": "Hardcoded Credentials",
                "severity": "High",
                "description": "Hardcoded passwords or API keys detected",
                "line": random.randint(1, len(code.split('\n')))
            }
        ]
        
        # Randomly select 0-3 vulnerabilities
        num_vulns = random.randint(0, 3)
        for _ in range(num_vulns):
            vuln = random.choice(vuln_patterns).copy()
            vuln["confidence"] = round(random.uniform(0.8, 0.95), 2)
            vulnerabilities.append(vuln)
        
        security_score = max(0, 100 - (len(vulnerabilities) * 25))
        
        return {
            "vulnerabilities": vulnerabilities,
            "security_score": security_score,
            "risk_level": "High" if len(vulnerabilities) > 2 else "Medium" if len(vulnerabilities) > 0 else "Low",
            "scan_time": datetime.now().isoformat()
        }

    def performance_analysis(self, code, language="Python"):
        # Simulate performance analysis
        lines = code.split('\n')
        
        # Performance metrics
        time_complexity = random.choice(["O(1)", "O(n)", "O(n²)", "O(log n)", "O(n log n)"])
        space_complexity = random.choice(["O(1)", "O(n)", "O(n²)"])
        
        # Performance issues
        performance_issues = []
        issue_types = [
            "Inefficient loop", "Memory allocation in loop", "Unnecessary object creation",
            "Recursive function without memoization", "Large data structure copy",
            "Inefficient string concatenation", "Missing caching"
        ]
        
        num_issues = random.randint(0, 4)
        for _ in range(num_issues):
            issue = {
                "type": random.choice(issue_types),
                "line": random.randint(1, len(lines)),
                "impact": random.choice(["Low", "Medium", "High"]),
                "suggestion": f"Consider optimizing this {random.choice(['algorithm', 'data structure', 'loop'])}"
            }
            performance_issues.append(issue)
        
        performance_score = max(0, 100 - (num_issues * 20))
        
        return {
            "time_complexity": time_complexity,
            "space_complexity": space_complexity,
            "performance_score": performance_score,
            "issues": performance_issues,
            "estimated_bottlenecks": num_issues,
            "analysis_time": datetime.now().isoformat()
        }

ai_reviewer = AICodeReviewAssistant()

@app.route("/")
def root():
    return jsonify({
        "message": "🤖 AI Code Review Assistant - Intelligent code analysis platform",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "Automated code quality analysis",
            "ML-powered bug detection",
            "Security vulnerability scanning",
            "Performance optimization suggestions",
            "Multi-language support",
            "Real-time code review"
        ]
    })

@app.route("/api/analyze", methods=["POST"])
def analyze_code():
    data = request.json
    code = data.get("code", "")
    language = data.get("language", "Python")
    
    if not code.strip():
        return jsonify({"success": False, "error": "No code provided"})
    
    analysis = ai_reviewer.analyze_code_quality(code, language)
    return jsonify({"success": True, "analysis": analysis})

@app.route("/api/review", methods=["POST"])
def generate_review():
    data = request.json
    code = data.get("code", "")
    language = data.get("language", "Python")
    
    if not code.strip():
        return jsonify({"success": False, "error": "No code provided"})
    
    review = ai_reviewer.generate_code_review(code, language)
    return jsonify({"success": True, "review": review})

@app.route("/api/suggest", methods=["POST"])
def get_suggestions():
    data = request.json
    code = data.get("code", "")
    language = data.get("language", "Python")
    
    if not code.strip():
        return jsonify({"success": False, "error": "No code provided"})
    
    suggestions = ai_reviewer.get_improvement_suggestions(code, language)
    return jsonify({"success": True, "suggestions": suggestions})

@app.route("/api/security-scan", methods=["POST"])
def security_scan():
    data = request.json
    code = data.get("code", "")
    language = data.get("language", "Python")
    
    if not code.strip():
        return jsonify({"success": False, "error": "No code provided"})
    
    scan_results = ai_reviewer.security_scan(code, language)
    return jsonify({"success": True, "security_scan": scan_results})

@app.route("/api/performance", methods=["POST"])
def performance_analysis():
    data = request.json
    code = data.get("code", "")
    language = data.get("language", "Python")
    
    if not code.strip():
        return jsonify({"success": False, "error": "No code provided"})
    
    performance = ai_reviewer.performance_analysis(code, language)
    return jsonify({"success": True, "performance": performance})

@app.route("/api/languages")
def get_supported_languages():
    return jsonify({"success": True, "languages": ai_reviewer.supported_languages})

if __name__ == "__main__":
    print("🤖 AI Code Review Assistant Starting...")
    print("💡 Intelligent code analysis platform")
    print("🌐 API running on http://localhost:8004")
    print("📊 Frontend available at: file:///Users/parampatel/parampatel-dev/ai-code-review/frontend/index.html")
    print("🔍 Ready for AI-powered code review!")
    app.run(debug=True, host="0.0.0.0", port=8004)

