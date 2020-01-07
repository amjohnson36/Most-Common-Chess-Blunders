import os

data = {}
count = 0

for filename in os.listdir("results/"):
    with open('results/{0}'.format(filename), 'r') as infile:
        for line in infile.readlines():
            l = line.split(',')
            
            if l[2] == "1\n":
            # skip blunders that were only played once to save memory
                continue
            
            blunder = l[0] + ',' + l[1]
            
            if blunder in data:
                data[blunder] += int(l[2])

            else:
                data[blunder] = int(l[2])
    count += 1
    print(str(len(data.keys())) + " " + str(count))
    print(filename + " done")


with open('Consolidated.output', 'w') as outfile:
        sorted_data = sorted(data, key=data.get, reverse=True)
        for r in sorted_data:
            outfile.write('{0},{1}\n'.format(r, data[r]))
