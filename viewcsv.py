# Import here all modules that your app import explicitly, otherwise PyInstaller will not know they
# are needed and produce an executable that complains about "ModuleNotFoundError".

import pandas
import streamlit
import plotly.express

# These imports are needed for the streamlit execution below.
import streamlit.web.cli as stcli
import sys

if __name__ == "__main__":
    sys.argv=["streamlit", "run", "viewmkicsv.py", "--global.developmentMode=false"]
    sys.exit(stcli.main())