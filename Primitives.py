from LOTlib.Evaluation import primitive

@primitive
def red_(img):
    return 'RED' in img.split('_')

@primitive
def green_(img):
    return 'GREEN' in img.split('_')

@primitive
def triangle_(img):
    return 'TRIANGLE' in img.split('_')

@primitive
def square_(img):
    return 'SQUARE' in img.split('_')

@primitive
def large_(img):
    return 'LARGE' in img.split('_')

@primitive
def small_(img):
    return 'SMALL' in img.split('_')