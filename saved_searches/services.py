from .models import SavedSearch, Notification


def check_saved_searches(property):

    saved_searches = SavedSearch.objects.all()

    for saved_search in saved_searches:

        if saved_search.city:
            if saved_search.city.lower() not in property.city.lower():
                continue

        if saved_search.property_type:
            if saved_search.property_type != property.property_type:
                continue

        if saved_search.min_price is not None:
            if property.price < saved_search.min_price:
                continue

        if saved_search.max_price is not None:
            if property.price > saved_search.max_price:
                continue

        if saved_search.min_bedrooms is not None:
            if property.bedrooms < saved_search.min_bedrooms:
                continue

        Notification.objects.create(
            user=saved_search.user,
            property=property,
            saved_search=saved_search,
            message=(
                f"New property matching your saved search "
                f'"{saved_search.name}"'
            ),
        )