# EcoSwap

Welcome new team :)

Flask, sqlalchemy, sqlite

PLEASE READ

The main branch has the version of the code that covers everything (that works) we have done. Most things that need tweaking are removed here and there are more annotations to help understand the code. If you have extra time, feel free to contact any one of us if you would like to see the previous extra code. See below for the main details about this project

Main Features
1.	Dropdown
2.	Search bar
3.	Crud operations - you can add and remove Users, Products, Categories, Posts (blog)
4.	Blog
In our project, most CRUD operations are done by FlaskForms. We get the forms, receive the data then use that to update the database. The main parts that return data in JSON include the part at the bottom of the app.py file, under --Postman-- which returns you all the products. Here you can also update some of the product details through postman by:

  {"name":"test3","price":"5", "product_des":"see here now"}

We can change the price and the product_des, by calling the name of the product. Be aware that currently once you try to change the details you have to change both, otherwise the new details will be set to None. The other JSON parts are in the api.py (and the search part towards the bottom of the app.py).

  api/product?category_id=1

You can GET products by categories, and the search function will also return you the products through the ILIKE query.

Main Features in Detail

1.Dropdown The dropdown functionality could be found where products are being listed for a category. This is found in app.py.
2.Search Bar There are two parts of this currently. In the search.html there is a form that returns the products as JSON and this is the search bar we use and see, and is written in the app.py. In the api.py file, we have the version where you can also use

  api/search?name=bag

3.CRUD operations 
These could be found in the app.py and is applied to user, product, category and post. The update function is only applied to the product; however, all other CRUD operations are applied to the rest. You can find the update product section in this new branch in the app.py line 309.
4.The Blog Post Form
Main purpose of this is to allow the registered user to create blog posts. The user is able to create a post (line 184) and also delete it (line 264) through in the app.py. The deleting is done by selecting the name of the post.

