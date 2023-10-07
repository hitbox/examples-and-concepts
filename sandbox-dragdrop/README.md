## sandbox-dragdrop

Working out a full demo of:

1. load objects from database
2. render drag+drop html
3. post json back
4. deserialize and save to database

## dragdrop

Minimal Flask, SQLAlchemy, Marshmallow, etc. web application to verify
machinery is working.

### TODO

- Decide how to pack data and nesting structure into the html.
  - Probably just put the primary key of objects in a data attribute.
  - Probably another data attribute that keeps the name of the list of objects.
  - Other data attributes for use by frontend to enforce limits and constraints.
- Post data back to app.
- Validate limits and constaints in app.
- Validation errors back to frontend.
- Deserialize and save to database.
- Clean up the views.
- The things in dragdrop/dropzone.py are probably overkill. Since marshalling
  is required, probably just dump objects to dicts and lists and render with
  recursive Jinja macro.

## build_nested/build_nested.py

Simplified case used to work out recursive function to filter and parse
XML/HTML elements building a nested object that represents objects and their
relationships.

Used to write the walk_dragdrop function in dragdrop/static/dragdrop.js.

```python
python build_nested/build_nested.py build_nested/trucks_pads_workers.html
```

## build_nested/collapse_nested.py

A brief look into collapsing XML-like data, as in replacing a node with some of
its children.

## Get Started

Create virtual environment, activate and update pip.

```sh
python -m venv venv
source venv/bin/activate
python -m pip install -U pip
```

Install dependencies

```sh
pip install -U -r requirements.txt
```

Create instance folder and config with, at least, SQLAlchemy database URI

```sh
cat instance/config.py
```

```python
import sqlalchemy as sa

SQLALCHEMY_DATABASE_URI = sa.engine.URL.create(
    drivername = 'postgresql+psycopg',
    database = 'dragdrop_database_name',
)
```

Create environment variables for flask

```sh
export FLASK_APP="dragdrop.app"
export DRAGDROP_CONFIG="config.py" # relative to instance folder
```

Create database

```sh
createdb dragdrop_database_name
```

Initialize database and run

```sh
flask db create-all
flask db initdata
flask run
```

## How It Works

1. Start with the normally related SQLAlchemy models.
   In this case,
   a. Trucks have a relation to pads which means the truck is "on" that pad.
   b. Workers have a relation to trucks (on or off pad) that means the worker
      is operating the truck in some capacity. Either a driver or bucket
      operator.

2. On web request, objects are loaded and sent through functions to wrap them
   in HTML template renderable objects. These objects produce draggble and
   dropzone elements. The elements include data attributes used by javascript
   to initialize dragging and dropping behavior. The data attributes include
   types to enforce what can be dropped, where.

   A form is rendered with a hidden input to capture JSON. The javascript
   updates the JSON input on initialization and after each drop event.

3. The javascript captures the state of dropzones and draggables in a recursive
   function that walks the HTML document.

   The walking function has a kind of three base cases check.

   The function recursively visits nodes, and:

   a. On a draggable element, an object is created from a data attribute of the
      element. The object will be the result of this step. Then, for each child
      of the element, the children are recursively walked for dropzone
      elements. The result object is updated from results of this secondary
      walk, if any. Finally the result object from this draggable is returned.

   b. On a "list collector" element, an object is created to contain a named
      list. The name of the list comes from data attributes of the element.
      Then, for each child of the element, it begins the top-level walk for all
      types and appends the result to the named list. Finally the result object
      is returned.

   c. On a dropzone element, an object is created from the elment's data
      attributes for the result. Then, if the elment is also a "list
      collector," the result object will contain a named list. The children of
      the element is then walked for all types of drag/drop elements. For each
      result of this secondary walking, if there is data, it is appended to the
      named list if available. If not, the result object is updated from the
      child's data. Finally the result is returned.

4. The captured, nested data is put into an input field as JSON and submitted.

5. For now, manually coded functions unwind the data into database objects and commit.
