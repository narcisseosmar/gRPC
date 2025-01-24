import grpc
from concurrent import futures
import app_manager_pb2
import app_manager_pb2_grpc

# Simuler une base de données pour les applications et leur statut
apps_db = {}

class AppManager(app_manager_pb2_grpc.AppManagerServicer):
    def DeployApp(self, request, context):
        app_name = request.app_name
        if app_name in apps_db:
            return app_manager_pb2.DeployAppResponse(
                success=False,
                message=f"L'application {app_name} est déjà déployée."
            )
        apps_db[app_name] = {
            "version": request.version,
            "config": request.config,
            "status": "Déployé"
        }
        return app_manager_pb2.DeployAppResponse(
            success=True,
            message=f"L'application {app_name} a été déployée avec succès."
        )

    def MonitoringStatus(self, request, context):
        app_name = request.app_name
        if app_name in apps_db:
            return app_manager_pb2.MonitoringStatusResponse(
                status=apps_db[app_name]["status"],
                details=f"Statut de {app_name}: {apps_db[app_name]['status']}"
            )
        else:
            return app_manager_pb2.MonitoringStatusResponse(
                status="Non trouvé",
                details=f"L'application {app_name} n'existe pas."
            )

    def ConfigureService(self, request, context):
        app_name = request.app_name
        if app_name in apps_db:
            apps_db[app_name]["config"] = request.config
            return app_manager_pb2.ConfigureServiceResponse(
                success=True,
                message=f"La configuration de {app_name} a été mise à jour."
            )
        else:
            return app_manager_pb2.ConfigureServiceResponse(
                success=False,
                message=f"L'application {app_name} n'existe pas."
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    app_manager_pb2_grpc.add_AppManagerServicer_to_server(AppManager(), server)
    server.add_insecure_port('[::]:50051')
    print("Serveur gRPC démarré sur le port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()