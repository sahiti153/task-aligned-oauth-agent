from agent.tools import send_email, read_emails, search_emails

# Test 1: Send a test email TO your test account (from itself)
print("📤 Testing send_email...")
result = send_email.invoke({
    "to": "oauthagenttest@gmail.com",  # replace with your test Gmail
    "subject": "Test Email 1",
    "body": "This is a test email to verify the Gmail agent tools are working."
})
print(result)

# Test 2: Read emails
print("\n📥 Testing read_emails...")
result = read_emails.invoke({"max_results": 3})
print(result)

# Test 3: Search emails
print("\n🔍 Testing search_emails...")
result = search_emails.invoke({"query": "subject:Test"})
print(result)