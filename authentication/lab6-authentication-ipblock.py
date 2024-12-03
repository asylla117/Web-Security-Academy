print("#list of usernames: #")
# generate usernames by printing 'carlos' twice and 'wiener' once.
for i in range(150):
    if i % 3:
        print("carlos")
    else:
        print("wiener")

print("#list of passwords: #")

# open the file in read mode ('r')
with open('passwords.txt', 'r') as file:
    contents = file.readlines()

# iterate thru file contents
i = 0
for pwd in contents:
    if i % 2:
        print(pwd.strip('\n'))
    else:
        print("peter")
        print(pwd.strip('\n'))
    i = i + 1 