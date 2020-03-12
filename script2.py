import pandas as pd
from sqlalchemy import create_engine

testFrame=pd.read_csv("BuildingLocations .csv",names=['Location','Lat','Long'])

engine=create_engine('sqlite://',echo=False)
testFrame.to_sql('locales',con=engine)
testResult = engine.execute("SELECT Location FROM locales")

for row in testResult:
    print("Location:",row['Location'])
