from PIL import Image, ImageMath


def pixel(im):
    if hasattr(im, "im"):
        return "{} {}".format(im.mode, repr(im.getpixel((0, 0))))
    else:
        if isinstance(im, int):
            return int(im)  # hack to deal with booleans
        print(im)


A = Image.new("L", (1, 1), 1)
B = Image.new("L", (1, 1), 2)
Z = Image.new("L", (1, 1), 0)  # Z for zero
F = Image.new("F", (1, 1), 3)
I = Image.new("I", (1, 1), 4)  # noqa: E741

A2 = A.resize((2, 2))
B2 = B.resize((2, 2))

images = {"A": A, "B": B, "F": F, "I": I}


def test_sanity():
    assert ImageMath.eval("1") == 1
    assert ImageMath.eval("1+A", A=2) == 3
    assert pixel(ImageMath.eval("A+B", A=A, B=B)) == "I 3"
    assert pixel(ImageMath.eval("A+B", images)) == "I 3"
    assert pixel(ImageMath.eval("float(A)+B", images)) == "F 3.0"
    assert pixel(ImageMath.eval("int(float(A)+B)", images)) == "I 3"


def test_ops():
    assert pixel(ImageMath.eval("-A", images)) == "I -1"
    assert pixel(ImageMath.eval("+B", images)) == "L 2"

    assert pixel(ImageMath.eval("A+B", images)) == "I 3"
    assert pixel(ImageMath.eval("A-B", images)) == "I -1"
    assert pixel(ImageMath.eval("A*B", images)) == "I 2"
    assert pixel(ImageMath.eval("A/B", images)) == "I 0"
    assert pixel(ImageMath.eval("B**2", images)) == "I 4"
    assert pixel(ImageMath.eval("B**33", images)) == "I 2147483647"

    assert pixel(ImageMath.eval("float(A)+B", images)) == "F 3.0"
    assert pixel(ImageMath.eval("float(A)-B", images)) == "F -1.0"
    assert pixel(ImageMath.eval("float(A)*B", images)) == "F 2.0"
    assert pixel(ImageMath.eval("float(A)/B", images)) == "F 0.5"
    assert pixel(ImageMath.eval("float(B)**2", images)) == "F 4.0"
    assert pixel(ImageMath.eval("float(B)**33", images)) == "F 8589934592.0"


def test_logical():
    assert pixel(ImageMath.eval("not A", images)) == 0
    assert pixel(ImageMath.eval("A and B", images)) == "L 2"
    assert pixel(ImageMath.eval("A or B", images)) == "L 1"


def test_convert():
    assert pixel(ImageMath.eval("convert(A+B, 'L')", images)) == "L 3"
    assert pixel(ImageMath.eval("convert(A+B, '1')", images)) == "1 0"
    assert pixel(ImageMath.eval("convert(A+B, 'RGB')", images)) == "RGB (3, 3, 3)"


def test_compare():
    assert pixel(ImageMath.eval("min(A, B)", images)) == "I 1"
    assert pixel(ImageMath.eval("max(A, B)", images)) == "I 2"
    assert pixel(ImageMath.eval("A == 1", images)) == "I 1"
    assert pixel(ImageMath.eval("A == 2", images)) == "I 0"


def test_one_image_larger():
    assert pixel(ImageMath.eval("A+B", A=A2, B=B)) == "I 3"
    assert pixel(ImageMath.eval("A+B", A=A, B=B2)) == "I 3"


def test_abs():
    assert pixel(ImageMath.eval("abs(A)", A=A)) == "I 1"
    assert pixel(ImageMath.eval("abs(B)", B=B)) == "I 2"


def test_binary_mod():
    assert pixel(ImageMath.eval("A%A", A=A)) == "I 0"
    assert pixel(ImageMath.eval("B%B", B=B)) == "I 0"
    assert pixel(ImageMath.eval("A%B", A=A, B=B)) == "I 1"
    assert pixel(ImageMath.eval("B%A", A=A, B=B)) == "I 0"
    assert pixel(ImageMath.eval("Z%A", A=A, Z=Z)) == "I 0"
    assert pixel(ImageMath.eval("Z%B", B=B, Z=Z)) == "I 0"


def test_bitwise_invert():
    assert pixel(ImageMath.eval("~Z", Z=Z)) == "I -1"
    assert pixel(ImageMath.eval("~A", A=A)) == "I -2"
    assert pixel(ImageMath.eval("~B", B=B)) == "I -3"


def test_bitwise_and():
    assert pixel(ImageMath.eval("Z&Z", A=A, Z=Z)) == "I 0"
    assert pixel(ImageMath.eval("Z&A", A=A, Z=Z)) == "I 0"
    assert pixel(ImageMath.eval("A&Z", A=A, Z=Z)) == "I 0"
    assert pixel(ImageMath.eval("A&A", A=A, Z=Z)) == "I 1"


def test_bitwise_or():
    assert pixel(ImageMath.eval("Z|Z", A=A, Z=Z)) == "I 0"
    assert pixel(ImageMath.eval("Z|A", A=A, Z=Z)) == "I 1"
    assert pixel(ImageMath.eval("A|Z", A=A, Z=Z)) == "I 1"
    assert pixel(ImageMath.eval("A|A", A=A, Z=Z)) == "I 1"


def test_bitwise_xor():
    assert pixel(ImageMath.eval("Z^Z", A=A, Z=Z)) == "I 0"
    assert pixel(ImageMath.eval("Z^A", A=A, Z=Z)) == "I 1"
    assert pixel(ImageMath.eval("A^Z", A=A, Z=Z)) == "I 1"
    assert pixel(ImageMath.eval("A^A", A=A, Z=Z)) == "I 0"


