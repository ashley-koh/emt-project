import eel

eel.init('web')

@eel.expose
def click_func_py():
  eel.changeHtml()

eel.start('index.html')