

# def build_dev_prompt(language, intent, user_input):
#     return f"""
#         You are a senior software engineer.

#         Language: {language}
#         User intent: {intent}

#         User input:
#         {user_input}

#         Instructions:
#         - Explain the issue clearly
#         - Provide corrected or improved code if applicable
#         - Share best practices
#         - Keep the response concise and developer-friendly

#         Respond in this format:
#         Explanation:
#         <text>

#         Code:
#         <code if any>

#         Tips:
#         - tip 1
#         - tip 2
#     """
    
def build_dev_prompt(language, intent, user_input):
    return user_input