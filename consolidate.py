import os

data = {}
count = 0
"""
with open('Consolidated.output', 'r') as infile:
    for line in infile.readlines():
        l = line.split(',')
        blunder = l[0] + ',' + l[1]
        data[blunder] = int(l[2])
"""

for filename in os.listdir("results/"):
    with open('results/{0}'.format(filename), 'r') as infile:
        for line in infile.readlines():
            l = line.split(',')
            
            if l[2] == "1\n":
                continue
            
            blunder = l[0] + ',' + l[1]
            
            if blunder in data:
                data[blunder] += int(l[2])

            else:
                data[blunder] = int(l[2])
    count += 1
    print(str(len(data.keys())) + " " + str(count))
    print(filename + " done")




with open('test', 'w') as outfile:
        sorted_data = sorted(data, key=data.get, reverse=True)
        for r in sorted_data:
            outfile.write('{0},{1}\n'.format(r, data[r]))

