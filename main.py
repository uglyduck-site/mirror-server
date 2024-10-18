import json
import subprocess
import jinja2

def apply_ssl_certificate(config):
    try:
        domain = config["domain"]
        email = config["email"]
        # Certbot command to apply for a certificate using standalone mode
        command = [
            "certbot", "certonly",
            "--standalone",
            "--non-interactive",
            "--agree-tos",
            "--email", email,
            "-d", domain,
            "--config-dir", f"./nginx/ssl/config",
            "--logs-dir", f"./nginx/ssl/logs",
            "--work-dir", f"./nginx/ssl/work"
        ]

        # Run the certbot command
        subprocess.run(command, check=True)
        print(f"SSL certificate for {domain} has been successfully applied.")
    except subprocess.CalledProcessError as e:
        print(f"Error while applying for SSL certificate: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

def generate_registry_server_configs(config):
    for registry in config["registries"]:
        # Create directory for the registry
        subprocess.run(["mkdir", "-p", f'registries/{registry}/data'])

        # use jinja2 to render the template file, output to registry directory
        template_loader = jinja2.FileSystemLoader(searchpath="./templates")
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template("config.yml.j2")
        output = template.render(registry=registry)

        # Write the rendered template to the registry directory
        with open(f"registries/{registry}/config.yml", "w") as f:
            f.write(output)

def generate_nginx_config(config):
    # use jinja2 to render the template file, output to nginx directory
    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("mirrors.conf.j2")
    output = template.render(config)

    # Write the rendered template to the nginx directory
    with open("nginx/conf.d/mirrors.conf", "w") as f:
        f.write(output)

def generate_docker_compose_config(config):
    # use jinja2 to render the template file, output to docker-compose directory
    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("docker-compose.yml.j2")
    output = template.render(config)

    # Write the rendered template to the docker-compose directory
    with open("docker-compose.yml", "w") as f:
        f.write(output)

if __name__ == "__main__":
    # Replace with your domain and email
    with open("config.json", "r") as f:
        config = json.load(f)

    apply_ssl_certificate(config)
    generate_registry_server_configs(config)
    generate_nginx_config(config)
    generate_docker_compose_config(config)


