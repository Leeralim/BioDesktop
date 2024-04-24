<p align="center">
  
  <div id="header" align="center">
    
  ![vniro_logo](https://github.com/Leeralim/BioDesktop/assets/49206103/8d771b81-2e45-41d7-ab60-a1cf79e161cf)
  
  </div>
    
  <h1 align="center" style="margin: 0 auto 0 auto;">BioDesktop</h1>
  <p align="center" style="margin: 0 auto 0 auto;">BioDesktop is a program written using the CustomTkinter UI-library. This program was developed for biologist scientists to process cruise biology data, longline cruises, correct and then load it into a database, as well as process data from Norwegian scientists for subsequent exchange with them. Available in light and dark themes.</p>
</p>

<br>

![image](https://github.com/Leeralim/BioDesktop/assets/49206103/0e9a96cd-df40-43fa-994d-769c414427e2)
| _`BioDesktop.py` on Windows 10 with dark mode_

![image](https://github.com/Leeralim/BioDesktop/assets/49206103/08fe7f4f-a777-4c18-b3ac-79b2bb99ce96)
| _`BioDesktop.py` on Windows 10 with light mode_

<br>


## 🔨 Instruments
The following instruments were used for development:
<div>
  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/pandas/pandas-original-wordmark.svg" title="Pandas" alt="Pandas" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/numpy/numpy-original-wordmark.svg" title="Numpy" alt="Numpy" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/postgresql/postgresql-original-wordmark.svg" title="Postgresql" alt="Postgresql" width="40" height="40"/>&nbsp;
</div>


## 📝 Formulation of the task
Upon completion of a research expedition (as a rule, it is carried out in the Barents and Norwegian Seas), the scientific expedition team brings various primary biological data:
- data on the species composition of aquatic organisms in certain areas (local in the Barents Sea, economic zones, ICES\NAFO), catch size, etc.
- data for biological analysis: indicators of sex, size, weight, age of individuals, fat content, samples, etc.
- trawl fishing data: coordinates, air temperature, water temperature, trawling horizon, etc.

Subsequently, this information is supplemented, adjusted and loaded into the database. The task was set to develop a program for operational scientists so that they could work with such data.

In the case of Norwegian data, it is necessary to process the resulting file, parse it and obtain from it the correct structure for loading into the database.

Voyages can be different - regular trawl voyages, using longlines, and individual Norwegian voyages. The program allows you to choose what information to work with:

![image](https://github.com/Leeralim/BioDesktop/assets/49206103/47bebdf9-8ac5-4544-b7f4-e074d5a7e782)

In terms of functionality, a regular trawl and a longline trawl are the same. Only the data and the slightly structure of the tables differ. Norwegian information processing is different.

## ⤵️ Unloading from the database

Sometimes scientists may need to unload a specific sea voyage from the database to make some calculations and adjustments. Data must be uploaded in CSV format. The user enters the call sign and sea voyage number, selects the directory where files from the database will be uploaded.

![image](https://github.com/Leeralim/BioDesktop/assets/49206103/b676f293-0979-4310-a7d9-75fdc133507f)

## ❌ Removal from the database
Sometimes a situation may arise when you need to delete one of the sea voyages in order to load it again after certain calculations and changes. The user enters the call sign and sea voyage number. The sea voyage is deleted from all tables in the database.

![image](https://github.com/Leeralim/BioDesktop/assets/49206103/69c9b218-a882-45e6-b803-fa86eab6edb2)

