# MONAI Deploy Express automated deployment on AWS

A CDK / CloudFormation project that allows the deployment of MONAI Deploy Express on EC2 in few a command lines or a few clicks ( CloudFormation UI). MONAI Deploy Express comes with a thorough installation guide, however the number of steps and the IT knowledge required to get through its deployment might be deterrant for less advanced IT users. This project enables any users to simply install MONAI Deploy Express (MDE) via a user inteface hosted in AWS CloudFormation console. Because the Infrastructure as Code (IaC) is built via CDK, more advanced users can also modifiy the python CDK code to alter the deployment to their own needs.

:warning: ** When sending DICOM data to MONAI Deploy Express over the internet:  Make sure to use only deidentified DICOM data. The MONAI Informatic Gateway component (MIG) does not support encrypted DICOM DIMSE transfer and therefore the solution deployed by this automation code is not proper to upload PHI over the internet**

## Deployment:

### Infrastructure as Code 
After the CloudFormation stack has completed you are provided with an 100% installed and functional MDE server running on AWS EC2. The server is configured for the underlaying Docker services to restart automatically upon each restart of the EC2 instance. Below is the list of actions taken by the IaC :

<table>
<th>Action</th><th>Name of resource created</th>
<tr><td>Create new VPC</td><td>MDE/mde-network/Vpc</td></tr>
<tr><td>Create a new Internet Gateway</td><td>MDE/mde-network/Vpc</td></tr>
<tr><td>Create a new SSH key used to securely connect on the MDE server by the end-user</td><td>/ec2/keypair/key-**************</td></tr>
<tr><td>Create an Elastic IP</td><td>MONAIDeployExpress-EIP</td></tr>
<tr><td>Create a public network</td><td>MDE/mde-network/Vpc/PublicSubnet1<br>MDE/mde-network/Vpc/PublicSubnet2</td></tr>
<tr><td>Create a public network</td><td>MDE/mde-network/Vpc/PublicSubnet1<br>MDE/mde-network/Vpc/PublicSubnet2</td></tr>
<tr><td>Create a new security group</td><td>MONAIDeployExpress-SG</td></tr>
<tr><td>create a new c4d.xlarge EC2 instance running ubuntu 22.04</td><td>MONAIDeployExpress</td></tr>
<tr><td>Create the default OS monaiuser account with the provided password.</td><td>--</td></tr>
<tr><td>Install MONAI deploy dependencies (python, docker , nvidia drivers and docker toolkit)</td><td>--</td></tr>
<tr><td>Install MONAI Informatic Gateway (MIG) CLI</td><td>--</td></tr>
<tr><td>Install MONAI Deploy Express binaries</td><td>--</td></tr>
<tr><td>Set the docker services to auto-restart</td><td>--</td></tr>
<tr><td>Associate the Elastic IP address with he EC2 instance</td><td>--</td></tr>
</table>

![MDE in AWS diagram](img/diagram.png)

### What remains to be done manually

#### <strong>Update the security group:</strong>
For security reason the security group associated to the EC2 instance does not allow the connection from any IP on any protocol. After the deployment is complete you need to update the security group associated with the MDE server to allow SSH and DICOM access. Follow the post installation section of this document to complete these steps.


