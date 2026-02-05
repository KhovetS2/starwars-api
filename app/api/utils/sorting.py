"""Sorting utilities for API routes."""

from typing import Any, Dict, List, Optional


def sort_results(
    results: List[Dict[str, Any]],
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
    numeric_fields: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """Sort a list of dictionaries by a given field.
    
    Args:
        results: List of dictionaries to sort
        sort_by: Field name to sort by (None = no sorting)
        sort_order: 'asc' for ascending, 'desc' for descending
        numeric_fields: List of field names that should be sorted as numbers
        
    Returns:
        Sorted list of dictionaries
    """
    if not sort_by or not results:
        return results
    
    numeric_fields = numeric_fields or []
    reverse = sort_order == "desc"
    
    def sort_key(item: Dict[str, Any]) -> Any:
        value = item.get(sort_by, "")
        
        # Handle None or "unknown" values
        if value is None or value == "unknown" or value == "n/a":
            # Put unknowns at end for asc, beginning for desc
            return (1, "") if not reverse else (0, "")
        
        # Handle numeric fields
        if sort_by in numeric_fields:
            try:
                # Remove commas from numbers like "1,000"
                if isinstance(value, str):
                    value = value.replace(",", "")
                return (0, float(value))
            except (ValueError, TypeError):
                # Non-numeric value, put at end
                return (1, "") if not reverse else (0, "")
        
        # Handle string fields
        return (0, str(value).lower())
    
    return sorted(results, key=sort_key, reverse=reverse)
