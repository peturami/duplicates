<h1>Tool for finding duplicates in files</h1>

The main function of this tool is finding duplicates in large csv/txt files. After defining parameters of the file (encoding - default is utf-8 and separator - default is ",") user can analyze file based on selected columns or whole rows and then save output to the file.

There are some other functions such as displaying part of the file content (could be handy when user doesn't know which separator to use) and splitting file into smaller chunks.

The tool consists of two scripts - dupl_frontend.py, dupl_frontend.py. To run this tool user can use runsDuplicates.bat where is neccessary to filled full path to python.exe with installed required packages. 


<h3>Used packages:</h3>
<ul>
  <li>Pandas</li>
  <li>Tkinter</li>
  <li>OS</li>
</ul>  
