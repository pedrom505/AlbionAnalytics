import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - thread: %(thread)-7s - %(name)-28s - %(levelname)-8s - %(message)s',
                    filename="application.log")

