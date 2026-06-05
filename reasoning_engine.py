import json

class AcademicAdvisorSystem:
    def __init__(self, kb_file):
        # Load the knowledge base
        with open(kb_file, 'r') as file:
            self.knowledge_base = json.load(file)
            
    def generate_facts(self, student_data):
        """Translates raw student data into discrete facts for the reasoning engine."""
        facts = set()
        
        # GPA Facts
        if student_data.get("gpa") > 3.5:
            facts.add("GPA > 3.5")
            facts.add("GPA > 3.0") # Inherently true
        elif 3.0 <= student_data.get("gpa") <= 3.49:
            facts.add("GPA Between 3.0 and 3.49")
            facts.add("GPA > 3.0")
        elif student_data.get("gpa") < 3.0:
            facts.add("GPA < 3.0")
            
        # Attendance Facts
        if student_data.get("attendance") > 80:
            facts.add("Attendance > 80%")
        else:
            facts.add("Attendance Below 80%")
            
        # Boolean Facts
        if not student_data.get("disciplinary_cases"):
            facts.add("No Disciplinary Cases")
        else:
            facts.add("Has Disciplinary Cases")
            
        if student_data.get("completed_prerequisites"):
            facts.add("Completed Prerequisite Courses")
            
        if student_data.get("outstanding_fees"):
            facts.add("Outstanding Fees")
        else:
            facts.add("No Outstanding Fees")
            
        return facts

    def forward_chaining(self, facts):
        """Applies rules to the known facts to generate conclusions and explanations."""
        conclusions = []
        explanations = []
        
        for rule in self.knowledge_base["rules"]:
            conditions = set(rule["conditions"])
            
            # If all conditions for a rule exist in the generated facts
            if conditions.issubset(facts):
                conclusion = rule["conclusion"]
                conclusions.append(conclusion)
                
                # Explanation Facility (Task 4)
                explanation = f"✓ {conclusion} because:\n"
                for condition in conditions:
                    explanation += f"   - {condition}\n"
                explanation += f"   Therefore, the {rule['rule_name']} was activated."
                explanations.append(explanation)
                
        return conclusions, explanations

def run_test_cases():
    advisor = AcademicAdvisorSystem('knowledge_base.json')

    # Task 3: Forward Chaining Inference (3 Profiles)
    profiles = [
        {
            "name": "Profile 1: High Achiever",
            "data": {
                "gpa": 3.8, "attendance": 90, "disciplinary_cases": False,
                "completed_prerequisites": True, "outstanding_fees": False
            }
        },
        {
            "name": "Profile 2: Struggling Student",
            "data": {
                "gpa": 2.5, "attendance": 75, "disciplinary_cases": True,
                "completed_prerequisites": False, "outstanding_fees": True
            }
        },
        {
            "name": "Profile 3: Average Student (Missing Fees)",
            "data": {
                "gpa": 3.2, "attendance": 85, "disciplinary_cases": False,
                "completed_prerequisites": True, "outstanding_fees": True
            }
        }
    ]

    for profile in profiles:
        print(f"\n{'='*40}\nEvaluating: {profile['name']}\n{'='*40}")
        print("Raw Data:", profile['data'])
        
        facts = advisor.generate_facts(profile['data'])
        print("\n[Generated Facts]:")
        for fact in facts: print(f" - {fact}")
            
        conclusions, explanations = advisor.forward_chaining(facts)
        
        print("\n[Conclusions & Explanations]:")
        if not conclusions:
            print("No actionable conclusions reached.")
        for explanation in explanations:
            print(explanation)

if __name__ == "__main__":
    run_test_cases()