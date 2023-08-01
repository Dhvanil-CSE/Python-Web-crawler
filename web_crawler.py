import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import argparse
import warnings
import os
warnings.filterwarnings("ignore")

# Specify the file path
file_path = "pyplot.png"
file_patht ='pyplotsize.png'
# Check if the file exists
if os.path.exists(file_path) and os.path.isfile(file_path):
    # Remove the file
    os.remove(file_path)
if os.path.exists(file_patht) and os.path.isfile(file_patht):
    # Remove the file
    os.remove(file_patht)

#argparse allows us to give input in terminal

parser = argparse.ArgumentParser(description='Web Crawler')
parser.add_argument('-u', '--url', required=True,type=str, help='URL of the website to crawl')
parser.add_argument('-t', '--threshold', type=int, help='Threshold (depth of recursion)',required=False)
parser.add_argument('-o', '--output',type=str, help='Output file',required=False)
parser.add_argument('-f', '--fsi',type=str, help='file size',required=False)
args = parser.parse_args()

#for getting the size of each link
def fsize(url):
  try:
      response=requests.head(url)
      if 'Content-Length' in response.headers:
        size=int(response.headers['Content-Length'])
        return size
      else:
        return None
  except:
    pass

page_list=[]              #stores the link of each page
list_new=[]               #final list of internal sites
ex_list=[]                #final list of external sites
sizel=[0,0,0,0,0,0]       #size list of internal site
sizee=[0,0,0,0,0,0]       #size list of external site
def scrape(site,threshold,level_list):
    try:
      if threshold > 0:
        level_list=[]                   #list for each level of recursion
        r=requests.get(site)            #send request to receive data from site
        s = BeautifulSoup(r.text,"lxml")   #
        href_tags = s.find_all(href=True)   #
        src_tags=s.find_all(src=True)       #
        for tag in href_tags:                 #
          href_value = tag['href']              #
          if not href_value.startswith("http"):   #
            if not href_value.startswith("/"):      #
              href_value=site+"/"+href_value        #
            elif href_value.startswith('#'):        #
              continue                              #
            elif href_value.startswith("//"):       #           
              href_value="http:"+href_value         #    
            else:                                   ##
              href_value=site+href_value              ###
          level_list.append(href_value)                 #######     This block is for recursing and getting links from the site and appending to list
        for tag in src_tags:                          ###
          src_value=tag['src']                      ##
          if not src_value.startswith("http"):      #
            if not src_value.startswith("/"):       #
              src_value=site+"/"+src_value          #
            elif src_value.startswith('#'):         #
              continue                              #
            elif src_value.startswith('//'):        #
              src_value="http:"+src_value           #
            else:                                  #
              src_value=site+src_value             #
          level_list.append(src_value)           #
        buf=[]                                  #
        for i in level_list:                    #    
            list_new.append(i)                #
            scrape(i,threshold-1,buf)       #
      else:                              #
        return                          #


    except Exception as e:
      print("An error occurred:", str(e))

#converting arguments to variables
site=args.url # website to be scrape
threshold=args.threshold
output_file=args.output
if threshold <= 0:
  raise ValueError("Please enter a positive integer with -t tag")
# calling function
count=0
print("Finding links of different types.....")
scrape(site,threshold,page_list)
list_new=set(list_new)
list_new=list(list_new) #removing repeated links
for i in list_new:
   count=count+1
   print(count)
   if i.startswith(site)==False:
     ex_list.append(i)
     list_new.remove(i)
#print(len(list_new))
ex_list=set(ex_list)
ex_list=list(ex_list)
newdic={"inter":{"html":[],"css":[],"js":[],"jpg":[],"png":[],"others":[]},"ext":{"html":[],"css":[],"js":[],"jpg":[],"png":[],"others":[]}}
for link in list_new:
  if ".html" in link or ".htm" in link:
    newdic["inter"]["html"].append(link)
  elif ".css" in link:
    newdic["inter"]["css"].append(link)
  elif ".js" in link:
    newdic["inter"]["js"].append(link)
  elif ".jpg" in link or ".jpeg" in link:
    newdic["inter"]["jpg"].append(link)
  elif ".png" in link:
    newdic["inter"]["png"].append(link)
  else:
    newdic["inter"]["others"].append(link)


