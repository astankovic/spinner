from .server import webserver
import get_data

if __name__ == '__main__':
    # instantiate pools
    meridian_pool = get_data.GamesPool()

    # start web server
    webServer = webserver.WebApp(meridian_pool.pool)
    webServer.app.run(debug=False, port=8181)

    meridian_pool.start()