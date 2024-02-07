AKS&ArgoCDのインストール
---
### 目次
- [AKSのインストール設定](#AKSのインストール設定)
- [ArgoCDのインストール設定](#ArgoCDのインストール設定)
### AKSのインストール設定
#### ①リソース グループ作成
```
az group create --name saas-core --location japaneast
```
#### ②AKSクラスター作成
```
az aks create -g saas-core -n saas-cluster --enable-managed-identity --node-count 1 --enable-addons monitoring --generate-ssh-keys
az aks enable-addons --addons azure-keyvault-secrets-provider --name saas-cluster --resource-group saas-core
```
#### ③マネージドID作成
```
az identity create --resource-group saas-core --name saas-cluster-mnid
```
#### ④作成されたマネージドIDに権限付与
--assignee マネージドIDのクライアントID
--scope 権限のスコープ
```
az role assignment create --role "Contributor" --assignee "69ab9774-6317-4963-90b4-aea06d941ebd" --scope /subscriptions/a849fbfa-c9d9-4fe3-b47f-60a4fa01253a
```
#### ⑤作成されたマネージドIDにアクセスポリシーの設定
```
az keyvault set-policy -n kv-saas-core --key-permissions get list --secret-permissions get list --certificate-permissions get list --object-id 69ab9774-6317-4963-90b4-aea06d941ebd
```
#### ⑥provider register の設定
```
az extension add --name aks-preview
az extension update --name aks-preview
az feature register --namespace "Microsoft.ContainerService" --name "EnablePodIdentityPreview"
az provider register --namespace Microsoft.ContainerService
```
#### ⑦クラスターの適用
```
az aks update -g saas-core -n saas-cluster --enable-pod-identity --enable-pod-identity-with-kubenet
```
#### ⑧PodIdentityの作成<br/>
参照ページ：https://learn.microsoft.com/ja-jp/azure/aks/use-azure-ad-pod-identity<br/>
※ ポッドに AzureIdentityBinding のセレクターと一致する値が指定された aadpodidbinding ラベルが必要です。<br/>
　 既定では、セレクターはポッドマネージド ID の名前（<font color="red">saas-pod-identity</font>）と一致しますが、<br/>
　 --binding-selector オプションを使用して設定することもできます。
```
az identity show -g saas-core -n saas-cluster-mnid --query id -otsv　⇒　出力内容を下記のidentity-resource-idに置き換える
az aks pod-identity add --resource-group saas-core --cluster-name saas-cluster --namespace saas-core  --name saas-pod-identity --identity-resource-id /subscriptions/a849fbfa-c9d9-4fe3-b47f-60a4fa01253a/resourcegroups/MC_saas-core_saas-cluster_japaneast/providers/Microsoft.ManagedIdentity/userAssignedIdentities/saas-cluster-agentpool
```
#### ⑨ACRの作成
作成した後、ACRにイメージの格納も必要
```
az acr create --resource-group saas-core --name djpsaascoreacr --sku Basic
az aks update -n saas-cluster -g saas-core --attach-acr djpsaascoreacr
```
#### ⑩nginx-tlsのインストール
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml
kubectl create secret tls test-tls --key="tls.key" --cert="tls.crt" -n saas-core

※自己証明書の作成
　openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=www.saas-core-platform.com"
```
### ArgoCDのインストール＆設定
#### ①Argo CDのインストール
```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
※argocd-serverのDepolymentを編集し、「--insecure」をargsに追加する
```
#### ②argocd-serverをLoadBalancerに変更する
```
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'　または　kubectl edit svc argocd-server -n argocd
※ローカルアクセスの場合
　kubectl port-forward svc/argocd-server -n argocd 8080:443
```
#### ③パスワードの取得
```
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```
#### ④ArgoCDログイン
```
argocd login XXX.XXX.XXX.XXX ⇒　argocd-serverのIP
```
#### ⑤ArgoCDパスワード変更
```
argocd account update-password 
```
#### ⑥ArgoCDアプリの作成
```
argocd repo add git@github.com:ITC-cloud-soft/Saas-AppRelease.git --insecure-ignore-host-key --ssh-private-key-path id_ed25519
or (argocd repo add https://gitlab.thomaszou2077.com/apiadmin/api-apprelease.git --username yyyy --password xxxxxxxxxxx)
argocd app create saas-core --repo git@github.com:ITC-cloud-soft/Saas-AppRelease.git --revision main --path overlays/dev --dest-server https://kubernetes.default.svc --dest-namespace saas-core
argocd app sync saas-core
```
