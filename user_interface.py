# inference_engine.py

class InferenceEngine:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def evaluate_hemoglobin_state(self, gender, hemoglobin_level):
        concept_name = f"Hemoglobin_level_{gender.lower()}"
        for state, range_ in self.kb.get_concept(concept_name).items():
            if "-" in range_:
                lower, upper = map(float, range_.split("-"))
                if lower <= float(hemoglobin_level) <= upper:
                    return state
            elif range_.endswith("+") and float(hemoglobin_level) >= float(range_[:-1]):
                return state
        return "Unknown Hemoglobin State"

    def evaluate_toxicity(self, fever, chills, skin_look, allergic_state):
        concept = self.kb.get_concept("Systemic_Toxicity")
        grades = [
            self.evaluate_parameter(concept["Fever"], fever),
            self.evaluate_parameter(concept["Chills"], chills),
            self.evaluate_parameter(concept["Skin-look"], skin_look),
            self.evaluate_parameter(concept["Allergic-state"], allergic_state),
        ]
        return max(grades, key=lambda x: ["Grade I", "Grade II", "Grade III", "Grade IV"].index(x))

    def evaluate_parameter(self, parameter_rules, value):
        for range_key, grade in parameter_rules.items():
            if range_key.endswith("+") and float(value) >= float(range_key[:-1]):
                return grade
            elif "-" in range_key:
                lower, upper = map(float, range_key.split("-"))
                if lower <= float(value) <= upper:
                    return grade
            elif value == range_key:
                return grade
        return "Unknown Grade"

    def get_treatment_recommendation(self, gender, hemoglobin_state, hematological_state, toxicity_grade):
        concept_name = f"Treatment_Recommendations_{gender.capitalize()}"
        key = (
            ("Hemoglobin-state", hemoglobin_state),
            ("Hematological-state", hematological_state),
            ("Systemic-Toxicity", toxicity_grade),
        )
        return self.kb.get_concept(concept_name).get(key, "No recommendation found.")


# Example usage:
if __name__ == "__main__":
    from knowledge_base import KnowledgeBase

    # Create a knowledge base instance and add concepts (you would load your existing knowledge here)
    kb = KnowledgeBase()
    # (Add your concepts here, as shown in previous examples)

    # Initialize the inference engine with the knowledge base
    engine = InferenceEngine(kb)

    # Example evaluation
    hemoglobin_state = engine.evaluate_hemoglobin_state(gender="male", hemoglobin_level=15)
    toxicity_grade = engine.evaluate_toxicity(fever=39, chills="Shaking", skin_look="Erythema", allergic_state="Edema")
    treatment = engine.get_treatment_recommendation("male", hemoglobin_state, "Normal", toxicity_grade)

    print(f"Hemoglobin State: {hemoglobin_state}")
    print(f"Toxicity Grade: {toxicity_grade}")
    print(f"Treatment Recommendation: {treatment}")
