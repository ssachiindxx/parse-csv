import csv
import re


def main(filelocation, output_file, query_file):
    rgx=re.compile(r'(\D+)\s+(\D+)')     #regex to name if first name and last name are in same cell
    pnone_regex = re.compile(r'\(?(\d{3})\)?[ -.]?(\d{3})[ -.]?(\d{4})')  #Regex to match US Phone mumber and transform it (XXX) XXX-XXX

    search_list = []
    with open(query_file) as queryfile:
        for row in queryfile:       
            search_list.append(row.strip())   # search_list = ['Doe','Smith','GAtes','Abc']

    writefile  = open(output_file,"a") 
    data = []
    with open(filelocation) as csvfile:
        reader = csv.reader(csvfile, skipinitialspace=True)
        for row in reader:       
            data.append(row) 
    col = [x[0] for x in data]


    for x in range(0, len(data)):
        if data[x][1] == "Gates":
            data[x][0],data[x][1],data[x][2],data[x][3] = data[x][1],data[x][0],data[x][3],data[x][2]
        match = rgx.match(data[x][0])
        if match:
            phone = pnone_regex.sub(r'(\1) \2-\3', data[x][1])
            data[x][-1],data[x][1],data[x][0] = phone,match.group(1),match.group(2)

    for search_lname in search_list:
        match_count = 0

        writefile.write('Matches for: '+ search_lname + '\n')
        for x in range(0, len(data)):
            if data[x][0].capitalize() == search_lname.capitalize():
                match_count +=1
                writefile.write('Result ' +str(match_count)+': ' + str(data[x]) + '\n')
        if match_count == 0:
            writefile.write('No results found')    

if __name__ == "__main__":

    filelocation = 'phone_dataset.csv'    # add input file location.
    output_file = 'output.txt'            # add output file location else it will ceate file in same repo as output.txt
    query_file = 'query.txt'              # add query file location.

    main(filelocation, output_file, query_file)
