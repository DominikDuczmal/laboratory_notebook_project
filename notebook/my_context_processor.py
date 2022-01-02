from django.utils import timezone
import django

def my_cp(request):
  """My custom context processor with a list of current app version and Date & Time"""

  ctx = {
    "now": django.utils.timezone.now(),
    "version": "1.0",
  }
  return ctx
