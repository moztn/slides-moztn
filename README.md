slides-moztn
============

## Description :
slides-moztn is a webapp written with the micro web framework Flask
 
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
     sudo pip install -r requirements.txt
   </pre>

  4-Configuring the database:
   <pre>
     $ cd slides-moztn
     $ python first_run.py
   </pre>

  5-Running the App:
   <pre>
     $ python slides.py
   </pre>

  A webserver will be started so that you can access the web app via http://http://127.0.0.1:5000/


