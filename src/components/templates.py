import jinja2


def get_template(config):
    template_loader = jinja2.FileSystemLoader(searchpath=config.FRONTEND_PATH)
    template_env = jinja2.Environment(loader=template_loader)
    return template_env.get_template("index.html")
