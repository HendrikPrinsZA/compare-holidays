from classes.core.Model import Model

class Holiday(Model):

  attributes = [
    'id',
    'country_id',
    'date',
    'title',
    'is_on_weekend',
  ]