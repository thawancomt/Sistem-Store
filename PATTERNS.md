Rule for URLS:
    All homepage's need to be called index

Rule for variables name:
    All the context passed to the front end need to be passed trought the context variable
    the context variable need to be a dictionary

Rule for Flaks Patterns:
    Never use a if statement to check the request method, like:
        "if request.method == 'POST' ..."
    
    Always use get and post decorators to handle the get and post routes

Rule for HTML files
    The names of files need to Be SnakeCase

Rule for CRUD process
    READ METHOD's
        The get all method need to be Called get_all
        the get by id  method need to be called get_by_id
        the get by username method  need to be called get_by_username
        the get by date method need to be called get_by_date

    Create method's
        All the creation of data on db need to be called as create
        
        Only 1 way of insertion is accepted

        All the creation throgh the insert method need to be checked against a schema
    
    Update method's
        All the update method's needs to include "update" on its name:
            not "Edit" or "modify/modification"
        All the update views need to be called update_view
        All the update endpoint that support post, need to be called update
        
Global Security Rules:
    All the endpoint needs a login level, except by the login page obvisly
    