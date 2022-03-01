from distutils.log import debug
from flask import Flask, render_template, request
import requests
import language_tool_python
app=app = Flask(__name__)

tool = language_tool_python.LanguageTool('en-US')

class grammer_correction:
    def __init__(self,text=""):
        self.text=text
        self.corr_text=""
    
    def gram_check(self):
        matches = tool.check(self.text)
        my_mistakes = []
        my_corrections = []
        start_positions = []
        end_positions = []
        
        for rules in matches:
            if len(rules.replacements)>0:
                start_positions.append(rules.offset)
                end_positions.append(rules.errorLength+rules.offset)
                my_mistakes.append(self.text[rules.offset:rules.errorLength+rules.offset])
                my_corrections.append(rules.replacements[0])
        my_new_text = list(self.text)
        
        for m in range(len(start_positions)):
            for i in range(len(self.text)):
                my_new_text[start_positions[m]] = my_corrections[m]
                if (i>start_positions[m] and i<end_positions[m]):
                    my_new_text[i]=""
        self.corr_text = "".join(my_new_text)
        
obj=grammer_correction()        
        



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST','GET'])
def take_data():
    obj.text=request.form['text1']
    obj.gram_check()
    return render_template('result.html',value1=obj.text,value2=obj.corr_text)


if __name__ == '__main__':
    app.debug=True
    app.run()