#condition for file size yes and output yes

if args.output!=None and (args.fsi=="Yes" or args.fsi=="yes" or args.fsi=="Y" or args.fsi=="y"):
  with open(args.output, "w") as file:

    file.write("Internal sites:->\n")
    file.write(f"Total : {len(list_new)}\n")
    file.write(f"HTML : {len(newdic['inter']['html'])}\n")
    for i in newdic["inter"]["html"]:
      file.write(f"{i} : {fsize(i)}\n")
      if fsize(i)!=None:
        sizel[0]=sizel[0]+fsize(i)
    file.write(f"CSS : {len(newdic['inter']['css'])}\n")
    for i in newdic["inter"]["css"]:
      file.write(f"{i} : {fsize(i)}\n"
      )
      if fsize(i)!=None:
        sizel[1]=sizel[1]+fsize(i)
    file.write(f"JS : {len(newdic['inter']['js'])}\n")
    for i in newdic["inter"]["js"]:
      file.write(f"{i} : {fsize(i)}\n")
      if fsize(i)!=None:
        sizel[2]=sizel[2]+fsize(i)
    file.write(f"JPG : {len(newdic['inter']['jpg'])}\n")
    for i in newdic["inter"]["jpg"]:
      file.write(f"{i} : {fsize(i)}\n")
      if fsize(i)!=None:
        sizel[3]=sizel[3]+fsize(i)
    file.write(f"png : {len(newdic['inter']['png'])}\n")
    for i in newdic["inter"]["png"]:
      file.write(f"{i} : {fsize(i)}\n")
      if fsize(i)!=None:
        sizel[4]=sizel[4]+fsize(i)
    file.write(f"Others : {len(newdic['inter']['others'])}\n")
    for i in newdic["inter"]["others"]:
      file.write(f"{i} : {fsize(i)}\n")
      if fsize(i)!=None:
        sizel[5]=sizel[5]+fsize(i)
    nlinks=[len(newdic["inter"]["html"]),len(newdic["inter"]["css"]),len(newdic["inter"]["js"]),len(newdic["inter"]["jpg"]),len(newdic["inter"]["png"]),len(newdic["inter"]["others"])]

    for link in ex_list:
      if ".html" in link or ".htm" in link:
        newdic["ext"]["html"].append(link)
      elif ".css" in link:
        newdic["ext"]["css"].append(link)
      elif ".js" in link:
        newdic["ext"]["js"].append(link)
      elif ".jpg" in link or ".jpeg" in link:
        newdic["ext"]["jpg"].append(link)
      elif ".png" in link:
        newdic["ext"]["png"].append(link)
      else:
        newdic["ext"]["others"].append(link)
    file.write(f"External sites:->\n")
    file.write(f"Total : {len(ex_list)}\n")
    file.write(f"HTML : {len(newdic['ext']['html'])}\n")
    for i in newdic["ext"]["html"]:
      file.write(f"{i} : {fsize(i)}\n")
      if fsize(i)!=None:
        sizee[0]=sizee[0]+fsize(i)
    file.write(f"CSS : {len(newdic['ext']['css'])}\n")
    for i in newdic["ext"]["css"]:
      file.write(f"{i} : {fsize(i)}\n")
      if fsize(i)!=None:
        sizee[1]=sizee[1]+fsize(i)
    file.write(f"JS : {len(newdic['ext']['js'])}\n")
    for i in newdic["ext"]["js"]:
      file.write(f"{i} : {fsize(i)}\n")
      if fsize(i)!=None:
        sizee[2]=sizee[2]+fsize(i)
    file.write(f"JPG : {len(newdic['ext']['jpg'])}\n")
    for i in newdic["ext"]["jpg"]:
      file.write(f"{i} : {fsize(i)}\n")
      if fsize(i)!=None:
        sizee[3]=sizee[3]+fsize(i)
    file.write(f"png : {len(newdic['ext']['png'])}\n")
    for i in newdic["ext"]["png"]:
      file.write(f"{i} : {fsize(i)}\n")
      if fsize(i)!=None:
        sizee[4]=sizee[4]+fsize(i)
    file.write(f"Others : {len(newdic['ext']['others'])}\n")
    for i in newdic["ext"]["others"]:
      file.write(f"{i} : {fsize(i)}\n")
      print(1)
      if fsize(i)!=None:
        sizee[5]=sizee[5]+fsize(i)

