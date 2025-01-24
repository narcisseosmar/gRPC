import grpc
from concurrent import futures
import subprocess
import deployer_pb2
import deployer_pb2_grpc

class Deployer(deployer_pb2_grpc.DeployerServicer):
    def DeployLaravelApp(self, request, context):
        repo_url = request.repo_url
        branch = request.branch
        server_ip = request.server_ip
        ssh_user = request.ssh_user
        ssh_key_path = request.ssh_key_path

        try:
            # Script de déploiement
            deploy_script = f"""
            ssh -i {ssh_key_path} {ssh_user}@{server_ip} << 'EOF'
            git clone -b {branch} {repo_url} /var/www/laravel-app
            cd /var/www/laravel-app
            cp .env.example .env
            composer install --no-dev --optimize-autoloader
            php artisan key:generate
            php artisan migrate --force
            chown -R www-data:www-data /var/www/laravel-app
            chmod -R 755 /var/www/laravel-app
            EOF
            """
            subprocess.run(deploy_script, shell=True, check=True)
            return deployer_pb2.DeployResponse(success=True, message="Déploiement réussi !")
        except subprocess.CalledProcessError as e:
            return deployer_pb2.DeployResponse(success=False, message=f"Erreur lors du déploiement : {e}")

    def MonitorDeployment(self, request, context):
        server_ip = request.server_ip
        try:
            # Vérifier si le projet est déployé
            check_script = f"ssh {server_ip} 'ls /var/www/laravel-app'"
            subprocess.run(check_script, shell=True, check=True)
            return deployer_pb2.MonitorResponse(status="Déployé", details="Le projet Laravel est déployé.")
        except subprocess.CalledProcessError:
            return deployer_pb2.MonitorResponse(status="Non déployé", details="Le projet Laravel n'est pas déployé.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    deployer_pb2_grpc.add_DeployerServicer_to_server(Deployer(), server)
    server.add_insecure_port('[::]:50051')
    print("Serveur gRPC démarré sur le port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()