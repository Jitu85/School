with open('.env', 'r') as f:
    lines = f.readlines()

with open('.env', 'w') as f:
    for line in lines:
        if line.startswith('DB_PASSWORD='):
            f.write('DB_PASSWORD=jitu\n')
        else:
            f.write(line)