#condition for no output and file size yes

if args.output==None and (args.fsi=="Yes" or args.fsi=="yes" or args.fsi=="Y" or args.fsi=="y"):
  print("Internal sites:->\n")
  print(f"Total : {len(list_new)}\n")
  print(f"HTML : {len(newdic['inter']['html'])}\n")
  for i in newdic["inter"]["html"]:
    print(f"{i} : {fsize(i)}\n")
    if fsize(i)!=None:
      sizel[0]=sizel[0]+fsize(i)
  print(f"CSS : {len(newdic['inter']['css'])}\n")
  for i in newdic["inter"]["css"]:
    print(f"{i} : {fsize(i)}\n"
    )
    if fsize(i)!=None:
      sizel[1]=sizel[1]+fsize(i)
  print(f"JS : {len(newdic['inter']['js'])}\n")
  for i in newdic["inter"]["js"]:
    print(f"{i} : {fsize(i)}\n")
    if fsize(i)!=None:
      sizel[2]=sizel[2]+fsize(i)
  print(f"JPG : {len(newdic['inter']['jpg'])}\n")
  for i in newdic["inter"]["jpg"]:
    print(f"{i} : {fsize(i)}\n")
    if fsize(i)!=None:
      sizel[3]=sizel[3]+fsize(i)
  print(f"png : {len(newdic['inter']['png'])}\n")
  for i in newdic["inter"]["png"]:
    print(f"{i} : {fsize(i)}\n")
    if fsize(i)!=None:
      sizel[4]=sizel[4]+fsize(i)
  print(f"Others : {len(newdic['inter']['others'])}\n")
  for i in newdic["inter"]["others"]:
    print(f"{i} : {fsize(i)}\n")
    if fsize(i)!=None:
      sizel[5]=sizel[5]+fsize(i)
  nlinks=[len(newdic["inter"]["html"]),len(newdic["inter"]["css"]),len(newdic["inter"]["js"]),len(newdic["inter"]["jpg"]),len(newdic["inter"]["png"]),len(newdic["inter"]["others"])]
  for link in ex_list:
    if ".html" in link or ".htm" in link:
      newdic["ext"]["html"].append(link)
    elif ".css" in link:
      newdic["ext"]["css"].append(link)
    elif ".js" in link:
      newdic["ext"]["js"].append(link)
    elif ".jpg" in link or ".jpeg" in link:
      newdic["ext"]["jpg"].append(link)
    elif ".png" in link:
      newdic["ext"]["png"].append(link)
    else:
      newdic["ext"]["others"].append(link)
  print(f"External sites:->\n")
  print(f"Total : {len(ex_list)}\n")
  print(f"HTML : {len(newdic['ext']['html'])}\n")
  for i in newdic["ext"]["html"]:
    print(f"{i} : {fsize(i)}\n")
    if fsize(i)!=None:
      sizee[0]=sizee[0]+fsize(i)
  print(f"CSS : {len(newdic['ext']['css'])}\n")
  for i in newdic["ext"]["css"]:
    print(f"{i} : {fsize(i)}\n")
    if fsize(i)!=None:
      sizee[1]=sizee[1]+fsize(i)
  print(f"JS : {len(newdic['ext']['js'])}\n")
  for i in newdic["ext"]["js"]:
    print(f"{i} : {fsize(i)}\n")
    if fsize(i)!=None:
      sizee[2]=sizee[2]+fsize(i)
  print(f"JPG : {len(newdic['ext']['jpg'])}\n")
  for i in newdic["ext"]["jpg"]:
    print(f"{i} : {fsize(i)}\n")
    if fsize(i)!=None:
      sizee[3]=sizee[3]+fsize(i)
  print(f"png : {len(newdic['ext']['png'])}\n")
  for i in newdic["ext"]["png"]:
    print(f"{i} : {fsize(i)}\n")
    if fsize(i)!=None:
      sizee[4]=sizee[4]+fsize(i)
  print(f"Others : {len(newdic['ext']['others'])}\n")
  for i in newdic["ext"]["others"]:
    print(f"{i} : {fsize(i)}\n")
    if fsize(i)!=None:
      sizee[5]=sizee[5]+fsize(i)

