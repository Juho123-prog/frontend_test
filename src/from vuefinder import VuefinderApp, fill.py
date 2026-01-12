import os
import sys
import logging

from vuefinder import VuefinderApp, fill_fs
from fs.memoryfs import MemoryFS
from fs.wrap import WrapReadOnly
from fs.osfs import OSFS
from werkzeug.serving import run_simple
from werkzeug.wrappers import Response
from werkzeug.middleware.dispatcher import DispatcherMiddleware

def health_app(environ, start_response):
    response = Response(
        '{"status":"ok"}',
        status=200,
        content_type="application/json",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )
    return response(environ, start_response)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("vuefinder_server")

if __name__ == "__main__":
    print("Starting vuefinder server")
    logger.info("Starting vuefinder server")
    app = VuefinderApp(enable_cors=True)

    # default adapter
    memfs = MemoryFS()
    fill_fs(memfs, {"README.txt": "Your adapter is being ready!"})
    app.add_fs("default", WrapReadOnly(memfs))

    try:
        # change folder
        os.chdir("C:/Users/AIMedical/Desktop/test")
        #print only directories' name on this current folder
        folder_list = [name for name in os.listdir(".") if os.path.isdir(name)]
        print("folder list: ", folder_list)
        logger.info(f"folder list: {folder_list}")
    except Exception:
        logger.exception("Failed to prepare file systems")

    for directory in folder_list:
        app.add_fs(directory, OSFS(f"{directory}/"))

    # vuefinder + health endpoint 결합
    application = DispatcherMiddleware(app, {
        "/health": health_app
    })
    run_simple("0.0.0.0", 8005, application, use_debugger=True, use_reloader=False)


