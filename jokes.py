#jokes
import pyjokes

def getjoke():
    the_joke = str(pyjokes.get_joke(language="en",category="neutral"))
    return the_joke