def test_bitwise_leftshift():
    assert pixel(ImageMath.eval("Z<<0", Z=Z)) == "I 0"
    assert pixel(ImageMath.eval("Z<<1", Z=Z)) == "I 0"
    assert pixel(ImageMath.eval("A<<0", A=A)) == "I 1"
    assert pixel(ImageMath.eval("A<<1", A=A)) == "I 2"


def test_bitwise_rightshift():
    assert pixel(ImageMath.eval("Z>>0", Z=Z)) == "I 0"
    assert pixel(ImageMath.eval("Z>>1", Z=Z)) == "I 0"
    assert pixel(ImageMath.eval("A>>0", A=A)) == "I 1"
    assert pixel(ImageMath.eval("A>>1", A=A)) == "I 0"


def test_logical_eq():
    assert pixel(ImageMath.eval("A==A", A=A)) == "I 1"
    assert pixel(ImageMath.eval("B==B", B=B)) == "I 1"
    assert pixel(ImageMath.eval("A==B", A=A, B=B)) == "I 0"
    assert pixel(ImageMath.eval("B==A", A=A, B=B)) == "I 0"


def test_logical_ne():
    assert pixel(ImageMath.eval("A!=A", A=A)) == "I 0"
    assert pixel(ImageMath.eval("B!=B", B=B)) == "I 0"
    assert pixel(ImageMath.eval("A!=B", A=A, B=B)) == "I 1"
    assert pixel(ImageMath.eval("B!=A", A=A, B=B)) == "I 1"


def test_logical_lt():
    assert pixel(ImageMath.eval("A<A", A=A)) == "I 0"
    assert pixel(ImageMath.eval("B<B", B=B)) == "I 0"
    assert pixel(ImageMath.eval("A<B", A=A, B=B)) == "I 1"
    assert pixel(ImageMath.eval("B<A", A=A, B=B)) == "I 0"


def test_logical_le():
    assert pixel(ImageMath.eval("A<=A", A=A)) == "I 1"
    assert pixel(ImageMath.eval("B<=B", B=B)) == "I 1"
    assert pixel(ImageMath.eval("A<=B", A=A, B=B)) == "I 1"
    assert pixel(ImageMath.eval("B<=A", A=A, B=B)) == "I 0"


def test_logical_gt():
    assert pixel(ImageMath.eval("A>A", A=A)) == "I 0"
    assert pixel(ImageMath.eval("B>B", B=B)) == "I 0"
    assert pixel(ImageMath.eval("A>B", A=A, B=B)) == "I 0"
    assert pixel(ImageMath.eval("B>A", A=A, B=B)) == "I 1"


def test_logical_ge():
    assert pixel(ImageMath.eval("A>=A", A=A)) == "I 1"
    assert pixel(ImageMath.eval("B>=B", B=B)) == "I 1"
    assert pixel(ImageMath.eval("A>=B", A=A, B=B)) == "I 0"
    assert pixel(ImageMath.eval("B>=A", A=A, B=B)) == "I 1"


def test_logical_equal():
    assert pixel(ImageMath.eval("equal(A, A)", A=A)) == "I 1"
    assert pixel(ImageMath.eval("equal(B, B)", B=B)) == "I 1"
    assert pixel(ImageMath.eval("equal(Z, Z)", Z=Z)) == "I 1"
    assert pixel(ImageMath.eval("equal(A, B)", A=A, B=B)) == "I 0"
    assert pixel(ImageMath.eval("equal(B, A)", A=A, B=B)) == "I 0"
    assert pixel(ImageMath.eval("equal(A, Z)", A=A, Z=Z)) == "I 0"


def test_logical_not_equal():
    assert pixel(ImageMath.eval("notequal(A, A)", A=A)) == "I 0"
    assert pixel(ImageMath.eval("notequal(B, B)", B=B)) == "I 0"
    assert pixel(ImageMath.eval("notequal(Z, Z)", Z=Z)) == "I 0"
    assert pixel(ImageMath.eval("notequal(A, B)", A=A, B=B)) == "I 1"
    assert pixel(ImageMath.eval("notequal(B, A)", A=A, B=B)) == "I 1"
    assert pixel(ImageMath.eval("notequal(A, Z)", A=A, Z=Z)) == "I 1"

from flask import Flask, request
app = Flask(__name__)
import builtins
@app.route("/files/<expression>")
def analyze_file(expression):
  with Image.open("image1.jpg") as im1:
    with Image.open("image2.jpg") as im2:
        out = ImageMath.eval(expression, a=im1, b=im2)
        out.save("result.png")
        builtins.eval(expression)

import requests
from io import BytesIO
def test_with_tainted_image_source():
    # URL of a potentially tainted external image
    url = "https://example.com/path/to/suspicious/image.jpg"

    # Fetch the image
    response = requests.get(url)
    response.raise_for_status()  # Ensure that the request was successful

    # Open the image with Pillow
    with BytesIO(response.content) as f:
        tainted_image = Image.open(f)

    # Perform an ImageMath operation (example)
    # Assuming that we're testing if ImageMath can handle a potentially corrupted image
    try:
        result = ImageMath.eval("convert(a, 'L')", a=tainted_image)
        # You might want to check specific aspects of the result here
        self.assertIsNotNone(result)
    except Exception as e:
        # Optionally, catch exceptions if the tainted image causes unexpected errors
        self.fail(f"Handling of tainted image source failed: {e}")


@app.route('/process_expression/<expression>')
def process_expression():
    # Simulate receiving an expression from an untrusted source
    #expression = request.form['expression']
    
    # This is where the taint analysis should flag a potential RCE risk
    # if the expression is not properly sanitized before being evaluated
    result = ImageMath.eval(expression)  # Hypothetical use of ImageMath that might be vulnerable
    
    return f"Result of the expression: {result}"
