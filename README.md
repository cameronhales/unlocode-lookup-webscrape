# unlocode-lookup-webscrape
UN/LOCODE is a 5 letter identifier for ports across the world, their website provides html tables for reference, but no lookup table. This project creates a simple lookup table for UN/LOCODE and Country and Port Name.

_______
## using Jupytext
This was written in a notebook but converted into a python file for better version control using a package called jupytext

To convert from .py to .ipynb open a terminal and type:
```jupytext --to notebook src/unlocode-lookup.ipynb```

And if you want to commit any changes convert back to a .py file using:
```jupytext --to py:percent src/unlocode-lookup.ipynb```

________

Also this should be used for educational purposes only and you should probably read the terms and conditions of a website before you use webscraping.