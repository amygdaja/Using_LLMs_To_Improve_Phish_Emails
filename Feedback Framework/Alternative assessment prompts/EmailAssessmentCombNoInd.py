import json

# -------------------------------------------------------------
# Persuasion
# -------------------------------------------------------------

def evaluate_persuasion(email, pipe):
    combined = {
        "email": email
    }

    system_instructions = """
                    You are an expert in persuasion psychology. Your task is to identify the persuasion principles used in the attached email.
                    
                    Persuasion principles
                    - Reciprocity: The email offers something and asks for a favor, click or confirmation in return 
                    - Scarcity: The email creates urgency by implying limited time, quantity or opportunity 
                    - Authority: The email claims or displays credibility through a recognized institution, title or role 
                    - Commitment/Consistency: The email references prior behavior of choices to push further action 
                    - Liking: The email uses familiarity, flattery or personalization to build trust or rapport 
                    - Social proof: The email references other people's participation or endorsement 

                    Mention how the persuasion principle is used in the explanation. If a principle is not present in the email, put "Not present" in the explanation.

                    Respond STRICTLY in JSON ONLY, in this exact format (no extra text before or after):
                    {
                        "Reciprocity": {"Explanation": "explanation"},
                        "Scarcity": {"Explanation": "explanation"},
                        "Authority": {"Explanation": "explanation"},
                        "Commitment/Consistency": {"Explanation": "explanation"},
                        "Liking": {"Explanation": "explanation"},
                        "Social proof": {"Explanation": "explanation"}
                    }
                    Do *NOT* output anything other than this JSON."""

    messages = [
            {
                "role": "user",
                "content": system_instructions + "\n\n" + json.dumps(combined, indent=2)
            }
        ]
    
    output = pipe(text_inputs=messages, max_new_tokens=400)

    return output[0]["generated_text"][-1]["content"]

# -------------------------------------------------------------
# Phishing (combined)
# -------------------------------------------------------------

def evaluate_phishing_combined(email, persuasion_principles, pipe):
    combined = {
        "email": email,
        "persuasion principles": persuasion_principles
    }

    system_instructions = """
                    You are an email security analyst. Your task is to determine whether the attached email is phishing or benign, on two dimensions:
                    Phishing Characteristics and Phishing Persuasion.
                 
                    For Phishing Characteristics, determine whether the email is phishing or not based on common phishing indicators.
                 
                    Task for Phishing Persuasion:
                    1. Review the attached email.
                    2. Review the attached list of persuasion principles that have already been identified. Do NOT identify any additional persuasion principles.
                    3. Examine the sender’s claimed purpose as stated or implied in the email.
                    4. Assess whether the identified persuasion principles are appropriate for a legitimate email with that purpose.
                    For Phishing Persuasion, an email is considered phishing if the persuasion principles used in the email are inconsistent with the sender’s claimed purpose and appear manipulative, deceptive, or inappropriate for legitimate communication.
                 
                    For each dimension, return exactly one of the following labels:
                    - "Phishing Email"
                    - "Benign Email"
                    Show your reasoning in the justification.

                    Respond STRICTLY in valid JSON only, in this exact format (no extra text before or after):
                        {
                            "Phishing Characteristics": {"Assessment": "<Phishing Email or Benign Email>", "Justification": "<Justification on the assessment>"},
                            "Phishing Persuasion": {"Assessment": "<Phishing Email or Benign Email>", "Justification": "<Justification on the assessment>"}
                            }
                    
                    Rules:
                    - The justification must be a maximum of 5 sentences per dimension.
                    - do NOT use bullet points, markdown, line breaks, or quotation marks within the justification.
                    - Do NOT add any text outside the JSON.
                    """
    messages = [
            {
                "role": "user",
                "content": system_instructions + "\n\n" + json.dumps(combined, indent=2)
            }
        ]

    output = pipe(text_inputs=messages, max_new_tokens=2000)

    return output[0]["generated_text"][-1]["content"]


