from flask import Flask

from Pages import MainpageBlueprint
from Pages import ResponseBlueprint

fl = Flask(__name__, template_folder="templates")

fl.register_blueprint(MainpageBlueprint().get_blueprint())
fl.register_blueprint(ResponseBlueprint().get_blueprint())


if(__name__=="__main__"):
    fl.run(debug=True,port=8080)
