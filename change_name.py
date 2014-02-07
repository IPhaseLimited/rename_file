import csv, json, os, sys
if __name__ == "__main__":
    root_dir = sys.path[0]
else:
    root_dir = os.path.dirname(__file__)

def makeList(file_dir = 'Replacement_LookUpTable.csv'):
    '''
    create a dictinary of wardnames using the wardcode as key for easy access
    '''
    csvfile  = open(file_dir, "rb")
    reader = csv.reader(csvfile)

    rownum = 0
    csvData = []
    for row in reader:
        row_dict = {}
        # Save header row.
        if rownum == 0:
            header = row
        else:
            colnum = 0
            for col in row:
                row_dict[header[colnum].lower()] = col
                colnum += 1
            csvData.append(row_dict)
        rownum += 1

    csvfile.close()
    arr_for_json = {}
    for row in csvData:
        arr_for_json[row['wardcode']] = row['wardname']

    #file_dir = file_dir.rsplit('.', 1)
    #with open('{0}.json'.format(file_dir[0]), 'w') as jfile:
        #jfile.write(json.dumps(arr_for_json))

    return arr_for_json

#get Disctinary from CSV file
check_list = makeList()

#create a list of files from current directory
file_list = [f for f in os.listdir(root_dir) if os.path.isfile(os.path.join(root_dir, f)) ]
#loop through each file and make sure we are dealing with just PDF
for f in file_list:
    f_arr = f.rsplit('.',1)
    if f_arr[1] == 'pdf':
        name = f_arr[0].rsplit('_',1)
        #rename file with wardcode included in its name
        try:
            new_name = check_list[name[1]]
            os.rename(f, '{0}.pdf'.format(new_name))
        except KeyError:
            print 'WardCode {} not found'.format(name[1])
