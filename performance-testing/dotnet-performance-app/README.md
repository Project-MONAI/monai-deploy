# Description
The dotnet-performance-app can be used for sending c-store and stow-rs requests for CT, US, MR and RF data.

## Running dotnet-performance-app
### Building the app locally

```bash
cd performance-testing/dotnet-performance-app
```

```bash
dotnet build
```

### Running as docker image
```bash
cd performance-testing/dotnet-performance-app
```

```bash
docker build -t dotnet-performance-app .
```

```bash
docker run -it --rm -p 5000:80 -p 5001:443 -e InformaticsGateway__Host={host} -e InformaticsGateway__Port={port} -e InformaticsGateway__StowPort={stowport} -e InformaticsGateway__StowUser={stowuser} -e InformaticsGateway__StowPassword={stowpassword} -e InformaticsGateway__StowWorkflowId={stowworkflowid} dotnet-performance-app
```
> **host** is to be replaced with the host that MIG is running on
> **port** is to be replaced with the port that MIG is set up to receive C-STORE request on
> **stowport** is to be replaced with the port that MIG is set up to receive STOW requests on
> **stowuser** is to be replaced with the user that is required for MIG auth. **ONLY** required if MIG auth is enabled
> **stowpassword** is to be replaced with the password that is required for MIG auth. **ONLY** required if MIG auth is enabled
> **stowworkflowid** is to be replaced with the workflow id that you want the STOW request to trigger. This is the unique ID for a workflow within Workflow Manager

Navigate to http://localhost:5000/swagger to see endpoint documentation



