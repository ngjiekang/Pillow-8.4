from flask import Flask, request
from PIL.ImageMath as ImageMath
app = Flask(__name__)

#Example of a taint source using Flask
@app.route('/process_expression', methods=['POST'])
def process_expression():
    # Simulate receiving an expression from an untrusted source
    expression = request.form['expression']
    
    # This is where the taint analysis should flag a potential RCE risk
    # if the expression is not properly sanitized before being evaluated
    result = ImageMath.eval(expression)  # Hypothetical use of ImageMath that might be vulnerable
    
    return f"Result of the expression: {result}"
  
