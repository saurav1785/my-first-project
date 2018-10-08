from bs4 import BeautifulSoup
import urllib.request
from flask import Flask, request,render_template,redirect,url_for
app = Flask(__name__)
headers = {}
headers['User-Agent']='Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'

class NewsMe:
    def __init__(self, url,order=1):
        self.url=url
        self.order = order
        req = urllib.request.Request(self.url,headers=headers)
        resp = urllib.request.urlopen(req)
        scrap_data = BeautifulSoup(resp.read(),"html.parser")
        self.scrap_data = scrap_data

    def html(self):
        return self.scrap_data.prettify()

    def headlines(self):
        d_1 = []
        a=[]
        self.head_list = [(i.text, i.get('a')) for i in self.scrap_data.find_all("h2")]
        _n = self._AvgHeadLen()
        for i in self.head_list:
            if len(i[0].strip()) > _n:
                d_1.append((i[0].strip(),i[0]))
        for link in self.scrap_data.find_all('a'):
            b = link.get('href')
            b = str(b)
            if(b.startswith("http",0,len(b))):
                print(b)
        return d_1


    def _AvgHeadLen(self):
        total_letter = 0
        for i in self.head_list:
            total_letter = total_letter+len(i[0].strip())
        return int(total_letter//len(self.head_list)*self.order)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/show/<search1>')
def show(search1):
    list2=[]
    search1='https://'+search1+'/'
    obj1 = NewsMe(search1)
    a=obj1.headlines()
    for i in range(len(a)):
        list2.append(a[i][0])
    return render_template('index.html',text=tuple(list2))

@app.route('/search_result', methods = ['POST','GET'])
def search_result():
    if request.method == "POST":
        search = request.form['news_search']
        return redirect(url_for('show', search1 = search))


if __name__ == '__main__':
    app.run(debug=True)
