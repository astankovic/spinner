from server import webserver
from threading import Thread
import get_data

if __name__ == '__main__':
    # instantiate pools
    meridian_pool = get_data.GamesPool()
    t1 = Thread(target=meridian_pool.start)
    # start web server
    webServer = webserver.WebApp(meridian_pool.pool)
    t2 = Thread(target=webServer.app.run, kwargs={'debug': False, 'port': 8181})
    t2.start()
    t1.start()
