import grpc
import deployer_pb2
import deployer_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = deployer_pb2_grpc.DeployerStub(channel)

        # Déployer une application Laravel
        deploy_response = stub.DeployLaravelApp(deployer_pb2.DeployRequest(
            repo_url="https://github.com/votre-repo/laravel-app.git",
            branch="main",
            server_ip="192.168.1.100",
            ssh_user="ubuntu",
            ssh_key_path="/path/to/ssh/key.pem"
        ))
        print(f"Résultat du déploiement : {deploy_response.message}")

        # Surveiller le déploiement
        monitor_response = stub.MonitorDeployment(deployer_pb2.MonitorRequest(
            server_ip="192.168.1.100"
        ))
        print(f"Statut du déploiement : {monitor_response.status}, Détails : {monitor_response.details}")

if __name__ == '__main__':
    run()