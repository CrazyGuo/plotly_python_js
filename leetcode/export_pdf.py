import pdfkit

tool_path = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
confg = pdfkit.configuration(wkhtmltopdf=tool_path)
pdfkit.from_url("https://leetcode-cn.com/problems/h-index-ii/solution/hzhi-shu-ii-by-leetcode/", "test.pdf", configuration=confg)

for i in range(790, 926): 
    url='https://github.com/grandyang/leetcode/issues/%d' % i
    #这里指定一下wkhtmltopdf的路径，这就是我为啥在前面让记住这个路径
    file_name = "%d.pdf" % i
    pdfkit.from_url(url, file_name, configuration=confg)
    print(file_name)