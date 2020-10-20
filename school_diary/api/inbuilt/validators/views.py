from rest_framework import views
from rest_framework import response
from rest_framework import status
import utils


class QuarterValidator(views.APIView):
    def get(self, request):
        result: dict = {"result": True}
        quarter: str = self.request.GET.get("quarter")
        if utils.get_quarter_by_date(quarter) == 0:
            result["result"] = False
        return response.Response(result, status.HTTP_200_OK)
