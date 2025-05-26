from handlers.auth import router as router_auth
from handlers.categories import router as router_category
from handlers.ping import router as router_ping
from handlers.tasks import router as router_task
from handlers.user import router as router_user

routers = [router_task, router_category, router_user, router_auth, router_ping]
