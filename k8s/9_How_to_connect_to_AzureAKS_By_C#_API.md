# How to conntect to Azure AKS

要使用 C# 与 Azure Kubernetes Service (AKS) API 进行连接并进行身份验证，您需要使用 Azure Active Directory (Azure AD) 进行身份验证，以获取访问 AKS 集群所需的访问令牌。以下是一些基本步骤：

1. **注册应用程序并获取 Azure AD 身份验证信息**：
    - 登录到 Azure 门户。
    - 转到 Azure Active Directory。
    - 在 Azure AD 中注册您的应用程序，并获取客户端 ID 和客户端机密。
    - 配置重定向 URI，以允许 Azure AD 授权您的应用程序。

2. **使用 C# 编写代码**：在 C# 中编写代码来获取 AKS 集群的访问令牌并与 AKS API 进行交互。以下是一个示例代码片段：

```csharp
using Microsoft.Azure.Management.ContainerService;
using Microsoft.Azure.Management.ContainerService.Models;
using Microsoft.Azure.Services.AppAuthentication;
using Microsoft.Rest.Azure.Authentication;
using System;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        string clientId = "YourClientId";
        string clientSecret = "YourClientSecret";
        string tenantId = "YourTenantId";
        string subscriptionId = "YourSubscriptionId";
        string resourceGroupName = "YourResourceGroupName";
        string aksClusterName = "YourAKSClusterName";

        var azureServiceTokenProvider = new AzureServiceTokenProvider();

        string accessToken = await azureServiceTokenProvider.GetAccessTokenAsync("https://management.azure.com/");

        var serviceClientCredentials = ApplicationTokenProvider.LoginSilentAsync(tenantId, clientId, clientSecret).Result;

        var containerServiceClient = new ContainerServiceClient(serviceClientCredentials)
        {
            SubscriptionId = subscriptionId
        };

        ManagedCluster aksCluster = await containerServiceClient.ManagedClusters.GetByResourceGroupAsync(resourceGroupName, aksClusterName);

        Console.WriteLine($"AKS Cluster Name: {aksCluster.Name}");
        Console.WriteLine($"Kubernetes Version: {aksCluster.KubernetesVersion}");
    }
}
```

在上述代码中，您需要替换以下值：
- `YourClientId`：从 Azure AD 注册的应用程序中获取的客户端 ID。
- `YourClientSecret`：从 Azure AD 注册的应用程序中获取的客户端机密。
- `YourTenantId`：Azure AD 租户的 ID。
- `YourSubscriptionId`：Azure 订阅的 ID。
- `YourResourceGroupName`：AKS 集群所在的资源组名称。
- `YourAKSClusterName`：AKS 集群的名称。

请确保在代码中包含必要的依赖项，以便成功构建和运行此代码。

此示例中的代码可用于获取 AKS 集群的信息，您可以根据您的需求扩展它来执行其他 AKS API 操作。