#no output given and no file size

if args.output==None and not (args.fsi=="Yes" or args.fsi=="yes" or args.fsi=="Y" or args.fsi=="y"):
  print("Internal sites:->\n")
  print(f"Total : {len(list_new)}\n")
  print(f"HTML : {len(newdic['inter']['html'])}\n")
  for i in newdic["inter"]["html"]:
    print(f"{i}\n") 
  print(f"CSS : {len(newdic['inter']['css'])}\n")
  for i in newdic["inter"]["css"]:
    print(f"{i}\n"
    )
  print(f"JS : {len(newdic['inter']['js'])}\n")
  for i in newdic["inter"]["js"]:
    print(f"{i}\n")
  print(f"JPG : {len(newdic['inter']['jpg'])}\n")
  for i in newdic["inter"]["jpg"]:
    print(f"{i}\n")
  print(f"png : {len(newdic['inter']['png'])}\n")
  for i in newdic["inter"]["png"]:
    print(f"{i}\n")
  print(f"Others : {len(newdic['inter']['others'])}\n")
  for i in newdic["inter"]["others"]:
    print(f"{i}\n")
  
  nlinks=[len(newdic["inter"]["html"]),len(newdic["inter"]["css"]),len(newdic["inter"]["js"]),len(newdic["inter"]["jpg"]),len(newdic["inter"]["png"]),len(newdic["inter"]["others"])]
  for link in ex_list:
    if ".html" in link or ".htm" in link:
      newdic["ext"]["html"].append(link)
    elif ".css" in link:
      newdic["ext"]["css"].append(link)
    elif ".js" in link:
      newdic["ext"]["js"].append(link)
    elif ".jpg" in link or ".jpeg" in link:
      newdic["ext"]["jpg"].append(link)
    elif ".png" in link:
      newdic["ext"]["png"].append(link)
    else:
      newdic["ext"]["others"].append(link)
  print(f"External sites:->\n")
  print(f"Total : {len(ex_list)}\n")
  print(f"HTML : {len(newdic['ext']['html'])}\n")
  for i in newdic["ext"]["html"]:
    print(f"{i}\n")
    print(f"CSS : {len(newdic['ext']['css'])}\n")
  for i in newdic["ext"]["css"]:
    print(f"{i}\n")
  print(f"JS : {len(newdic['ext']['js'])}\n")
  for i in newdic["ext"]["js"]:
    print(f"{i}\n")
  print(f"JPG : {len(newdic['ext']['jpg'])}\n")
  for i in newdic["ext"]["jpg"]:
    print(f"{i}\n")
  print(f"png : {len(newdic['ext']['png'])}\n")
  for i in newdic["ext"]["png"]:
    print(f"{i}\n")
  print(f"Others : {len(newdic['ext']['others'])}\n")
  for i in newdic["ext"]["others"]:
    print(f"{i}\n")
  
  #condition for output yes and file size no
