#jokes
import pyjokes

def get_joke():
    the_joke = str(pyjokes.get_joke(language="en",category="neutral"))
    return the_joke

