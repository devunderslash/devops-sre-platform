Registry - https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest

Kubeconfig - aws eks update-kubeconfig --region us-east-1 --name dev-eks-cluster --kubeconfig ~/.kube/config

patch to add an ALB - kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'

The above command will add the LoadBalancer type to the argocd-server service. This will create an AWS Application Load Balancer (ALB) and expose the ArgoCD UI to the internet. You can get the DNS name of the ALB by running the following command:

kubectl get svc argocd-server -n argocd -o json | jq --raw-output '.status.loadBalancer.ingress[0].hostname'

store dns in variable - export ARGOCD_SERVER=`kubectl get svc argocd-server -n argocd -o json | jq --raw-output '.status.loadBalancer.ingress[0].hostname'`

Resource - https://medium.com/@chauhanhimani512/install-argocd-on-the-eks-cluster-and-configure-sync-with-the-github-manifest-repository-9e3d62e1c093


Add this to TF setup for Vault - 
eksctl create addon --name aws-ebs-csi-driver --cluster <CLUSTER_NAME> --service-account-role-arn arn:aws:iam::<AWS_ACCOUNT_NUMBER>:role/AmazonEKS_EBS_CSI_DriverRole --force

Add LB for argocd DNS to terraform (confirm this is the best way to do this)