if args.output!=None and not(args.fsi=="Yes" or args.fsi=="yes" or args.fsi=="Y" or args.fsi=="y"):
  with open(args.output, "w") as file:

    file.write("Internal sites:->\n")
    file.write(f"Total : {len(list_new)}\n")
    file.write(f"HTML : {len(newdic['inter']['html'])}\n")
    for i in newdic["inter"]["html"]:
      file.write(f"{i}\n")
    file.write(f"CSS : {len(newdic['inter']['css'])}\n")
    for i in newdic["inter"]["css"]:
      file.write(f"{i}\n"
      )
    file.write(f"JS : {len(newdic['inter']['js'])}\n")
    for i in newdic["inter"]["js"]:
      file.write(f"{i}\n")
    file.write(f"JPG : {len(newdic['inter']['jpg'])}\n")
    for i in newdic["inter"]["jpg"]:
      file.write(f"{i}\n")
    file.write(f"png : {len(newdic['inter']['png'])}\n")
    for i in newdic["inter"]["png"]:
      file.write(f"{i}\n")
    file.write(f"Others : {len(newdic['inter']['others'])}\n")
    for i in newdic["inter"]["others"]:
      file.write(f"{i}\n")
  
    nlinks=[len(newdic["inter"]["html"]),len(newdic["inter"]["css"]),len(newdic["inter"]["js"]),len(newdic["inter"]["jpg"]),len(newdic["inter"]["png"]),len(newdic["inter"]["others"])]
    for link in ex_list:
      if ".html" in link or ".htm" in link:
        newdic["ext"]["html"].append(link)
      elif ".css" in link:
        newdic["ext"]["css"].append(link)
      elif ".js" in link:
        newdic["ext"]["js"].append(link)
      elif ".jpg" in link or ".jpeg" in link:
        newdic["ext"]["jpg"].append(link)
      elif ".png" in link:
        newdic["ext"]["png"].append(link)
      else:
        newdic["ext"]["others"].append(link)
    file.write(f"External sites:->\n")
    file.write(f"Total : {len(ex_list)}\n")
    file.write(f"HTML : {len(newdic['ext']['html'])}\n")
    for i in newdic["ext"]["html"]:
      file.write(f"{i}\n")
    file.write(f"CSS : {len(newdic['ext']['css'])}\n")
    for i in newdic["ext"]["css"]:
      file.write(f"{i}\n")
    file.write(f"JS : {len(newdic['ext']['js'])}\n")
    for i in newdic["ext"]["js"]:
      file.write(f"{i}\n")
    file.write(f"JPG : {len(newdic['ext']['jpg'])}\n")
    for i in newdic["ext"]["jpg"]:
      file.write(f"{i}\n")
    file.write(f"png : {len(newdic['ext']['png'])}\n")
    for i in newdic["ext"]["png"]:
      file.write(f"{i}\n")
    file.write(f"Others : {len(newdic['ext']['others'])}\n")
    for i in newdic["ext"]["others"]:
      file.write(f"{i}\n")
# plotting garphs using matplotlib
nelinks=[len(newdic["ext"]["html"]),len(newdic["ext"]["css"]),len(newdic["ext"]["js"]),len(newdic["ext"]["jpg"]),len(newdic["ext"]["png"]),len(newdic["ext"]["others"])]
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8))

br1 = np.arange(len(nlinks))
br2 = [x + barWidth for x in br1]
plt.bar(br1, nlinks , color ='r', width = barWidth,
        edgecolor ='grey', label ='Internal')
plt.bar(br2, nelinks , color ='g', width = barWidth,
        edgecolor ='grey', label ='External')

plt.xlabel('Types of links', fontweight ='bold', fontsize = 15)
plt.ylabel('number of links', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(nlinks))],
        ['html', 'css', 'js', 'jpg', 'png','others'])
plt.legend()
plt.savefig('pyplot.png')

if (args.fsi=="Yes" or args.fsi=="yes" or args.fsi=="Y" or args.fsi=="y"):

  plt.bar(br1, sizel , color ='r', width = barWidth,
          edgecolor ='grey', label ='Internal')
  plt.bar(br2, sizee , color ='g', width = barWidth,
          edgecolor ='grey', label ='External')

  plt.xlabel('Types of links', fontweight ='bold', fontsize = 15)
  plt.ylabel(' Total size of links', fontweight ='bold', fontsize = 15)
  plt.xticks([r + barWidth for r in range(len(nlinks))],
          ['html', 'css', 'js', 'jpg', 'png','others'])
  plt.legend()
  plt.savefig('pyplotsize.png')
