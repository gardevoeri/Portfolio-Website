# PORTFÓLIO WEBSITE WITH PYTHON FLASK
#### Video Demo:  https://www.youtube.com/watch?v=rZdmwDA8Gjw
#### Description: A portfólio website created with Python flask, using HTML, CSS, Javascript and SQLite with portóflio and blog pages and a restricted area for logged users create, edit and delete projects and blog posts.

# The Project
This project consists of a aplication **app.py** with the main project, an **helpers.py** file with functions to assist the main functioning of the app, a database to store the information about users, projects and blog posts **portfolio.db**, a folder **static** with the files with CSS, Javascript and static images, logos and icons of the webpage, a folder **uploads** to store de images of projects and blog posts and a **templates** folder with the templates of the pages for the website.

## app.py
In app.py we have the main app with the functions to create the views that allow us to access the webpages of our website. The first lines of code show the **import** of the libraries used in the aplication. The **os** library that allows to manipulate diferent directories to access the files, the **CS50** librarie that allows to use SQL in the app, the **flask** librarie to create the app and views necessary to our webpage, the **flask_session** to create the diferent sessions to be accessed by the users, **werkzeug.security** library is used to ensure the security of passwords for the users in sessions and the **datetime** library to access the date and time of the creation on blog posts and projects created. From the **helpers.py** import we have the function that allow us to control which pages can be accessed with and without a login with the function *login_required* and create a page for errors in access with the *apology* function.

After that we have the configurations of the application, the sessions configurations, the uploads folder access configurations and then the inicialization of the session and the database access creation.

### The functions in app.py
The first function is **after_request()** that ensures that the access of the users is not saved in cache so it has to be redone after the end of each new session. The function *login* is accessed by */login* and query the database in the table users checking if the username provided via POST by the form exists in the database and verify if the password is correct by using the *check_password_hash()* function. If its correct the user is granted access to the admin area with the *redirect()* funtion to the */admin* path or is sent to the *apology()* function page. If the route is accessed via GET the *login.html* page is rendered with the function *render_template()*

The function **logout()** has the route */logout* accessed via GET and clears the session of the user redirecting it then back to the */login* page.

The **register()** function creates new users to access the admin area. Via POST access the username, password and password confirmation provided in a form at the *register.html* page. The function confirms if the two passwords provided are equal. If they are not the same the *flash()* function is called to show the warning to the user and then its sent back to the register page. If the passwords match then a new row is added to the database in the table users with the new user created. Then the *flash()* function is called again confirming that the user was registered.

The **admin()** function is responsible for creating new projects and blog posts and accessing then in the search area. This function has a *@login_required* view. It means that can only be accessed if a session is active with a valid login from the users table. It queries the database for the username of the current user so it can be displayed on the page. Than are created two empty lists for projects and blogposts that will be populated later with the database query from the form received via POST. To create a project is verified if the variable for the title of the project is not empty them the other requests are inserted to the database and its created a path to the image of the post in the *uploads* folder if a image was provided. The same process is than called for creating a blogpost. To search for projects and blogposts than id verified if via POST was received a request for a search and them is used a wild card and the request value to query the database for titles corresponding to the search.

The **delete-post(id)** function has as parameter the *id* of the post to be deleted that is received via GET when the link to the post is accessed in the admin page. Then the database is query to delete the post with the same id.

The **edit-post(id)** function is similiar to the *delete-post(id)* but instead of deleting it, the *request.method* POST is verified. If the method is GET the database is queried for the post current data, and then the fields in the form at the page are filled with the current information to be edited. If the method is POST, it means that there is a edition to be sent to the database and them the data on the form is them sent as a UPDATE to the database table.

The functions **delete-project(id)** and **edit-project(id)** has the same functioning as the *delete-post(id)* and *edit-post(id)* functions.

The functions **index()** and **about()** are used to render the templates of the html pages.

The functions **projects()** and **blog()** create the access to the templates of those two pages and query the database tables to send to the pages the posts that exist to be accessed.