# -------------------------------------------------------------
# Sophistication (combined)
# -------------------------------------------------------------

def evaluate_sophistication_combined(email, user_profile, knowledge_base, persuasion_principles, pipe):
    combined = {
        "email": email,
        "user profile": user_profile,
        "knowledge base": knowledge_base,
        "persuasion principles": persuasion_principles
    }

    system_instructions = """
                    You are a professional email communication analyst. Your task is to evaluate the sophistication of the attached email on four dimensions: 
                    Email Etiquette, Email Content, General Personalization, and Personalization of Persuasion Principles.

                    Email Etiquette refers to the structure and writing quality of the email.
                    - An email is Sufficient if its structure and writing quality would be considered acceptable in a typical workplace. Otherwise, it is Insufficient.
                 
                    Email Content refers to the accuracy, relevance and clarity of the email.
                    - An email is Sufficient if a recipient could clearly understand the message without needing additional clarification. Otherwise, it is Insufficient.

                    General Personalization refers to how appropriately personalized an email is, according to the attached user profile. 
                    - Task for assessing General Personalization:
                        1. Review the attached email.
                        2. Review the attached user profile.
                        3. Evaluate how well the email is personalized for the recipient in the user profile.
                    - An email is Sufficient if it demonstrates appropriate personalization for the recipient in the attached profile. Otherwise, it is Insufficient.
                 
                    Personlization of Persuasion Principles refers to whether the persuasion techniques used in an email are appropriate for the attached recipient's profile.
                    - Task for Personalization of Persuasion Principles:
                        1. Review the attached email.
                        2. Review the attached list of persuasion principles that have already been identified. Do NOT identify any additional persuasion principles.
                        3. Review the attached knowledge base which contains information on what persuasion techniques are effective for specific recipients (e.g., based on job role and nationality).
                        4. Review the attached profile that belongs to the recipient.
                        5. Assess the alignment of the chosen persuasion principles with the knowledge base's recommendations.
                    - An email is Sufficient if the identified persuasion techniques are appropriate for the recipient profile and context. Otherwise, it is Insufficient.                 
                 
                    For each dimension, return exactly one of the following labels:
                    - "Sufficient"
                    - "Insufficient"
                    Show your reasoning in the justification.

                    Respond STRICTLY in valid JSON only, in this exact format (no extra text before or after):
                       {
                          "Email Etiquette": {"Assessment": "<Sufficient or Insufficient>", "Justification": "<Justification on the assessment>"},
                          "Email Content": {"Assessment": "<Sufficient or Insufficient>", "Justification": "<Justification on the assessment>"},
                          "General Personalization": {"Assessment": "<Sufficient or Insufficient>", "Justification": "<Justification on the assessment>"},
                          "Personalization of Persuasion Principles": {"Assessment": "<Sufficient or Insufficient>", "Justification": "<Justification on the assessment>"}
                        }
                    Rules:
                    - The justification must be a maximum of 5 sentences per dimension.
                    - do NOT use bullet points, markdown, line breaks, or quotation marks within the justification.
                    - Do NOT add any text outside the JSON."""
    
    messages = [
            {
                "role": "user",
                "content": system_instructions + "\n\n" + json.dumps(combined, indent=2)
            }
        ]

    output = pipe(text_inputs=messages, max_new_tokens=2000)

    return output[0]["generated_text"][-1]["content"]

# -------------------------------------------------------------
# Phishing and Sophistication (combined)
# -------------------------------------------------------------

