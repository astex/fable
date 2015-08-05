from app import create_app

with create_app('config.py').app_context():
    try:
        import IPython
        shell = IPython.embed()
        shell(ns_locals=locals())
    except ImportError:
        import code
        code.interact(local=locals())
