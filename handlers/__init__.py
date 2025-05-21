from handlers.tasks import router as router_task
from handlers.ping import router as router_ping
from handlers.categories import router as router_category
from handlers.user import router as router_user


routers = [router_task, router_category, router_user, router_ping]
