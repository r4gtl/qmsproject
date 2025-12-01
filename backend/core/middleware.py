from django.utils.deprecation import MiddlewareMixin
from .models import set_current_company


class CompanyMiddleware(MiddlewareMixin):
    """
    Middleware to set the current company in thread-local storage.

    This makes the company available throughout the request lifecycle,
    enabling automatic filtering of company-owned models.
    """

    def process_request(self, request):
        """
        Extract company from the authenticated user's profile
        and set it in thread-local storage.
        """
        company = None

        if request.user and request.user.is_authenticated:
            try:
                # Get company from user's profile
                if hasattr(request.user, 'profile'):
                    company = request.user.profile.company
                    request.company = company  # Also attach to request for easy access
            except Exception as e:
                # Handle case where profile doesn't exist
                print(f"Error getting company for user {request.user}: {e}")
                company = None

        # Set in thread-local storage
        set_current_company(company)

    def process_response(self, request, response):
        """
        Clean up thread-local storage after request
        """
        set_current_company(None)
        return response
