import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from pymongo import MongoClient


class DocumentModelType(type):
    """
    Class-factory for Document model
    """
    def __init__(cls, name, bases, attrs):
        super(DocumentModelType, cls).__init__(name, bases, attrs)
        cls._collection = cls.get_collection()


class BaseDocumentModel(metaclass=DocumentModelType):
    """
    Abstract base model for MongoDB
    """
    _pre_save_hooks = []
    _connection = MongoClient(settings.MONGODB_URI)
    _collection = _connection
    validate_fields = True
    fields = {}

    def __init__(self, data, validate_fields=True, validators=list()):
        self.data = data
        self.validate_fields = validate_fields
        self.validation_errors = {}
        self._pre_save_hooks = validators
        self._id = data.get('_id')

    @classmethod
    def get_collection(cls):
        """
        Returns collection corresponding to the class.
        """
        return cls._connection[settings.MONGODB_NAME][cls._get_collection_name()]

    @classmethod
    def _get_collection_name(cls):
        """
        Returns name of the mongodb collection which is mapped by the class.
        defaults to lowercase name of the class
        """
        return cls.Meta.collection_name if cls.Meta.collection_name\
            else cls.__name__.lower()

    def validate_data_type(self):
        """
        Validate fields and their type
        :return: True if data valid
        """
        if self.validate_fields:
            for key, value in self.data.items():
                validator = self.fields.get(key)
                if validator and not self.validate_field_type(value, validator):
                    print(value, validator)
                    return False
        return True

    def validate_field_type(self, value, validator):
        """
        Method to check the value type
        :param value: Value
        :param validator: Expected type of the value
        :return: True if valid else False
        """
        try:
            if isinstance(value, validator):
                return True
            else:
                self.validation_errors[value] = 'Invalid data'
        except:
            pass
        return False

    def validate(self):
        """
        Applies additional validations on entity object.
        :return:True if valid else False
        """
        for hook in self._pre_save_hooks:
            try:
                hook(self)
            except ValidationError as e:
                self.validation_errors.update(e.args[0])
        return False if self.validation_errors else True

    def is_valid(self):
        """
        Method to call both type validation and custom validation
        :return: True if valid else False
        """
        return bool(self.validate_data_type() and self.validate())

    def save(self):
        """
        Method to save the document
        """
        self.validate()
        if self._id:
            self.update()
        else:
            self.create()

    def update(self):
        """
        Updates existing document
        """
        self.data["updated_at"] = datetime.datetime.utcnow()
        self._collection.update_one(
            {"_id": self.data["_id"]},
            {"$set": self.data},
            upsert=False
        )

    def create(self):
        """
        Method to create a new document
        """
        self.data["created_at"] = datetime.datetime.utcnow()
        self.data["updated_at"] = datetime.datetime.utcnow()
        self._collection.insert_one(self.data)  # `self.data` will be updated with key `_id`
        self._id = self.data["_id"]

    class Meta:
        """
        Meta field descriptions are set here
        """
        collection_name = None
