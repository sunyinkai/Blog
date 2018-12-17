import requests
import re
import urllib
import time
# from selenium import webdriver
# # headers={
# # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
# # Chrome/70.0.3538.110 Safari/537.36'
# # }
# url='http://www.51nod.com/Challenge/Problem.html#!#problemId=1663'
# # content=urllib.open(url).read()
# # print(content)
# brower=webdriver.Chrome()
# brower.get(url=url)
# time.sleep(20)
# pageSource=brower.page_source
# with open('a.html','w') as f:
#     f.write(pageSource)
# brower.close()

headers={
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
 Chrome/70.0.3538.110 Safari/537.36'
}
# url='http://www.51nod.com/Challenge/Problem?problemId=1252'
# t=requests.get(url=url,headers=headers)
# content=t.content.decode()
# with open('a.txt','w') as f:
#     f.write(content)
f=open('a.txt','r')
content=f.read(10240)
print(type(content))
print(content)
str=''
#title
title_pattern='"Title":"(.*?)","IsPay"'
title=re.findall(pattern=title_pattern,string=content)
title=title[0].replace('\\n','\n')
print(title)

#description
descripion_pattern='"Description":"(.*?)","InputDescription'
descripion=re.findall(pattern=descripion_pattern,string=content)
print(descripion)
descripion=descripion[0]
print(descripion)






#input_description
input_pattern='"InputDescription":"(.*?)OutputDescription"'
input_description=re.findall(pattern=input_pattern,string=content)
input_description=input_description[0]
print(input_description)
print('----out-----')
#output_descrition
output_pattern='"OutputDescription":"(.*?)","'
output_descrition=re.findall(pattern=output_pattern,string=content)
output_descrition=output_descrition[0]
print(output_descrition)


#inputSample
input_pattern='"InputSample":"(.*?)","OutputSample"'
input_sample=re.findall(pattern=input_pattern,string=content)
input_sample=input_sample[0]
print(input_sample)

#outputSample
output_pattern='"OutputSample":"(.*?)","TimeLimit":'
output_sample=re.findall(pattern=output_pattern,string=content)
output_sample=output_sample[0].replace('\\n','\n')
print(output_sample)

timelimit_pattern=''

f.close()
with open('out.txt','w') as f:
    f.write(str)
