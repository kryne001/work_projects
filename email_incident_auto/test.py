with open('/Users/kyler.rynear.-nd/email_incident_auto/ending_name.txt', 'r') as file:
    file_content = file.read()

print(file_content)

with open('/Users/kyler.rynear.-nd/email_incident_auto/ending_name.txt', 'w') as file:
    file.write("BRIAN ANDERSON")

with open('/Users/kyler.rynear.-nd/email_incident_auto/ending_name.txt', 'r') as file:
    file_content = file.read()

print(file_content)