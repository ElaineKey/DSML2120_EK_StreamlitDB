"""All calculations live here so the UI stays thin. Each function takes a
(filtered) dataframe and returns numbers or a dataframe."""
import pandas as pd

FUNNEL_STEPS = ["sessions", "product_views", "add_to_cart", "checkouts", "purchases"]

STEP_RATES = {
    "view_rate": ("product_views", "sessions"),
    "cart_rate": ("add_to_cart", "product_views"),
    "checkout_rate": ("checkouts", "add_to_cart"),
    "purchase_rate": ("purchases", "checkouts"),
}


