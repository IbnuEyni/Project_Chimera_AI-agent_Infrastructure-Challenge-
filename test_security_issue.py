# Test file with intentional security issues for CodeRabbit to catch

def unsafe_query(user_input):
    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    return query

def hardcoded_secret():
    # Hardcoded API key
    api_key = "sk-1234567890abcdef"
    return api_key

def no_input_validation(prompt):
    # No prompt injection protection
    return f"System: {prompt}"
