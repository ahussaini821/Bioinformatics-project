import pandas as pd

df = pd.read_csv("kinase target final2.csv")
html_start = '<html><head><title>Kinview</title><script type="text/javascript" src="https://www.ncbi.nlm.nih.gov/projects/sviewer/js/sviewer.js"></script></head><body><div id="Kinview" class="SeqViewerApp" data-autoload><a href="?embedded=true&amp;appname=testapp1&amp;id=NC_0000'
html_end = '"></a></div></body></html>'
format_start = '&mk='
format_end = '|008000'

for count in range(1,25):
    html_start = '<html><head><title>Kinview</title><script type="text/javascript" src="https://www.ncbi.nlm.nih.gov/projects/sviewer/js/sviewer.js"></script></head><body><div id="Kinview" class="SeqViewerApp" data-autoload><a href="?embedded=true&amp;appname=testapp1&amp;id=NC_0000'
    file_name = 'Chrom' + str(count) +'.html'
    if count == 23:
        output = open("ChromX.html", "w")
    elif count == 24:
        output = open("ChromY.html", "w")
    else:
        output = open(file_name, "w")
    final_html = ""
    curr_url = ''
    curr_items = []
    if count > 10:
        html_start += str(count)
    else:
        html_start += str(0) + str(count)
    print(count)
    for index, row in df.iterrows():
        curr_marker = '|' + row["Target accession"] + ' ' + row["Location"]
        if count == 23:

            if row['Chromosome'] == 'X':
                html_start = '<html><head><title>Kinview</title><script type="text/javascript" src="https://www.ncbi.nlm.nih.gov/projects/sviewer/js/sviewer.js"></script></head><body><div id="Kinview" class="SeqViewerApp" data-autoload><a href="?embedded=true&amp;appname=testapp1&amp;id=NC_000023.11'
                start_pos = row["Start"]
                end_pos = row["End"]
                full_pos = str(start_pos) + ':' + str(end_pos)
                curr_url += format_start + full_pos + curr_marker + format_end
        elif count == 24:
            if row['Chromosome'] == 'Y':
                html_start = '<html><head><title>Kinview</title><script type="text/javascript" src="https://www.ncbi.nlm.nih.gov/projects/sviewer/js/sviewer.js"></script></head><body><div id="Kinview" class="SeqViewerApp" data-autoload><a href="?embedded=true&amp;appname=testapp1&amp;id=NC_000024.10'
                start_pos = row["Start"]
                end_pos = row["End"]
                full_pos = str(start_pos) + ':' + str(end_pos)
                curr_url += format_start + full_pos + curr_marker + format_end
        else:
            if row['Chromosome'] == str(count):

                start_pos = row["Start"]
                end_pos = row["End"]
                full_pos = str(start_pos) + ':' + str(end_pos)
                curr_url += format_start + full_pos + curr_marker + format_end
    final_html = html_start + curr_url + html_end
    output.write(final_html)
    output.close()
