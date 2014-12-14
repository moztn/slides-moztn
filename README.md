slides-moztn
============

## Description :
slides-moztn is a webapp written with the micro web framework Flask. It is basically a sort of platfom to aggregate all presentations  done by  Mozilla Tunisia community in different events. What makes this project different from Slideshare and Co is its support for presentations written in HTML5.
 
## Running :
pip and virtualenv need to be installed on your machine.

  1-Setting a virtual environment:
   <pre>
     mkdir venv
     virtualenv venv
     source venv/bin/activate
   </pre>


  2-Cloning the project
   <pre>
     cd venv
     git clone https://github.com/moztn/slides-moztn.git
   </pre>

 
  3-Installing dependencies:
   <pre>
     cd slides-moztn
     pip install -r requirements.txt
   </pre>


  4-Running the App:
   <pre>
     $ python slides.py
   </pre>

  5- Init data base :
   <pre>
     $ python first_run.py
   </pre>


  A webserver will be started so that you can access the web app via http://127.0.0.1:5000/

  You can check our page "GitHub Good Practices" (in french) via http://wiki.mozilla-tunisia.org/Github_good_practices 


