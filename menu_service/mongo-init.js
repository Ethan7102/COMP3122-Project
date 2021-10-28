db.auth('project', 'pass')
db = db.getSiblingDB('menu_db')

db.createCollection('menu');

db.menu.insertOne({
    "store_id": "c123",
    "store_name": "Shop One",
    "items": [
      {
        "id": "Coffee",
        "description": {
          "translations": {
            "en_us": "Deliciously roasted beans"
          }
        },
        "title": {
          "translations": {
            "en_us": "Coffee"
          }
        },
        "quantity_info": {},
        "external_data": "External data for coffee",
        "modifier_group_ids": {
          "ids": [
            "Add-milk",
            "Add-sugar"
          ]
        },
        "price_info": {
          "price": 300
        },
        "tax_info": {
          "tax_rate": 8
        }
      },
      {
        "id": "Blueberry",
        "title": {
          "translations": {
            "en_us": "Blueberry"
          }
        },
        "quantity_info": {
          "overrides": [
            {
              "context_type": "MODIFIER_GROUP",
              "context_value": "Choose-flavor",
              "quantity": {
                "max_permitted": 1
              }
            }
          ]
        },
        "external_data": "External data for blueberry flavor",
        "price_info": {
          "price": 5,
          "overrides": [
            {
              "context_type": "MODIFIER_GROUP",
              "context_value": "Choose-flavor",
              "price": 0
            }
          ]
        },
        "tax_info": {
          "tax_rate": 8
        }
      },
      {
        "id": "Muffin",
        "description": {
          "translations": {
            "en_us": "Great for afternoon snack time!"
          }
        },
        "title": {
          "translations": {
            "en_us": "Fresh-baked muffin"
          }
        },
        "external_data": "External data for muffin",
        "modifier_group_ids": {
          "ids": [
            "Choose-flavor"
          ]
        },
        "price_info": {
          "price": 300
        },
        "tax_info": {
          "tax_rate": 8
        }
      },
      {
        "id": "Sugar",
        "title": {
          "translations": {
            "en_us": "Sugar"
          }
        },
        "quantity_info": {
          "overrides": [
            {
              "context_type": "MODIFIER_GROUP",
              "context_value": "Add-sugar",
              "quantity": {
                "max_permitted": 2
              }
            }
          ]
        },
        "external_data": "External data for sugar",
        "price_info": {
          "price": 2,
          "overrides": [
            {
              "context_type": "MODIFIER_GROUP",
              "context_value": "Add-sugar",
              "price": 0
            }
          ]
        },
        "tax_info": {
          "tax_rate": 8
        }
      },
      {
        "id": "Chocolate-deluxe",
        "title": {
          "translations": {
            "en_us": "Chocolate deluxe"
          }
        },
        "quantity_info": {
          "overrides": [
            {
              "context_type": "MODIFIER_GROUP",
              "context_value": "Choose-flavor",
              "quantity": {
                "max_permitted": 1
              }
            }
          ]
        },
        "external_data": "External data for chocolate deluxe flavor",
        "price_info": {
          "price": 100,
          "overrides": [
            {
              "context_type": "MODIFIER_GROUP",
              "context_value": "Choose-flavor",
              "price": 50
            }
          ]
        },
        "tax_info": {
          "tax_rate": 8
        },
      },
      {
        "id": "Milk",
        "title": {
          "translations": {
            "en_us": "Milk"
          }
        },
        "quantity_info": {
          "overrides": [
            {
              "context_type": "MODIFIER_GROUP",
              "context_value": "Add-milk",
              "quantity": {
                "max_permitted": 1
              }
            }
          ]
        },
        "external_data": "External data for milk",
        "price_info": {
          "price": 0,
          "overrides": [
            {
              "context_type": "MODIFIER_GROUP",
              "context_value": "Add-milk",
              "price": 0
            }
          ]
        },
        "tax_info": {
          "tax_rate": 8
        }
      },
      {
        "id": "Tea",
        "description": {
          "translations": {
            "en_us": "A soothing cuppa"
          }
        },
        "title": {
          "translations": {
            "en_us": "Tea"
          }
        },
        "quantity_info": {},
        "external_data": "External data for tea",
        "modifier_group_ids": {
          "ids": [
            "Add-milk",
            "Add-sugar"
          ]
        },
        "price_info": {
          "price": 250
        },
        "tax_info": {
          "tax_rate": 8
        }
      },
      {
        "id": "Chicken-sandwich",
        "description": {
          "translations": {
            "en_us": "Whole grain bread, grilled chicken and salad"
          }
        },
        "title": {
          "translations": {
            "en_us": "Chicken sandwich"
          }
        },
        "external_data": "External data for chicken sandwich",
        "price_info": {
          "price": 700
        },
        "tax_info": {
          "tax_rate": 8
        }
      }
    ],
    "display_options": {
      "disable_item_instructions": true
    },
    "menus": [
      {
        "service_availability": [
          {
            "time_periods": [
              {
                "start_time": "00:00",
                "end_time": "23:59"
              }
            ],
            "day_of_week": "monday"
          },
          {
            "time_periods": [
              {
                "start_time": "00:00",
                "end_time": "23:59"
              }
            ],
            "day_of_week": "tuesday"
          },
          {
            "time_periods": [
              {
                "start_time": "00:00",
                "end_time": "23:59"
              }
            ],
            "day_of_week": "wednesday"
          },
          {
            "time_periods": [
              {
                "start_time": "00:00",
                "end_time": "23:59"
              }
            ],
            "day_of_week": "thursday"
          },
          {
            "time_periods": [
              {
                "start_time": "00:00",
                "end_time": "23:59"
              }
            ],
            "day_of_week": "friday"
          },
          {
            "time_periods": [
              {
                "start_time": "00:00",
                "end_time": "23:59"
              }
            ],
            "day_of_week": "saturday"
          },
          {
            "time_periods": [
              {
                "start_time": "00:00",
                "end_time": "23:59"
              }
            ],
            "day_of_week": "sunday"
          }
        ],
        "category_ids": [
          "Sandwiches",
          "Snacks",
          "Drinks"
        ],
        "id": "All-day",
        "title": {
          "translations": {
            "en_us": "All day"
          }
        }
      }
    ],
    "categories": [
      {
        "entities": [
          {
            "type": "ITEM",
            "id": "Muffin"
          }
        ],
        "id": "Snacks",
        "title": {
          "translations": {
            "en_us": "Snacks"
          }
        }
      },
      {
        "entities": [
          {
            "type": "ITEM",
            "id": "Chicken-sandwich"
          }
        ],
        "id": "Sandwiches",
        "title": {
          "translations": {
            "en_us": "Sandwiches"
          }
        }
      },
      {
        "entities": [
          {
            "type": "ITEM",
            "id": "Coffee"
          },
          {
            "type": "ITEM",
            "id": "Tea"
          }
        ],
        "id": "Drinks",
        "title": {
          "translations": {
            "en_us": "Drinks"
          }
        }
      }
    ],
    "modifier_groups": [
      {
        "quantity_info": {
          "quantity": {
            "max_permitted": 2
          }
        },
        "title": {
          "translations": {
            "en_us": "Add sugar"
          }
        },
        "external_data": "External data for sugar choice",
        "modifier_options": [
          {
            "type": "ITEM",
            "id": "Sugar"
          }
        ],
        "display_type": null,
        "id": "Add-sugar"
      },
      {
        "quantity_info": {
          "quantity": {
            "max_permitted": 1,
            "min_permitted": 1
          }
        },
        "title": {
          "translations": {
            "en_us": "Choose flavor"
          }
        },
        "external_data": "External data for muffin flavor choice",
        "modifier_options": [
          {
            "type": "ITEM",
            "id": "Blueberry"
          },
          {
            "type": "ITEM",
            "id": "Chocolate-deluxe"
          }
        ],
        "id": "Choose-flavor"
      },
      {
        "quantity_info": {
          "quantity": {
            "max_permitted": 1
          }
        },
        "title": {
          "translations": {
            "en_us": "Add milk"
          }
        },
        "external_data": "External data for milk choice",
        "modifier_options": [
          {
            "type": "ITEM",
            "id": "Milk"
          }
        ],
        "id": "Add-milk"
      }
    ]
  });
