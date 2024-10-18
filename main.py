import json
import subprocess
import jinja2

def check_environment():
    # check if docker is installed
    if subprocess.run(["docker", "--version"], stdout=subprocess.PIPE).returncode != 0:
        print("Docker is not installed. Please install Docker.")
        exit(1)
    # check if docker compose is installed
    if subprocess.run(["docker", "compose", "version"], stdout=subprocess.PIPE).returncode != 0:
        print("Docker Compose is not installed. Please install Docker Compose.")
        exit(1)


def generate_registry_server_configs(config):
    # clean up the existing directories
    subprocess.run(["rm", "-rf", "./registries/*"])
    for registry in config["registries"]:
        print(f"{registry}")
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


def generate_traefik_config(config):
    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("traefik.yml.j2")
    output = template.render(config=config)

    # Write the rendered template to the nginx directory
    with open("traefik/traefik.yml", "w") as f:
        f.write(output)

def generate_docker_compose_config(config):
    # use jinja2 to render the template file, output to docker-compose directory
    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("docker-compose.yml.j2")
    output = template.render(config=config)

    # Write the rendered template to the docker-compose directory
    with open("docker-compose.yml", "w") as f:
        f.write(output)

def docker_compose_up():
    try:
        # Run docker-compose up
        subprocess.run(["docker", "compose", "up", "-d"], check=True)
        print("Docker Compose has started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while starting Docker Compose: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

def print_green(message):
    print(f"\033[92m{message}\033[0m")

if __name__ == "__main__":
    # Replace with your domain and email
    with open("config.json", "r") as f:
        config = json.load(f)

    print_green("Checking environment...")
    check_environment()

    print_green("Generating registry server configurations...")
    generate_registry_server_configs(config)

    print_green("Generating Traefik configuration...")
    generate_traefik_config(config)

    print_green("Generating Docker Compose configuration...")
    generate_docker_compose_config(config)

    print_green("Starting Docker Compose...")
    docker_compose_up()