#### <strong> Install the MDE workflows:</strong>
The MDE workflow manager service is left without any configuration after the installation, so that the user can install his own MDE workflows. you can refer to the [MONAI Dpeloy Express install guide,  Samples Workflows section](https://github.com/Project-MONAI/monai-deploy/tree/main/deploy/monai-deploy-express#sample-workflows) to install the default workflows.

## Installation

### Prerequisites 

An AWS account with the sufficient ressource availability for the creation of G4 type EC2 instance, 1 VPC and 1 elastic IP.
* G4 type EC2 instance quota limit increase can be requested in the `service quotas` menu of the AWS console, category `Amazon Elastic Compute Cloud (Amazon EC2)`->`All G and VT Spot Instance Requests`.
* VPC count limit increase can be requested in the `service quotas` menu of the AWS console, category `Amazon Virtual Private Cloud (Amazon VPC)`->`VPCs per Region`.
* Elastic IP limit increase can be requested in the `service quotas` menu of the AWS console, category `Amazon Elastic Compute Cloud (Amazon EC2)`->`EC2-VPC Elastic IPs`


There are 2 ways to deploy this solution. Users can do the [installation via Cloudformation](#installation-via-cloudformation) template or do the [installation via CDK CLI](#installation-via-cdk-cli).

### Installation via CloudFormation

1. Copy the file `MDE.template.json` from this repository root folder to your local filesystem.
2. Login to your AWS account Web console and use the top search for the "CloudFormation" service.
3. In the CloudFormation service menu, click the `[ Create Stack ]` button.
4. In the stack creation menu -> "Specify Template" section , select "upload a template file" and click the `[ Choose file ]` button. Browser to the `MDE.template.json` file copied locally at step 1, then click the `[ Next ]` button.
5. In the "Specific Stack details" menu, fill the below information, and click the `[ Next ]` button.<br>
* <strong>Stack Name:</strong> Enter "`MDE`"
* <strong>BootstrapVersion:</strong> Leave the default value.
* <strong>SsmParameterValueawsservicec***Parameter:</strong> Leave the default value.
* <strong>monaiuserpassword:</strong> Choose a password for the monaiuser linux user. This user will be part of the root group. The password needs to be 8 chars at minimum, and contain uppercase, lowercase and special characters. 
6. In the "Configure Stack Options" menu, you can add tags to all the resources to be created if you would like, then press the `[ Next ]` button.
7. In the "Review" menu, click the "`I acknowledge that AWS CloudFormation might create IAM resources.`" check and click the `[ Submit ]` button.

At this point the CloudFormation stack deployment starts and takes about 20 minutes to clomplete. You can use the refresh button in the Stacks menu at in the left side to monitor when the stack completes.

![MDE in AWS diagram](img/stack_deployment.png)
    

Once completed, refer to the [post installation tasks](#post-installation-tasks) to access to the MDE server.

### Installation via CDK CLI.

You will need the following software packages installed locally to deploy this solution via CDK.

Python3/pip: The deployment automation code is written in Python.
AWS CDK: Please refer to [CDK documentation](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) to install the framework and bootstrap your AWS environment.

1. Bootstrap the AWS account for CDK. Refer to the CDK documentation  [Bootstrapping](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html#:~:text=to%20do%20that.-,Bootstrapping,-Deploying%20stacks%20with) section to know more about bootstrapping your AWS account for CDK.

2. Clone this repository. You can either download and unzip the package from the repository webite, or use the git clone command.

3. **In the cloned directory**, create a virtualenv for Python. Virtual environment is needed to deploy required versions of packages:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

4. Deploy the stack via CDK:

```
$ cdk deploy --parameters monaiuserpassword=[your monai user password]
```

to the question `Do you wish to deploy these changes (y/n)?` press Y and Enter.


The deployment takes approximately 20 minutes. Once completed, refer to the [post installation tasks](#post-installation-tasks) to access to the MDE server.

## Post deployment tasks

After the installation has completed, 2 steps remain to be done. 1st the security group associated with the MDE server needs to be updated with the IP address of the SSH and DICOM client(s). 2nd, Your SSH client has to be configured to use a specific SSH key to connect to the server.

### Configuring the Security Group for SSH and DICOM access

Follow the steps below to add inbound rules in the MDE security group:

1. Logon the AWS Web Console with the same account as the one used for the deployment of the server, and within the same region.
2. In the AWS Web Console select the `EC2` service.
3. In the EC2 service left menu bar, select `Security Groups`.
4. In the Security Group list, select the group named `MONAIDeployExpress-SG` and click `[ Actions -> Edit inboudn rules ]`. 
5. In the `Edit inbound rules` menu, Update the `Source` field for each rule and select `My IP`. These rules will allow any machine going on the public network via the listed IP address to connect to the SSH port (This is not sufficient to logon the server though, the server remains only accessible to owners of the SSH key).
![MDE in AWS diagram](img/security_group.png)
<strong>Note:</strong> Usage of web proxies can bias the detection of the user public IP in the security group rules editing menu. If you are using a web proxy to access to the internet, ensure that the IP automatically added in the source field is the one your computer uses to communicate on the internet for non-HTTP protocols.

### Connecting on the server via SSH
A SSH key is required to connect to the MDE server. in the EC2 console->Key pair menu, you will find that a key pair called 'MonaiDeployExpress' has been created during the deployment. However key pairs can only be downloaded 1 time upon their creation, and it is not possible to download this key pair anymore from this menu. Instead the Cloudformation/CDK deployment exports the key pair and saves it in `parameter Store`, a component of the `AWS Systems Manager` service. Follow the below steps to download the SSH key: 

1. Logged in the AWS console with the same account and in the same region as used for the deployment, in the search field at the top of the console, search for `Parameter Store`.
2. in the `Parameter Store` menu, select the parameter called `/ec2/keypair/key-*********` and click the `[ View details ]` button.
3. In the details menu, click on the `show` link at the bottom left of the details pane. the Certificate key displays.
4. Copy the certificate key, from  the tag `-----BEGIN RSA PRIVATE KEY-----` to the tag `-----END RSA PRIVATE KEY-----`, tags included, and paste the the copied content in a new file named `mde-server.pem` on your local filesystem.

This pem file will be used to connect to the MDE server via SSH. Note that authentication by SSH key is the only authentication enabled by default on the MDE server.

5. In the AWS Web Console search field ( top menu bar ), search for the `EC2 service`. In the EC2 service left menu bar, select `Elastic IPs`. In the Elastic IPs list, note down the IP address for the `Elastic IP` named `MONAIDeployExpress-EIP`. This Elastic IP is attached to the MDE server and we will be used to connect to the server via SSH.

6. The methods to connect on the MDE server may change from one SSH client to another. Follow the AWS documentation about how to [Connect to your Linux instance from Windows using PuTTY](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html) to learn how to convert the `mde-server.pem` key file to a .ppk file and configure your Putty session with. Configure the EC2 instance IP address with the Elastic IP noted in the step above.

7. When ready to connect to the MDE server, use the Elastic IP as the hostname , and `ubuntu` as the user. Once logged in the MDE server, type the command `su - monaiuser` to switch to the monaiuser user.