The functions **project_content(id)** and **blog_content(id)** send to their pages the content of the project and blog post thar was accesed via link in the project and blog page.

The **download_file(name)** function is responsable for creating the endpoint to the uploads folder so the images can then be accessed by the pages.


## helpers.py
The purpose of the file is to have functions that support the functining of *app.py* with functions that can be used in other situations and are not necessarily atached to the main purpose of the aplication.

### The functions in helpers.py

The **login_required(f)** function remembers the accessed login to permit the access to areas where the login is required without the need to new access.

The **apology(message, code=400)** is used to render an apology message in case of incorrect usage. The default value for code is 400 but the function was used with diferent code value in app.py to represent the code 401, for user or password invalid. When called the function renders the template *fail.html*.

[!NOTE] The functions in helpers.py where used previously in the project for pset9 Finance in CS50 and adapted to this project.

## portfolio.db

The **portfolio.db** database was created using SQLite3 and has the tables **users** to armazenate the usernames and password_hash of the passwords for the access of the admin area, the table **projects** to store the projects that will be displayed in the projects page and the table **blog** to store the blog posts to be presented in the blog page.

The following is the query used to create the *users* table:

```
CREATE TABLE users  (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
username TEXT NOT NULL,
hash TEXT NOT NULL )
```

The following is the query used to create the *projects* table:

```
CREATE TABLE projects  (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
title TEXT NOT NULL,
tools TEXT,
image TEXT,
description TEXT,
content TEXT,
datetime TEXT )

```

The following is the query used to create the *blog* table:

```
CREATE TABLE blog  (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
title TEXT NOT NULL,
keywords TEXT,
image TEXT,
description TEXT,
content TEXT,
datetime TEXT )
```

## The uploads folder
This folder stores the images sent via POST to the admin area when creating a blog post of project. They are stored with the name of the database where they name will be stored then the id of the blog post or project to which will be conected.

## The static folder
The static folder has three other folders: **assets**, **css** and **script**.

The **assets** folder stores the static images of the project like icons, logos and photos. Images that will not change with the new posts os projects sent.
The **css** folder stores the css files used in the layout page, admin page and other hmtl pages of the project. The *admin.css* is responsible for the layout and style in the admin area and pages related. The *layout.css* file has the CSS structure to the main pages of the project with the css reset and utilitary classes. The *style.css* has the design choices of the website, with color choices for buttons, titles, font sizes and styles and background images and filters.
The **script** folder stores the script for the admin pages and related pages to its access, the login page and the main website.

### The functions in the script folder
In *script.js* we have the *navToggle* used to transform the navbar view of the site in to a hamburguer toggle view for smaller screens making the website fully responsive. It uses an Event Listener method to open and close the navbar to access the content.
In the *login.js* file we have the validation function to send messages to the user if the username or password was not filled correctly without the need of validation on the server site of the aplication.
In the *admin.js* file is the function to allow a toggle to the diferent areas of usage of the admin page, displaying only the area that is currently in use, creating tabs for each of the areas.

[!NOTE]In this project was not used any type of framework for CSS or Javascript. This website uses the vanilla form of CSS and Javascript.


## The templates folder
The templates folder is where all the html pages are stored. The pages can be accessed with or without *login_required* method depending on the content.

**layout.html**
The *layout.html* page contain the main layout of the free accessed pages of the website. The page links with a *link* tag to the css *layout.css* and *style.css* stylesheets. The *title* tag contains a *jinja* block to create new titles in the extended pages. The page is divided in three main areas: the *header* where is located the navbar to be displayed in all webpages, the *main* that contains the jinja block for the main content of each page to be located and the *footer* that also will be displayed in all pages. In the navbar at the header a *anchor* tag *a* with a logo svg sending to the home page, and a hidden svg for a toggle button to be displayed only in smaller screens. The nav bar has a *ul* tag with the links to the pages of the website: Home (the index), About, Projects and Blog all being anchored to the routes in app.py.
The footer has anchor tags to the social media acounts and a smaller ul tag with the same links to pages and again the main logo with then a anchor tag to the route for the restricted area connecting to the admin page.

