import csv
import numpy as np
import os

in_folder = "csv"
out_folder = "csv_fixed"

def process_csv(file_name):
  line_count = 0
  data = []
  with open(in_folder+"/"+file_name+".csv", encoding="utf8", errors='ignore') as f:
    csv_reader = csv.reader(f, delimiter=',')
    
    row_number = 0

    area_path_index = 0
    iteration_path_index = 0
    priority_index = 0

    authorized_date_index = 0
    node_name_index = 0
    team_project_index = 0
    watermark_index = 0
    effort_index = 0
    reason_index = 0
    changed_date_index = 0
    created_date_index = 0
    closed_date_index = 0
    state_change_date_index = 0
    activated_date_index = 0
    assigned_to_index = 0
    authorized_as_index = 0
    created_by_index = 0
    changed_by_index = 0
    closed_by_index = 0
    accepted_by_index = 0
    reviewed_by_index = 0

    for row in csv_reader:
      if line_count == 0:
        for r in row:
          if r == "Area Path":
            area_path_index = row_number
          if r == "Iteration Path":
            iteration_path_index = row_number
          if r == "Priority":
            priority_index = row_number
          if r == "Authorized Date":
            authorized_date_index = row_number
          if r == "Node Name":
            node_name_index = row_number
          if r == "Team Project":
            team_project_index = row_number
          if r == "Watermark":
            watermark_index = row_number
          if r == "Effort":
            effort_index = row_number

          if r == "Reason":
            reason_index = row_number
          if r == "Changed Date":
            changed_date_index = row_number
          if r == "Created Date":
            created_date_index = row_number
          if r == "Closed Date":
            closed_date_index = row_number
          if r == "State Change Date":
            state_change_date_index = row_number
          if r == "Activated Date":
            activated_date_index = row_number
          if r == "Assigned To":
            assigned_to_index = row_number
          if r == "Authorized As":
            authorized_as_index = row_number
          if r == "Created By":
            created_by_index = row_number
          if r == "Changed By":
            changed_by_index = row_number
          if r == "Closed By":
            closed_by_index = row_number
          if r == "Accepted By":
            accepted_by_index = row_number
          if r == "Reviewed By":
            reviewed_by_index = row_number

          row_number += 1;
          
      else:
        row[0] = ""
        row[area_path_index] = "Archived.OldTfsServer\\"+file_name
        row[iteration_path_index] = "Archived.OldTfsServer"
        row[priority_index] = "2"

      line_count += 1

      array = np.array(row)
      
      columns_remove = [
        authorized_date_index,
        node_name_index,
        team_project_index,
        watermark_index,
        effort_index,
        reason_index,
        changed_date_index,
        created_date_index,
        closed_date_index,
        state_change_date_index,
        activated_date_index,
        assigned_to_index,
        authorized_as_index,
        created_by_index,
        changed_by_index,
        closed_by_index,
        accepted_by_index,
        reviewed_by_index,
      ]

      columns_remove_sort = np.sort(columns_remove)[::-1]

      print(columns_remove_sort)

      for i in columns_remove_sort:
        array = np.delete(array, i)

      data.append(array)

  with open(out_folder+"/"+file_name+"_fixed.csv", 'w', encoding='UTF8') as f:
      writer = csv.writer(f)
      writer.writerows(data)
  
# process_csv("AdditionIT")


in_files = os.listdir(in_folder)
num_file = 0;
for f in in_files:
  num_file += 1
  print(num_file)
  name = f.split(".")[0]
  print(name)
  if name != '':
    process_csv(f.split(".")[0])
  