def evaluate_all_combined(email, user_profile, knowledge_base, persuasion_principles, pipe):
    combined = {
        "email": email,
        "user profile": user_profile,
        "knowledge base": knowledge_base,
        "persuasion principles": persuasion_principles
    }

    system_instructions = """
                    You are a professional email communication analyst. You are tasked with evaluating the attached email on six dimensions: 
                    Phishing Characteristics, Malicious use of Persuasion Principles, Email Etiquette, Email Content, General Personalization, and Personalization of Persuasion Principles.
                            
                    For Phishing Characteristics, determine whether the email is phishing or not based on common phishing indicators.
                 
                    Task for Phishing Persuasion:
                    1. Review the attached email.
                    2. Review the attached list of persuasion principles that have already been identified. Do NOT identify any additional persuasion principles.
                    3. Examine the sender’s claimed purpose as stated or implied in the email.
                    4. Assess whether the identified persuasion principles are appropriate for a legitimate email with that purpose.
                    For Phishing Persuasion, an email is considered phishing if the persuasion principles used in the email are inconsistent with the sender’s claimed purpose and appear manipulative, deceptive, or inappropriate for legitimate communication.
                 
                    For each dimension, return exactly one of the following labels:
                    - "Phishing Email"
                    - "Benign Email"
                    Show your reasoning in the justification.
                 
                    Email Etiquette refers to the structure and writing quality of the email.
                    - An email is Sufficient if its structure and writing quality would be considered acceptable in a typical workplace. Otherwise, it is Insufficient.
                 
                    Email Content refers to the accuracy, relevance and clarity of the email.
                    - An email is Sufficient if a recipient could clearly understand the message without needing additional clarification. Otherwise, it is Insufficient.

                    General Personalization refers to how appropriately personalized an email is, according to the attached user profile. 
                    - Task for assessing General Personalization:
                        1. Review the attached email.
                        2. Review the attached user profile.
                        3. Evaluate how well the email is personalized for the recipient in the user profile.
                    - An email is Sufficient if it demonstrates appropriate personalization for the recipient in the attached profile. Otherwise, it is Insufficient.
                 
                    Personlization of Persuasion Principles refers to whether the persuasion techniques used in an email are appropriate for the attached recipient's profile.
                    - Task for Personalization of Persuasion Principles:
                        1. Review the attached email.
                        2. Review the attached list of persuasion principles that have already been identified. Do NOT identify any additional persuasion principles.
                        3. Review the attached knowledge base which contains information on what persuasion techniques are effective for specific recipients (e.g., based on job role and nationality).
                        4. Review the attached profile that belongs to the recipient.
                        5. Assess the alignment of the chosen persuasion principles with the knowledge base's recommendations.
                    - An email is Sufficient if the identified persuasion techniques are appropriate for the recipient profile and context. Otherwise, it is Insufficient.                 
                 
                    For each dimension, return exactly one of the following labels:
                    - "Sufficient"
                    - "Insufficient"
                    Show your reasoning in the justification.

                    Respond STRICTLY in valid JSON only, in this exact format (no extra text before or after):
                       {
                          "Phishing Characteristics": {"Assessment": "<Phishing Email or Benign Email>", "Justification": "<Justification on the assessment>"},
                          "Phishing Persuasion": {"Assessment": "<Phishing Email or Benign Email>", "Justification": "<Justification on the assessment>"},
                          "Email Etiquette": {"Assessment": "<Sufficient or Insufficient>", "Justification": "<Justification on the assessment>"},
                          "Email Content": {"Assessment": "<Sufficient or Insufficient>", "Justification": "<Justification on the assessment>"},
                          "General Personalization": {"Assessment": "<Sufficient or Insufficient>", "Justification": "<Justification on the assessment>"},
                          "Personalization of Persuasion Principles": {"Assessment": "<Sufficient or Insufficient>", "Justification": "<Justification on the assessment>"}
                        }
                    Rules:
                    - The justification must be a maximum of 5 sentences per dimension.
                    - do NOT use bullet points, markdown, line breaks, or quotation marks within the justification.
                    - Do NOT add any text outside the JSON."""
    
    messages = [
            {
                "role": "user",
                "content": system_instructions + "\n\n" + json.dumps(combined, indent=2)
            }
        ]

    output = pipe(text_inputs=messages, max_new_tokens=3000)

    return output[0]["generated_text"][-1]["content"]