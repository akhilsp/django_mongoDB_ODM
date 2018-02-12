# django_mongoDB_ODM
Simple object-document-mapper (ODM) for django which maps MongoDB collections. Just a wrapper around pymongo.

##Set-up
```bash
  git clone https://github.com/akhilsp/django_mongoDB_ODM.git
  cd django_mongoDB_ODM
  pipenv install
```

## Usage
  - In your django settings file, add mongoDB configurations
  ```python
      MONGODB_URI = mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
      MONGODB_NAME = 'mongodb_database_name'
  ```
  - You can create Model mappings by creating sub-class for `BaseDocumentModel` like
  ```python
  from django_mongoDB_ODM.core.base_models import BaseDocumentModel

  class MyModel(BaseDocumentModel):
      class Meta:
          collection_name = 'my_collection' # defaults to lower case name of the class. Here, it is `mymodel`

  my_document = MyModel(data={'first_name': 'foo', 'last_name': 'bar'})
  print(my_document.data)

  my_document.save()
  print(my_document.data)
  ```
