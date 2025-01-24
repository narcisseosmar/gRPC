import grpc
import app_manager_pb2
import app_manager_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = app_manager_pb2_grpc.AppManagerStub(channel)

        # Déployer une application
        deploy_response = stub.DeployApp(app_manager_pb2.DeployAppRequest(
            app_name="MyApp",
            version="1.0.0",
            config="config.json"
        ))
        print(f"Déploiement de l'application : {deploy_response.message}")

        # Surveiller le statut de l'application
        status_response = stub.MonitoringStatus(app_manager_pb2.MonitoringStatusRequest(
            app_name="MyApp"
        ))
        print(f"Statut de l'application : {status_response.status}, Détails : {status_response.details}")

        # Configurer le service
        configure_response = stub.ConfigureService(app_manager_pb2.ConfigureServiceRequest(
            app_name="MyApp",
            config="new_config.json"
        ))
        print(f"Configuration du service : {configure_response.message}")

if __name__ == '__main__':
    run()