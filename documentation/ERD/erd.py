from graphviz import Digraph

# Create a new directed graph
erd_detailed = Digraph(comment='Event Supply Rental Website ERD', format='png')
erd_detailed.attr(rankdir='LR', fontsize='24')

# Define entities (tables)
entities = {
    "User": [
        "id (PK, INT)", "username (VARCHAR)", "email (VARCHAR)",
        "password (VARCHAR)", "is_staff  (INT)", "is_admin  (INT)",
        "social_auth_provider (VARCHAR)", "created (DATETIME)"
    ],
    "Profile": [
        "id (PK, INT)", "user_id (FK, INT)",
        "phone_number (VARCHAR)"
    ],
    "Address": [
        "id (PK, INT)", "user_id (FK, INT)", "street (VARCHAR)",
        "city (VARCHAR)", "postal_code (VARCHAR)",
        "town_or_city (VARCHAR)", "street_address1 (VARCHAR)",
        "street_address2 (VARCHAR)", "county (VARCHAR)",
        "country (COUNTRYFIELD)", "is_default (BOOL)",
        "type (INT)", "created_on (DATETIME)"
    ],
    "Category": [
        "id (PK, INT)", "name (VARCHAR)", "parent_id (FK, INT)"
        "slug (VARCHAR)", "created_on (DATETIME)"
    ],
    "Supply": [
        "id (PK, INT)", "name (VARCHAR)", "sku (VARCHAR)",
        "category_id (FK, INT)", "description (VARCHAR)",
        "quantity_available (INT)", "price_per_day (DECIMAL)",
        "created_on (DATETIME)"
    ],
    "Supply Image": [
        "id (PK, INT)", "supply_id (FK, INT)",
        "image_url (Urlfield)", "image (ImageField)", "created_on (DATETIME)"
    ],
    "Order": [
        "id (PK, INT)", "order_number (VARCHAR)", "profile_id (FK, INT)",
        "billing_address_id (FK, INT)", "delivery_address_id (FK, INT)",
        "full_name (VARCHAR)", "email (VARCHAR)",
        "phone_number (VARCHAR)", "order_total (DECIMAL)",
        "grand_total (DECIMAL)", "delivery_cost (DECIMAL)",
        "original_bag (TEXT)", "stripe_pid (VARCHAR)"
        "status (INT)", "created_on (DATETIME)"
    ],
    "Order Item": [
        "id (PK, INT)", "order_id (FK, INT)", "supply_id (FK, INT)",
        "quantity (INT)", "rental_start_date (DATETIME)",
        "renting_days (INT)", "price_per_day (DECIMAL)",
        "lineitem_total (DECIMAL)", "created_on (DATETIME)"
    ],
    "Saved Item": [
        "id (PK, INT)", "user_id (FK, INT)", "supply_id (FK, INT)",
        "created (DATETIME)"
    ],
    "Review": [
        "id (PK, INT)", "user_id (FK, INT)", "supply_id (FK, INT)",
        "rating (INT)", "comment (VARCHAR)", "created_at (DATETIME)"
    ]
}

# Add nodes
for entity, fields in entities.items():
    label = "<<TABLE BORDER='0' CELLBORDER='1' CELLSPACING='0'>"
    match entity:
        case "Supply" | "Supply Image" | "Review" | "Saved Item" | "Address":
            label += f"<TR><TD BGCOLOR='green'><B>{entity}</B></TD></TR>"
        case _:
            label += f"<TR><TD BGCOLOR='lightblue'><B>{entity}</B></TD></TR>"
    for field in fields:
        label += f"<TR><TD ALIGN='LEFT'>{field}</TD></TR>"
    label += "</TABLE>>"
    erd_detailed.node(entity, label=label, shape='plain')

# Define relationships
relationships = [
    ("Profile", "User"),
    ("Address", "User"),
    ("Saved Item", "User"),
    ("Saved Item", "Supply"),
    ("Supply", "Category"),
    ("Category", "Category"),
    ("Supply Image", "Supply"),
    ("Order", "Profile"),
    ("Order", "Address"),  # billing
    ("Order", "Address"),  # delivery
    ("Order Item", "Order"),
    ("Order Item", "Supply"),
    ("Review", "User"),
    ("Review", "Supply")
]

# Add edges
for child, parent in relationships:
    erd_detailed.edge(child, parent)

# Render the diagram
erd_detailed.render('event-supply-rental-erd', cleanup=True)
