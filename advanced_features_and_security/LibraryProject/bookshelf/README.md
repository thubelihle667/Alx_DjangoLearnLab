# Django Permissions and Groups Setup Guide

## Custom Permissions
Defined in `Book` model (models.py):
- can_view
- can_create
- can_edit
- can_delete

## Groups and Their Permissions
- **Viewers**: can_view
- **Editors**: can_view, can_create, can_edit
- **Admins**: All permissions

## Enforcing Permissions
Views are protected using `@permission_required` decorator in `views.py`.
Example:
```python
@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    ...