**index.html**
The *index* page of the website extends the content of the layout page with its content only in the main block. The page is divided then in four section tags. A *hero* section, a *about* section, a *projects* section and a *blog* section. Each of the section shows a small part of the pages corresponding to its content. Being the hero section a background image, with a button that leads to the about section bellow, a *h1* tag for the main title and a subtitle. The about section has a short introdutory paragraph with an image an a link to the about page, a link to social media (hire) and a link do file download(curriculum). The project section has a selection of some of the projects to being displayed in a mosaic grid. Each project leads to the project-content page and the MORE anchor takes to the projects page. In the blog section the first card has a link to a choosen blog post, them  to smaller anchors take to the last blog post submited and a diferent blog post by choice.

**about.html**
The *about* page aldo extends the layout page showing the navbar and footer. The main content is divided in two sections with complementary paragraphs for information and a image of the creator. In the end of the first section a anchor to the blog page and in the end of the second a anchor to the projects page. The content of the main is wraped in a *article* tag.

**projects.html**
The *projects* page display all the projects that exist in the database in cards. The jinja sintax allows to insert the information of each project in a diferent card from the list projects sent from the *projects()* function. By clicking the anchor tag in each project card the project-content page of the project id selected is displayed.

**projects-content.html**
Shows the content of the project with the id selected in the card of choice from the projects page.


**blog.html**
The *blog* page display all the blogposts that exist in the database in cards. The jinja sintax allows to insert the information of each post in a diferent card from the list blogposts sent from the *blog()* function. By clicking the anchor tag in each post card the blog-content page of the post id selected is displayed.

**blog-content.html**
Shows the content of the blogpost with the id selected in the card of choice from the blog page.

**login.html**
The *login* page extends the admin layout and the main block contain a form for entering the username and password to access the restricted area. The tag *span* above the form with an id of *error* is responsible for showing the validation messages from the script.

**fail.html**
The fail page is displayed when the *apology()* function is called in app.py. The content is a image with the source for the memegen api content and a link using the anchor tag to the login page for a new attempt.

**admin.html**
The admin page is displayed with a correct login from the user.
The page has a block for diferent scripts link using jinja syntax and a block for a title aswell. The body is divided in three main parts, the header with a navbar, a main content and a footer. The header has a title *h2* text and a anchor to the */logout* route to disconect the current user. The main block has the tabs for each part of the content to be displayed separetly using the script function.

The *search* div contains two forms, one for consulting the projects and another for blogposts sent via POST to the */admin* route. Bellow the search forms the table to show the contents of the querys with the for loops to access the content of each project and blog post. The delete and edit buttons redirect to the */delete-project* or */delete-post* and the    */edit-project* and */edit-post* routes.

The *new-project* div contains the form to insert a new project in the database. The input tags receive the content that is sent to the /admin to query the database for the new content.

The *new-blog-post* div works the same way as the new-project div now sending the content to the blog table.

The register area is displayed in the iframe in the end of the page.

The footer has a ul with the anchor for all the pages in the website for easy access and a link to the github page of the creator.

**register.html**
The register page is accessed through a *iframe* tag in the admin.html page. The page links with the script *login.js* for validation of the form. In the top of the body a jinja for loop to access the flash() function that display messages of error and validations for the content sent to the server for valid password compatibilty and correct registration of the new user. The span tag above the form display the validation from the scrip and the form sends via POST the data to the /register route in app.py.

**edit-project.html** and **edit-post.html**
The *edit-project* and *edit-post* pages extend the admin page layout. The main content of both pages are the same form structure present in the admin page to create new project and blog post. The content of the input fields now receive the query result of the project and post informed in the id at the search. The form then is sent to the routes */edit-project/id* or */edit-post/id* to update the database tables.
