from pyecharts.charts import Bar

from chart import TxtFileReader, jsonFileReader

txtFile = TxtFileReader("testData.txt")
jsonFile = jsonFileReader("testData.json")

txt_record_list = txtFile.readData()
for record in txt_record_list:
    print(record.name, record.age, record.gender, record.occupation)

json_record_list = jsonFile.readData()
for record in json_record_list:
    print(record.name, record.age, record.gender, record.occupation)

for record in json_record_list:
    txt_record_list.append(record)
for record in txt_record_list:
    print(record.name, record.age, record.gender, record.occupation)

bar = Bar()
bar.add_xaxis(["xx", "xx", "xx", "xx", "xx", "xx"])
bar.add_yaxis("Series A", [record.age for record in txt_record_list])
bar.set_global_opts(title_opts={"text": "Test Bar Chart"})
bar.render("testResult.html")

if __name__ == "__main__":
    pass
